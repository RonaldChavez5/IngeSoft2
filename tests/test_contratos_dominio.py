import unittest
from contextlib import redirect_stdout
from datetime import date, timedelta
from io import StringIO
from cdt import CDT
from cuenta import Cuenta
from cuenta_operable import CuentaOperable
from cuenta_ahorros import CuentaAhorros
from tarjeta_credito import TarjetaCredito
from credito_vivienda import CreditoVivienda
from generador_extractos import generar_extractos
from tests.dobles import crear_entorno


class PruebasContratosDominio(unittest.TestCase):
    def test_cdt_no_promete_operaciones_de_cuenta_disponible(self):
        cdt = CDT("CDT-1", "Ana", 100_000, date(2026, 11, 1))
        self.assertIsInstance(cdt, Cuenta)
        self.assertNotIsInstance(cdt, CuentaOperable)
        self.assertFalse(hasattr(cdt, "retirar"))
        self.assertFalse(hasattr(cdt, "cobrar_cuota"))
        with self.assertRaises(ValueError):
            cdt.redimir(date(2026, 10, 31))
        self.assertEqual(cdt.saldo, 100_000)
        self.assertEqual(cdt.redimir(date(2026, 11, 1)), 100_000)
        self.assertEqual(cdt.saldo, 0)

    def test_extractos_de_cuenta_tarjeta_credito_y_cdt(self):
        productos = [CuentaAhorros("1", "Ana", 100), TarjetaCredito(500),
                     CreditoVivienda(1_000), CDT("CDT", "Ana", 200, date(2027, 1, 1))]
        self.assertEqual(generar_extractos(productos), [
            "Cuenta 1 - saldo: $100.0", "Tarjeta - deuda: $0.0",
            "Crédito vivienda - pendiente: $1000.0", "Cuenta CDT - saldo: $200.0"])
        self.assertFalse(hasattr(productos[1], "depositar"))
        self.assertFalse(hasattr(productos[2], "retirar"))

    def test_internacional_conserva_formula_original(self):
        servicio, *_ = crear_entorno()
        origen, destino = CuentaAhorros("1", "Ana", 1_000_000), CuentaAhorros("2", "Luis", 0)
        tx = servicio.transferir(origen, destino, 100_000.0, "INTERNACIONAL")
        self.assertEqual(tx.comision, 28_000)
        self.assertEqual(origen.saldo, 872_000)
        self.assertEqual(destino.saldo, 100_000)

    def test_montos_invalidos_no_generan_efectos(self):
        for monto in [0, -1, 5_000_001]:
            with self.subTest(monto=monto):
                servicio, repo, avisos, recibos, eventos = crear_entorno()
                origen, destino = CuentaAhorros("1", "Ana", 9_000_000), CuentaAhorros("2", "Luis", 0)
                with self.assertRaises(ValueError):
                    servicio.transferir(origen, destino, monto, "MISMO_BANCO")
                self.assertEqual((origen.saldo, destino.saldo), (9_000_000, 0))
                self.assertEqual((repo.registros, avisos.mensajes, recibos.comprobantes, eventos.eventos),
                                 ([], [], [], []))

    def test_tope_exacto_cinco_millones_admitido(self):
        servicio, *_ = crear_entorno()
        origen, destino = CuentaAhorros("1", "Ana", 5_000_000), CuentaAhorros("2", "Luis", 0)
        servicio.transferir(origen, destino, 5_000_000.0, "MISMO_BANCO")
        self.assertEqual((origen.saldo, destino.saldo), (0, 5_000_000))

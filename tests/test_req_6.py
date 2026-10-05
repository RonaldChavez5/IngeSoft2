import unittest
from datetime import date, timedelta
from io import StringIO
from contextlib import redirect_stdout
from cdt import CDT
from cuenta_ahorros import CuentaAhorros
from cuenta_infantil import CuentaInfantil
from pago_servicio import PagoServicio
from comision_servicios import ComisionServicios
from tests.dobles import crear_entorno
from main import construir_servicio


class PruebasServiciosPublicos(unittest.TestCase):
    def test_pago_184300_descuenta_185800_y_reutiliza_pipeline(self):
        servicio, repo, avisos, recibos, eventos = crear_entorno(
            {"SERVICIO_PUBLICO": ComisionServicios()})
        cuenta = CuentaAhorros("1", "Ana", 500_000)
        tx = servicio.ejecutar(PagoServicio(cuenta, "FACT-123"),
                               184_300.0, "SERVICIO_PUBLICO")
        self.assertEqual(cuenta.saldo, 314_200)
        self.assertEqual(repo.registros, [("1", "FACT-123", 184_300.0, 1_500.0)])
        self.assertEqual(recibos.comprobantes, [tx])
        self.assertEqual(eventos.eventos, [tx])
        self.assertEqual(len(avisos.mensajes), 1)
        self.assertIn("FACT-123", avisos.mensajes[0][1])

    def test_integracion_comprobante_referencia_y_todos_los_canales(self):
        servicio = construir_servicio()
        salida = StringIO()
        with redirect_stdout(salida):
            servicio.ejecutar(PagoServicio(CuentaAhorros("1", "Ana", 500_000), "FACT-123"),
                               184_300.0, "SERVICIO_PUBLICO")
        texto = salida.getvalue()
        self.assertIn("Destino: FACT-123", texto)
        for etiqueta in ["[POSTGRES] INSERT", "[SMS] Para", "[PUSH] Para", "[AUDITORIA]", "[ANTIFRAUDE]"]:
            self.assertEqual(texto.count(etiqueta), 1)

    def test_mismos_montos_invalidos_y_saldo_insuficiente(self):
        for monto, saldo, error in [(0, 500_000, ValueError),
                                     (-1, 500_000, ValueError),
                                     (5_000_001, 9_000_000, ValueError),
                                     (184_300, 184_300, RuntimeError)]:
            with self.subTest(monto=monto):
                servicio, repo, avisos, recibos, eventos = crear_entorno(
                    {"SERVICIO_PUBLICO": ComisionServicios()})
                cuenta = CuentaAhorros("1", "Ana", saldo)
                with self.assertRaises(error):
                    servicio.ejecutar(PagoServicio(cuenta, "FACT-123"), monto, "SERVICIO_PUBLICO")
                self.assertEqual(cuenta.saldo, saldo)
                self.assertEqual(repo.registros, [])
                self.assertEqual(avisos.mensajes, [])
                self.assertEqual(recibos.comprobantes, [])
                self.assertEqual(eventos.eventos, [])

    def test_cdt_no_puede_pagar(self):
        cdt = CDT("CDT-1", "Ana", 1_000_000, date.today()+timedelta(days=180))
        with self.assertRaisesRegex(TypeError, "cuenta operable"):
            PagoServicio(cdt, "FACT-123")
        self.assertEqual(cdt.saldo, 1_000_000)

    def test_pago_infantil_respeta_limite_con_comision(self):
        servicio, repo, *_ = crear_entorno({"SERVICIO_PUBLICO": ComisionServicios()})
        cuenta = CuentaInfantil("INF-1", "Sara", 500_000)
        cuenta.retirar(150_000)
        with self.assertRaises(ValueError):
            servicio.ejecutar(PagoServicio(cuenta, "FACT-123"), 49_000.0, "SERVICIO_PUBLICO")
        self.assertEqual(cuenta.saldo, 350_000)
        self.assertEqual(repo.registros, [])

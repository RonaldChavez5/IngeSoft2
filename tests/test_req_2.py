import unittest
from datetime import date, timedelta
from contextlib import redirect_stdout
from io import StringIO
from cuenta_infantil import CuentaInfantil
from cuenta_ahorros import CuentaAhorros
from cobro_cuota_manejo import CobroCuotaManejo
from tests.dobles import crear_entorno


class PruebasCuentaInfantil(unittest.TestCase):
    def setUp(self):
        self.hoy = date(2026, 10, 4)
        self.cuenta = CuentaInfantil("INF-1", "Sara", 1_000_000, lambda: self.hoy)

    def test_150000_mas_60000_rechazado_saldo_intacto(self):
        self.cuenta.retirar(150_000)
        with self.assertRaisesRegex(ValueError, "límite diario"):
            self.cuenta.retirar(60_000)
        self.assertEqual(self.cuenta.saldo, 850_000)
        self.cuenta.retirar(50_000)
        self.assertEqual(self.cuenta.saldo, 800_000)

    def test_el_limite_se_reinicia_al_cambiar_dia(self):
        self.cuenta.retirar(200_000)
        self.hoy += timedelta(days=1)
        self.cuenta.retirar(200_000)
        self.assertEqual(self.cuenta.saldo, 600_000)

    def test_depositos_sin_tope_no_reinician_retiros(self):
        self.cuenta.retirar(200_000)
        self.cuenta.depositar(8_000_000)
        self.assertEqual(self.cuenta.saldo, 8_800_000)
        with self.assertRaises(ValueError):
            self.cuenta.retirar(1)

    def test_origen_transferencia_y_comision_cuentan_en_limite(self):
        servicio, repo, notificador, _, observador = crear_entorno()
        destino = CuentaAhorros("2", "Luis", 0)
        servicio.transferir(self.cuenta, destino, 150_000.0, "OTRO_BANCO")
        self.assertEqual(self.cuenta.saldo, 842_500)
        with self.assertRaises(ValueError):
            servicio.transferir(self.cuenta, destino, 50_000.0, "MISMO_BANCO")
        self.assertEqual(self.cuenta.saldo, 842_500)
        self.assertEqual(destino.saldo, 150_000)
        self.assertEqual(len(repo.registros), 1)
        self.assertEqual(len(notificador.mensajes), 1)
        self.assertEqual(len(observador.eventos), 1)

    def test_cuota_se_cobra_aun_con_limite_de_retiros_agotado(self):
        self.cuenta.retirar(200_000)
        with redirect_stdout(StringIO()):
            CobroCuotaManejo().cobrar_mensual([self.cuenta])
        self.assertEqual(self.cuenta.saldo, 787_100)

    def test_rechazo_por_saldo_no_consume_cupo_del_dia(self):
        cuenta = CuentaInfantil("INF-2", "Luz", 10_000, lambda: self.hoy)
        with self.assertRaises(RuntimeError):
            cuenta.retirar(100_000)
        cuenta.depositar(200_000)
        cuenta.retirar(200_000)
        self.assertEqual(cuenta.saldo, 10_000)

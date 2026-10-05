import unittest
from contextlib import redirect_stdout
from io import StringIO
from cuenta_ahorros import CuentaAhorros
from auditoria_consola import AuditoriaConsola
from antifraude_consola import AntifraudeConsola
from observador_multiple import ObservadorMultiple
from tests.dobles import crear_entorno


class PruebasAntifraude(unittest.TestCase):
    def test_transferencia_exitosa_audita_y_reporta_una_vez(self):
        servicio, *_ = crear_entorno()
        servicio.auditoria = ObservadorMultiple([AuditoriaConsola(), AntifraudeConsola()])
        salida = StringIO()
        with redirect_stdout(salida):
            servicio.transferir(CuentaAhorros("1", "Ana", 100_000),
                                CuentaAhorros("2", "Luis", 0), 50_000.0, "MISMO_BANCO")
        self.assertEqual(salida.getvalue().count("[AUDITORIA]"), 1)
        self.assertEqual(salida.getvalue().count("[ANTIFRAUDE]"), 1)

    def test_rechazada_no_produce_eventos(self):
        servicio, repo, notificador, _, _ = crear_entorno()
        servicio.auditoria = ObservadorMultiple([AuditoriaConsola(), AntifraudeConsola()])
        for monto, tipo, error in [(50_000, "MISMO_BANCO", RuntimeError),
                                   (0, "MISMO_BANCO", ValueError),
                                   (6_000_000, "MISMO_BANCO", ValueError),
                                   (1, "DESCONOCIDO", ValueError)]:
            with self.subTest(monto=monto, tipo=tipo):
                salida = StringIO()
                with redirect_stdout(salida), self.assertRaises(error):
                    servicio.transferir(CuentaAhorros("1", "Ana", 0),
                                        CuentaAhorros("2", "Luis", 0), monto, tipo)
                self.assertEqual(salida.getvalue(), "")
        self.assertEqual(repo.registros, [])
        self.assertEqual(notificador.mensajes, [])

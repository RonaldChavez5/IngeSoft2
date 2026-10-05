import unittest
from contextlib import redirect_stdout
from io import StringIO
from cuenta_ahorros import CuentaAhorros
from main import construir_servicio
from oracle_repositorio import OracleRepositorio


class PruebasMigracion(unittest.TestCase):
    def test_configuracion_real_usa_postgres_y_conserva_canales(self):
        servicio = construir_servicio()
        salida = StringIO()
        with redirect_stdout(salida):
            servicio.transferir(CuentaAhorros("1", "Ana", 100_000),
                                CuentaAhorros("2", "Luis", 0), 50_000.0, "LLAVE")
        texto = salida.getvalue()
        self.assertIn("[POSTGRES] INSERT INTO", texto)
        self.assertNotIn("[ORACLE]", texto)
        for etiqueta in ["[SMS] Para", "[PUSH] Para", "[AUDITORIA]", "[ANTIFRAUDE]"]:
            self.assertEqual(texto.count(etiqueta), 1)

    def test_oracle_se_puede_reconectar_sin_cambiar_servicio(self):
        servicio = construir_servicio()
        servicio.repositorio = OracleRepositorio()
        salida = StringIO()
        with redirect_stdout(salida):
            servicio.transferir(CuentaAhorros("1", "Ana", 100_000),
                                CuentaAhorros("2", "Luis", 0), 50_000.0, "MISMO_BANCO")
        self.assertIn("[ORACLE] INSERT INTO", salida.getvalue())
        self.assertNotIn("[POSTGRES]", salida.getvalue())

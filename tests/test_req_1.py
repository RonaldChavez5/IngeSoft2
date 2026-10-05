import unittest
from comision_llave import ComisionLlave
from cuenta_ahorros import CuentaAhorros
from tests.dobles import crear_entorno


class PruebasLlave(unittest.TestCase):
    def test_llave_descuenta_exactamente_50000(self):
        servicio, repo, notificador, _, _ = crear_entorno({"LLAVE": ComisionLlave()})
        origen = CuentaAhorros("1", "Ana", 100_000)
        destino = CuentaAhorros("2", "Luis", 0)
        tx = servicio.transferir(origen, destino, 50_000.0, "LLAVE")
        self.assertEqual(origen.saldo, 50_000)
        self.assertEqual(destino.saldo, 50_000)
        self.assertEqual(tx.comision, 0)
        self.assertEqual(len(repo.registros), 1)
        self.assertEqual(len(notificador.mensajes), 1)

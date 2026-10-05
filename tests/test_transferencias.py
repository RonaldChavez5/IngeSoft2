import unittest
from cuenta_ahorros import CuentaAhorros
from tests.dobles import crear_entorno


class PruebasTransferencias(unittest.TestCase):
    def setUp(self):
        (self.servicio, self.repositorio, self.notificador,
         self.comprobante, self.observador) = crear_entorno()
        self.ana = CuentaAhorros("001-1", "Ana", 2_000_000)
        self.luis = CuentaAhorros("001-2", "Luis", 500_000)

    def test_mismo_banco_sin_comision(self):
        tx = self.servicio.transferir(self.ana, self.luis, 150_000.0, "MISMO_BANCO")
        self.assertEqual(tx.comision, 0)
        self.assertEqual(self.ana.saldo, 1_850_000)
        self.assertEqual(self.luis.saldo, 650_000)

    def test_otro_banco_comision_7500(self):
        tx = self.servicio.transferir(self.ana, self.luis, 150_000.0, "OTRO_BANCO")
        self.assertEqual(tx.comision, 7_500)
        self.assertEqual(self.ana.saldo, 1_842_500)
        self.assertEqual(self.luis.saldo, 650_000)
        self.assertEqual(self.repositorio.registros,
                         [("001-1", "001-2", 150_000.0, 7_500.0)])

    def test_saldo_insuficiente_sin_efectos_externos(self):
        with self.assertRaisesRegex(RuntimeError, "Saldo insuficiente"):
            self.servicio.transferir(self.ana, self.luis, 2_000_000.0, "OTRO_BANCO")
        self.assertEqual(self.ana.saldo, 2_000_000)
        self.assertEqual(self.luis.saldo, 500_000)
        self.assertEqual(self.repositorio.registros, [])
        self.assertEqual(self.notificador.mensajes, [])
        self.assertEqual(self.comprobante.comprobantes, [])
        self.assertEqual(self.observador.eventos, [])

    def test_exito_se_guarda_y_notifica_una_sola_vez(self):
        tx = self.servicio.transferir(self.ana, self.luis, 50_000.0, "MISMO_BANCO")
        self.assertEqual(len(self.repositorio.registros), 1)
        self.assertEqual(len(self.notificador.mensajes), 1)
        self.assertEqual(self.comprobante.comprobantes, [tx])
        self.assertEqual(self.observador.eventos, [tx])

    def test_tipo_desconocido_no_cambia_saldos(self):
        with self.assertRaisesRegex(ValueError, "Tipo de transferencia desconocido"):
            self.servicio.transferir(self.ana, self.luis, 50_000.0, "DESCONOCIDO")
        self.assertEqual(self.ana.saldo, 2_000_000)
        self.assertEqual(self.luis.saldo, 500_000)
        self.assertEqual(self.repositorio.registros, [])
        self.assertEqual(self.notificador.mensajes, [])
        self.assertEqual(self.observador.eventos, [])


if __name__ == "__main__":
    unittest.main()

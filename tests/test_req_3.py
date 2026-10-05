import unittest
from contextlib import redirect_stdout
from io import StringIO
from cuenta_ahorros import CuentaAhorros
from notificador_multiple import NotificadorMultiple
from sms_gateway import SmsGateway
from push_gateway import PushGateway
from tests.dobles import crear_entorno, NotificadorEspia


class PruebasPush(unittest.TestCase):
    def test_cada_canal_recibe_un_solo_mensaje(self):
        servicio, *_ = crear_entorno()
        sms, push = NotificadorEspia(), NotificadorEspia()
        servicio.notificador = NotificadorMultiple([sms, push])
        servicio.transferir(CuentaAhorros("1", "Ana", 100_000),
                            CuentaAhorros("2", "Luis", 0), 50_000.0, "MISMO_BANCO")
        self.assertEqual(len(sms.mensajes), 1)
        self.assertEqual(push.mensajes, sms.mensajes)

    def test_consola_muestra_sms_y_push_por_transferencia(self):
        servicio, *_ = crear_entorno()
        servicio.notificador = NotificadorMultiple([SmsGateway(), PushGateway()])
        salida = StringIO()
        with redirect_stdout(salida):
            servicio.transferir(CuentaAhorros("1", "Ana", 100_000),
                                CuentaAhorros("2", "Luis", 0), 50_000.0, "MISMO_BANCO")
        self.assertEqual(salida.getvalue().count("[SMS] Para"), 1)
        self.assertEqual(salida.getvalue().count("[PUSH] Para"), 1)

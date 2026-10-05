from transaccion import Transaccion
from transaccion_service import TransaccionService
from validador_monto import ValidadorMonto
from comisiones import Comisiones
from politicas_comision import MismoBanco, OtroBanco, Internacional


class RepositorioMemoria:
    def __init__(self):
        self.registros = []

    def guardar_transaccion(self, origen, destino, monto, comision):
        self.registros.append((origen, destino, monto, comision))


class NotificadorEspia:
    def __init__(self):
        self.mensajes = []

    def enviar(self, destinatario, mensaje):
        self.mensajes.append((destinatario, mensaje))


class ComprobanteEspia:
    def __init__(self):
        self.comprobantes: list[Transaccion] = []

    def emitir(self, transaccion):
        self.comprobantes.append(transaccion)


class ObservadorEspia:
    def __init__(self):
        self.eventos: list[Transaccion] = []

    def registrar(self, transaccion):
        self.eventos.append(transaccion)


def crear_entorno(politicas_extra=None):
    politicas = {"MISMO_BANCO": MismoBanco(), "OTRO_BANCO": OtroBanco(),
                 "INTERNACIONAL": Internacional()}
    politicas.update(politicas_extra or {})
    repositorio = RepositorioMemoria()
    notificador = NotificadorEspia()
    comprobante = ComprobanteEspia()
    observador = ObservadorEspia()
    servicio = TransaccionService(ValidadorMonto(), Comisiones(politicas),
                                  repositorio, notificador, comprobante, observador)
    return servicio, repositorio, notificador, comprobante, observador

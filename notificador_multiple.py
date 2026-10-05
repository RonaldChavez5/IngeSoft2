from collections.abc import Iterable
from contratos import Notificador


class NotificadorMultiple:
    def __init__(self, canales: Iterable[Notificador]):
        self._canales = tuple(canales)

    def enviar(self, destinatario: str, mensaje: str) -> None:
        for canal in self._canales:
            canal.enviar(destinatario, mensaje)

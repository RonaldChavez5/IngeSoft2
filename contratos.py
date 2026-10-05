from typing import Protocol
from transaccion import Transaccion


class Validador(Protocol):
    def validar(self, monto: float) -> None: ...


class CalculadorComision(Protocol):
    def calcular(self, tipo: str, monto: float) -> float: ...


class Operacion(Protocol):
    def aplicar(self, monto: float, comision: float, tipo: str) -> Transaccion: ...


class RepositorioTransacciones(Protocol):
    def guardar_transaccion(self, origen: str, destino: str,
                            monto: float, comision: float) -> None: ...


class Notificador(Protocol):
    def enviar(self, destinatario: str, mensaje: str) -> None: ...


class EmisorComprobante(Protocol):
    def emitir(self, transaccion: Transaccion) -> None: ...


class ObservadorTransaccion(Protocol):
    def registrar(self, transaccion: Transaccion) -> None: ...

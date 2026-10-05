from collections.abc import Iterable
from contratos import ObservadorTransaccion
from transaccion import Transaccion


class ObservadorMultiple:
    def __init__(self, observadores: Iterable[ObservadorTransaccion]):
        self._observadores = tuple(observadores)

    def registrar(self, transaccion: Transaccion) -> None:
        for observador in self._observadores:
            observador.registrar(transaccion)

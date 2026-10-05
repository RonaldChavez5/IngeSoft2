from typing import Protocol


class GeneraExtracto(Protocol):
    def generar_extracto(self) -> str: ...


class DevengaIntereses(Protocol):
    def calcular_intereses(self) -> float: ...


class RecibeCuotas(Protocol):
    def pagar_cuota(self, monto: float) -> None: ...


class PermiteAvances(Protocol):
    def retirar(self, monto: float) -> None: ...

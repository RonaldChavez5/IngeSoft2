from typing import Protocol


class PoliticaComision(Protocol):
    def calcular(self, monto: float) -> float: ...


class MismoBanco:
    def calcular(self, monto: float) -> float:
        return 0.0


class OtroBanco:
    def calcular(self, monto: float) -> float:
        return 7_500.0


class Internacional:
    def calcular(self, monto: float) -> float:
        return monto * 0.03 + 25_000

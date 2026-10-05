from datetime import date
from cuenta import Cuenta


class CDT(Cuenta):
    """Inversión a término; no ofrece retiro ni cobro mensual de cuenta operable."""

    def __init__(self, numero: str, titular: str, monto: float, vencimiento: date):
        super().__init__(numero, titular, monto)
        self.vencimiento = vencimiento

    def redimir(self, hoy: date) -> float:
        if hoy < self.vencimiento:
            raise ValueError("El CDT aún no ha vencido")
        monto = self.saldo
        self.saldo = 0.0
        return monto

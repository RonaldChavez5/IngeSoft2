from datetime import date
from cuenta import Cuenta


class CDT(Cuenta):
    def __init__(self, numero: str, titular: str, monto: float, vencimiento: date):
        super().__init__(numero, titular, monto)
        self.vencimiento = vencimiento

    def retirar(self, monto: float) -> None:
        if date.today() < self.vencimiento:
            raise NotImplementedError("Un CDT no permite retiros antes del vencimiento")
        super().retirar(monto)

from collections.abc import Callable
from datetime import date
from cuenta_operable import CuentaOperable


class CuentaInfantil(CuentaOperable):
    LIMITE_DIARIO = 200_000.0

    def __init__(self, numero: str, titular: str, saldo_inicial: float,
                 reloj: Callable[[], date] = date.today):
        super().__init__(numero, titular, saldo_inicial)
        self._reloj = reloj
        self._fecha_retiros = reloj()
        self._retirado_hoy = 0.0

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")
        hoy = self._reloj()
        acumulado = self._retirado_hoy if hoy == self._fecha_retiros else 0.0
        if acumulado + monto > self.LIMITE_DIARIO:
            raise ValueError("Supera el límite diario de retiros de $200.000")
        super().retirar(monto)
        self._fecha_retiros = hoy
        self._retirado_hoy = acumulado + monto

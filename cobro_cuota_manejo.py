from collections.abc import Iterable
from cuenta_operable import CuentaOperable


class CobroCuotaManejo:
    CUOTA = 12_900.0

    def cobrar_mensual(self, cuentas: Iterable[CuentaOperable]) -> None:
        for cuenta in cuentas:
            cuenta.cobrar_cuota(self.CUOTA)
            print(f"Cuota de manejo cobrada a {cuenta.numero}")

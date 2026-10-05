from cuenta import Cuenta


class CobroCuotaManejo:
    CUOTA = 12_900.0

    def cobrar_mensual(self, cuentas: list[Cuenta]) -> None:
        for cuenta in cuentas:
            cuenta.retirar(self.CUOTA)
            print(f"Cuota de manejo cobrada a {cuenta.numero}")

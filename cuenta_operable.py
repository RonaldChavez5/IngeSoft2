from cuenta import Cuenta


class CuentaOperable(Cuenta):
    """Retiros sujetos a saldo y a las condiciones de disponibilidad del producto.

    Un rechazo debe dejar intacto el saldo. Los depósitos positivos no tienen tope.
    La cuota administrativa es independiente de los retiros voluntarios.
    """

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")
        self.saldo += monto

    def retirar(self, monto: float) -> None:
        self._debitar(monto)

    def _debitar(self, monto: float) -> None:
        if monto > self.saldo:
            raise RuntimeError("Saldo insuficiente")
        self.saldo -= monto

    def cobrar_cuota(self, monto: float) -> None:
        self._debitar(monto)

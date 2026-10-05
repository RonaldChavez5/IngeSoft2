from cuenta import Cuenta
from transaccion import Transaccion


class Transferencia:
    """Movimiento de dinero entre dos cuentas; no conoce proveedores externos."""

    def __init__(self, origen: Cuenta, destino: Cuenta):
        self.origen = origen
        self.destino = destino

    def aplicar(self, monto: float, comision: float, tipo: str) -> Transaccion:
        self.origen.retirar(monto + comision)
        self.destino.depositar(monto)
        return Transaccion(self.origen.numero, self.destino.numero,
                           self.origen.titular, monto, comision, tipo,
                           f"Transferiste ${monto} a la cuenta {self.destino.numero}")

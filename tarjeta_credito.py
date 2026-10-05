from producto_bancario import ProductoBancario


class TarjetaCredito(ProductoBancario):
    def __init__(self, cupo: float):
        self.deuda = 0.0
        self.cupo = float(cupo)

    def depositar(self, monto: float) -> None:
        pass  # no aplica

    def retirar(self, monto: float) -> None:
        if self.deuda + monto > self.cupo:
            raise RuntimeError("Cupo insuficiente")
        self.deuda += monto

    def calcular_intereses(self) -> float:
        return self.deuda * 0.028

    def pagar_cuota(self, monto: float) -> None:
        self.deuda -= monto

    def generar_extracto(self) -> str:
        return f"Tarjeta - deuda: ${self.deuda}"

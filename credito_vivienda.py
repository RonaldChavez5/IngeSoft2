class CreditoVivienda:
    def __init__(self, valor_prestamo: float):
        self.saldo_pendiente = float(valor_prestamo)

    def calcular_intereses(self) -> float:
        return self.saldo_pendiente * 0.011

    def pagar_cuota(self, monto: float) -> None:
        self.saldo_pendiente -= monto

    def generar_extracto(self) -> str:
        return f"Crédito vivienda - pendiente: ${self.saldo_pendiente}"

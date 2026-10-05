class Cuenta:
    """Datos comunes de una cuenta; no promete disponibilidad del dinero."""

    def __init__(self, numero: str, titular: str, saldo_inicial: float):
        self.numero = numero
        self.titular = titular
        self.saldo = float(saldo_inicial)

    def generar_extracto(self) -> str:
        return f"Cuenta {self.numero} - saldo: ${self.saldo}"

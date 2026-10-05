class Cuenta:
    def __init__(self, numero: str, titular: str, saldo_inicial: float):
        self.numero = numero
        self.titular = titular
        self.saldo = float(saldo_inicial)

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")
        self.saldo += monto

    def retirar(self, monto: float) -> None:
        if monto > self.saldo:
            raise RuntimeError("Saldo insuficiente")
        self.saldo -= monto

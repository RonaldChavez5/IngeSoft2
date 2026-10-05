class ValidadorMonto:
    def validar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")
        if monto > 5_000_000:
            raise ValueError("Supera el tope diario")

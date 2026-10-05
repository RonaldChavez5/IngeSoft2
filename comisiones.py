class Comisiones:
    def calcular(self, tipo: str, monto: float) -> float:
        if tipo == "MISMO_BANCO":
            return 0.0
        if tipo == "OTRO_BANCO":
            return 7_500.0
        if tipo == "INTERNACIONAL":
            return monto * 0.03 + 25_000
        raise ValueError("Tipo de transferencia desconocido")

from collections.abc import Mapping
from politicas_comision import PoliticaComision


class Comisiones:
    def __init__(self, politicas: Mapping[str, PoliticaComision]):
        self._politicas = dict(politicas)

    def calcular(self, tipo: str, monto: float) -> float:
        try:
            politica = self._politicas[tipo]
        except KeyError:
            raise ValueError("Tipo de transferencia desconocido") from None
        return politica.calcular(monto)

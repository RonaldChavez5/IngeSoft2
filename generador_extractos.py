from collections.abc import Iterable
from producto_bancario import GeneraExtracto


def generar_extractos(productos: Iterable[GeneraExtracto]) -> list[str]:
    return [producto.generar_extracto() for producto in productos]

from dataclasses import dataclass


@dataclass(frozen=True)
class Transaccion:
    origen: str
    destino: str
    titular: str
    monto: float
    comision: float
    tipo: str
    mensaje: str

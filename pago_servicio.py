from cuenta_operable import CuentaOperable
from transaccion import Transaccion


class PagoServicio:
    """Débito para una factura; la referencia es el destino del comprobante."""

    def __init__(self, origen: CuentaOperable, referencia: str):
        if not isinstance(origen, CuentaOperable):
            raise TypeError("El pago requiere una cuenta operable")
        if not referencia.strip():
            raise ValueError("La referencia de la factura es obligatoria")
        self.origen = origen
        self.referencia = referencia

    def aplicar(self, monto: float, comision: float, tipo: str) -> Transaccion:
        self.origen.retirar(monto + comision)
        return Transaccion(self.origen.numero, self.referencia, self.origen.titular,
                           monto, comision, tipo,
                           f"Pagaste ${monto} a la factura {self.referencia}")

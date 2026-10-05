from transaccion import Transaccion


class ComprobanteConsola:
    def emitir(self, transaccion: Transaccion) -> None:
        print("===== BANCO ANDINO - COMPROBANTE =====")
        print(f"Origen: {transaccion.origen}")
        print(f"Destino: {transaccion.destino}")
        print(f"Monto:    ${transaccion.monto}")
        print(f"Comisión: ${transaccion.comision}")
        print("======================================")

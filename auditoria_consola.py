from datetime import datetime
from transaccion import Transaccion


class AuditoriaConsola:
    def registrar(self, transaccion: Transaccion) -> None:
        print(f"[AUDITORIA] {datetime.now().isoformat()} {transaccion.tipo} "
              f"{transaccion.origen} -> {transaccion.destino} ${transaccion.monto}")

from transaccion import Transaccion


class AntifraudeConsola:
    def registrar(self, transaccion: Transaccion) -> None:
        print(f"[ANTIFRAUDE] {transaccion.tipo} {transaccion.origen} "
              f"-> {transaccion.destino} ${transaccion.monto}")

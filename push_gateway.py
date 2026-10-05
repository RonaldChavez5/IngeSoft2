class PushGateway:
    def enviar(self, destinatario: str, mensaje: str) -> None:
        print(f"[PUSH] Para {destinatario}: {mensaje}")

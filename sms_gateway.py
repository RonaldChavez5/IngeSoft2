class SmsGateway:
    def enviar(self, destinatario: str, mensaje: str) -> None:
        print("[SMS] Conectando al proveedor de mensajería...")
        print(f"[SMS] Para {destinatario}: {mensaje}")

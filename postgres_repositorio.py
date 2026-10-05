class PostgresRepositorio:
    def guardar_transaccion(self, origen: str, destino: str,
                            monto: float, comision: float) -> None:
        print("[POSTGRES] Conectando a postgresql://prod-db/BANCO...")
        print(f"[POSTGRES] INSERT INTO transacciones VALUES ('{origen}', '{destino}', {monto}, {comision})")

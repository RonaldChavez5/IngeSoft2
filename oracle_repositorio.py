class OracleRepositorio:
    def guardar_transaccion(self, origen: str, destino: str,
                            monto: float, comision: float) -> None:
        print("[ORACLE] Conectando a jdbc:oracle:thin:@prod-db:1521/BANCO...")
        print(f"[ORACLE] INSERT INTO transacciones VALUES ('{origen}', '{destino}', {monto}, {comision})")

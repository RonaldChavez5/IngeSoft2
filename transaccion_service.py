from contratos import (Validador, CalculadorComision, Operacion,
                       RepositorioTransacciones, Notificador,
                       EmisorComprobante, ObservadorTransaccion)
from cuenta_operable import CuentaOperable
from transferencia import Transferencia
from transaccion import Transaccion


class TransaccionService:
    """Coordina el flujo de una operación con dependencias inyectadas."""

    def __init__(self, validador: Validador, comisiones: CalculadorComision,
                 repositorio: RepositorioTransacciones, notificador: Notificador,
                 comprobante: EmisorComprobante, auditoria: ObservadorTransaccion):
        self.validador = validador
        self.comisiones = comisiones
        self.repositorio = repositorio
        self.notificador = notificador
        self.comprobante = comprobante
        self.auditoria = auditoria

    def transferir(self, origen: CuentaOperable, destino: CuentaOperable,
                   monto: float, tipo: str) -> Transaccion:
        return self.ejecutar(Transferencia(origen, destino), monto, tipo)

    def ejecutar(self, operacion: Operacion, monto: float, tipo: str) -> Transaccion:
        self.validador.validar(monto)
        comision = self.comisiones.calcular(tipo, monto)
        transaccion = operacion.aplicar(monto, comision, tipo)
        self.repositorio.guardar_transaccion(transaccion.origen, transaccion.destino,
                                            monto, comision)
        self.comprobante.emitir(transaccion)
        self.notificador.enviar(transaccion.titular, transaccion.mensaje)
        self.auditoria.registrar(transaccion)
        return transaccion

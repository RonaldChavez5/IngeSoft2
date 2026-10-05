from cuenta_operable import CuentaOperable
from transferencia import Transferencia
from validador_monto import ValidadorMonto
from comisiones import Comisiones
from oracle_repositorio import OracleRepositorio
from sms_gateway import SmsGateway
from comprobante_consola import ComprobanteConsola
from auditoria_consola import AuditoriaConsola


class TransaccionService:
    def __init__(self, comisiones: Comisiones):
        self.validador = ValidadorMonto()
        self.comisiones = comisiones
        self.repositorio = OracleRepositorio()
        self.notificador = SmsGateway()
        self.comprobante = ComprobanteConsola()
        self.auditoria = AuditoriaConsola()

    def transferir(self, origen: CuentaOperable, destino: CuentaOperable,
                   monto: float, tipo: str) -> None:
        self.ejecutar(Transferencia(origen, destino), monto, tipo)

    def ejecutar(self, operacion: Transferencia, monto: float, tipo: str) -> None:
        self.validador.validar(monto)
        comision = self.comisiones.calcular(tipo, monto)
        transaccion = operacion.aplicar(monto, comision, tipo)
        self.repositorio.guardar_transaccion(transaccion.origen, transaccion.destino,
                                            monto, comision)
        self.comprobante.emitir(transaccion)
        self.notificador.enviar(transaccion.titular, transaccion.mensaje)
        self.auditoria.registrar(transaccion)

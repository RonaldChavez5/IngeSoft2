from datetime import date, timedelta
from comisiones import Comisiones
from politicas_comision import MismoBanco, OtroBanco, Internacional
from cuenta_ahorros import CuentaAhorros
from cdt import CDT
from transaccion_service import TransaccionService
from cobro_cuota_manejo import CobroCuotaManejo
from tarjeta_credito import TarjetaCredito
from credito_vivienda import CreditoVivienda
from generador_extractos import generar_extractos
from validador_monto import ValidadorMonto
from oracle_repositorio import OracleRepositorio
from sms_gateway import SmsGateway
from comprobante_consola import ComprobanteConsola
from auditoria_consola import AuditoriaConsola


def construir_servicio() -> TransaccionService:
    return TransaccionService(
        ValidadorMonto(),
        Comisiones({"MISMO_BANCO": MismoBanco(), "OTRO_BANCO": OtroBanco(),
                    "INTERNACIONAL": Internacional()}),
        OracleRepositorio(), SmsGateway(), ComprobanteConsola(), AuditoriaConsola(),
    )


def main() -> None:
    ana = CuentaAhorros("001-1", "Ana", 2_000_000)
    luis = CuentaAhorros("001-2", "Luis", 500_000)
    cdt_ana = CDT("CDT-9", "Ana", 10_000_000, date.today() + timedelta(days=183))
    servicio = construir_servicio()
    servicio.transferir(ana, luis, 150_000.0, "OTRO_BANCO")
    CobroCuotaManejo().cobrar_mensual([ana, luis])
    productos = [TarjetaCredito(3_000_000), CreditoVivienda(120_000_000)]
    for extracto in generar_extractos(productos):
        print(extracto)


if __name__ == "__main__":
    main()

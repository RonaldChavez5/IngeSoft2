# UML final - rama main, R1 a R5

Las interfaces `Protocol` se implementan estructuralmente: tener los métodos
indicados cumple el contrato, sin una cláusula `implements` explícita.
Se muestran tres vistas del mismo modelo para mantener legibles sus relaciones.
La demostración R6 agrega `PagoServicio ..|> Operacion` y
`ComisionServicios ..|> PoliticaComision`; solo se encuentra en `demo-r6`.

## Dominio y capacidades

```mermaid
classDiagram
    direction TB
    class Cuenta {
        +numero: str
        +titular: str
        +saldo: float
        +generar_extracto() str
    }
    class CuentaOperable {
        +depositar(monto)
        +retirar(monto)
        +cobrar_cuota(monto)
    }
    class CuentaAhorros
    class CuentaInfantil {
        +LIMITE_DIARIO: float
        -reloj
        -fecha_retiros
        -retirado_hoy
        +retirar(monto)
    }
    class CDT {
        +vencimiento: date
        +redimir(hoy) float
    }
    class CobroCuotaManejo {
        +cobrar_mensual(cuentas)
    }
    class GeneraExtracto {
        <<interface>>
        +generar_extracto() str
    }
    class DevengaIntereses {
        <<interface>>
        +calcular_intereses() float
    }
    class RecibeCuotas {
        <<interface>>
        +pagar_cuota(monto)
    }
    class PermiteAvances {
        <<interface>>
        +retirar(monto)
    }
    class TarjetaCredito
    class CreditoVivienda
    class GeneradorExtractos {
        <<function>>
        +generar_extractos(productos) list
    }
    Cuenta <|-- CuentaOperable
    Cuenta <|-- CDT
    CuentaOperable <|-- CuentaAhorros
    CuentaOperable <|-- CuentaInfantil
    Cuenta ..|> GeneraExtracto
    TarjetaCredito ..|> GeneraExtracto
    CreditoVivienda ..|> GeneraExtracto
    TarjetaCredito ..|> DevengaIntereses
    CreditoVivienda ..|> DevengaIntereses
    TarjetaCredito ..|> RecibeCuotas
    CreditoVivienda ..|> RecibeCuotas
    TarjetaCredito ..|> PermiteAvances
    CobroCuotaManejo ..> CuentaOperable : cobra
    GeneradorExtractos ..> GeneraExtracto : consume
```

## Flujo y comisiones

```mermaid
classDiagram
    direction TB
    class TransaccionService {
        +transferir(origen, destino, monto, tipo) Transaccion
        +ejecutar(operacion, monto, tipo) Transaccion
    }
    class Operacion {
        <<interface>>
        +aplicar(monto, comision, tipo) Transaccion
    }
    class Transferencia {
        +origen: CuentaOperable
        +destino: CuentaOperable
        +aplicar(monto, comision, tipo) Transaccion
    }
    class Transaccion {
        <<immutable>>
        +origen: str
        +destino: str
        +titular: str
        +monto: float
        +comision: float
        +tipo: str
        +mensaje: str
    }
    class Validador {
        <<interface>>
        +validar(monto)
    }
    class ValidadorMonto
    class CalculadorComision {
        <<interface>>
        +calcular(tipo, monto) float
    }
    class Comisiones {
        -politicas: dict
        +calcular(tipo, monto) float
    }
    class PoliticaComision {
        <<interface>>
        +calcular(monto) float
    }
    class MismoBanco
    class OtroBanco
    class Internacional
    class ComisionLlave
    Operacion <|.. Transferencia
    Validador <|.. ValidadorMonto
    CalculadorComision <|.. Comisiones
    PoliticaComision <|.. MismoBanco
    PoliticaComision <|.. OtroBanco
    PoliticaComision <|.. Internacional
    PoliticaComision <|.. ComisionLlave
    Comisiones o-- PoliticaComision : registro
    TransaccionService ..> Validador : inyectado
    TransaccionService ..> CalculadorComision : inyectado
    TransaccionService ..> Operacion : ejecuta
    TransaccionService ..> Transferencia : crea operación de dominio
    Transferencia ..> CuentaOperable : debita y acredita
    Transferencia ..> Transaccion : crea resultado
    TransaccionService ..> Transaccion : retorna
```

## Infraestructura y composición

```mermaid
classDiagram
    direction TB
    class TransaccionService
    class RepositorioTransacciones {
        <<interface>>
        +guardar_transaccion(origen, destino, monto, comision)
    }
    class Notificador {
        <<interface>>
        +enviar(destinatario, mensaje)
    }
    class EmisorComprobante {
        <<interface>>
        +emitir(transaccion)
    }
    class ObservadorTransaccion {
        <<interface>>
        +registrar(transaccion)
    }
    class OracleRepositorio
    class PostgresRepositorio
    class SmsGateway
    class PushGateway
    class NotificadorMultiple
    class ComprobanteConsola
    class AuditoriaConsola
    class AntifraudeConsola
    class ObservadorMultiple
    class Main {
        <<module>>
        +construir_servicio() TransaccionService
        +main()
    }
    RepositorioTransacciones <|.. OracleRepositorio
    RepositorioTransacciones <|.. PostgresRepositorio
    Notificador <|.. SmsGateway
    Notificador <|.. PushGateway
    Notificador <|.. NotificadorMultiple
    NotificadorMultiple o-- Notificador : canales
    EmisorComprobante <|.. ComprobanteConsola
    ObservadorTransaccion <|.. AuditoriaConsola
    ObservadorTransaccion <|.. AntifraudeConsola
    ObservadorTransaccion <|.. ObservadorMultiple
    ObservadorMultiple o-- ObservadorTransaccion : observadores
    TransaccionService ..> RepositorioTransacciones : inyectado
    TransaccionService ..> Notificador : inyectado
    TransaccionService ..> EmisorComprobante : inyectado
    TransaccionService ..> ObservadorTransaccion : inyectado
    Main ..> TransaccionService : construye
    Main ..> PostgresRepositorio : construye
    Main ..> NotificadorMultiple : construye
    Main ..> SmsGateway : construye
    Main ..> PushGateway : construye
    Main ..> ComprobanteConsola : construye
    Main ..> ObservadorMultiple : construye
    Main ..> AuditoriaConsola : construye
    Main ..> AntifraudeConsola : construye
    Main ..> ValidadorMonto : construye
    Main ..> Comisiones : construye
    Main ..> MismoBanco : registra
    Main ..> OtroBanco : registra
    Main ..> Internacional : registra
    Main ..> ComisionLlave : registra
```

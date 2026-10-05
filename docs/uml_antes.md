# UML original

Las líneas y clases rojas señalan herencia, contratos o dependencias problemáticas.
La flecha sólida con triángulo representa herencia; la discontinua con triángulo,
implementación; la flecha discontinua simple, dependencia.

```mermaid
classDiagram
    direction TB
    class Cuenta {
        +numero: str
        +titular: str
        +saldo: float
        +depositar(monto)
        +retirar(monto)
    }
    class CuentaAhorros
    class CDT {
        +vencimiento: date
        +retirar(monto)
    }
    class TransaccionService {
        +transferir(origen, destino, monto, tipo)
    }
    class OracleRepositorio {
        +guardar_transaccion(origen, destino, monto, comision)
    }
    class SmsGateway {
        +enviar(destinatario, mensaje)
    }
    class CobroCuotaManejo {
        +cobrar_mensual(cuentas)
    }
    class ProductoBancario {
        <<interface>>
        +depositar(monto)
        +retirar(monto)
        +calcular_intereses()
        +pagar_cuota(monto)
        +generar_extracto()
    }
    class TarjetaCredito
    class CreditoVivienda
    class Main
    Cuenta <|-- CuentaAhorros
    Cuenta <|-- CDT
    ProductoBancario <|.. TarjetaCredito
    ProductoBancario <|.. CreditoVivienda
    TransaccionService ..> OracleRepositorio : new
    TransaccionService ..> SmsGateway : new
    TransaccionService ..> Cuenta : usa
    CobroCuotaManejo ..> Cuenta : cobra
    Main ..> CuentaAhorros : new
    Main ..> CDT : new
    Main ..> TransaccionService : new
    Main ..> CobroCuotaManejo : new
    Main ..> TarjetaCredito : new
    Main ..> CreditoVivienda : new
    style CDT fill:#fee2e2,stroke:#dc2626
    style ProductoBancario fill:#fee2e2,stroke:#dc2626
    style TransaccionService fill:#fee2e2,stroke:#dc2626
    linkStyle 1,2,3,4,5,7 stroke:#dc2626,stroke-width:2px
```

# Laboratorio L2: SOLID - Banco Andino

Ingeniería de Software II · Universidad Nacional de Colombia, sede Bogotá · 2026.

## Lenguaje y ejecución

Python 3.12 o superior, solo biblioteca estándar. Se eligió porque permite ejecutar
el programa y `unittest` sin instalar una base de datos ni librerías externas.

```bash
python main.py
```

La traducción conserva los 11 archivos y los defectos del original. `ValueError`
equivale a argumento inválido; `RuntimeError`, a estado inválido; y
`NotImplementedError`, al retiro no soportado del CDT. Los valores se convierten
a `float` para conservar el modelo `double`. Se usan 183 días para representar
el CDT futuro de la demostración; el día exacto no interviene en la salida.
La caracterización compara el código Python original con su refactorización,
no las convenciones de formato numérico de Java contra las de Python.

## Bloque 0. Arranque

La ejecución mueve $150.000 de Ana a Luis y cobra $7.500 de comisión. Luego
cobra $12.900 a cada cuenta. Los saldos finales son $1.829.600 y $637.100.
La salida original está en [salida_original.txt](salida_original.txt).

## Bloque 1. Diagnóstico

| Clase / método | Letra | Evidencia | Consecuencia para el banco o cliente |
|---|---|---|---|
| `TransaccionService.transferir` | S | Valida, calcula comisión, mueve dinero, guarda, imprime, notifica y audita. | Cambiar un comprobante obliga a tocar el mismo método que descuenta el dinero. |
| `TransaccionService.transferir` | O | Cadena `if/elif` por tipo, equivalente al `switch` original. | Una modalidad nueva obliga a editar código de transferencias que ya estaba funcionando. |
| `CDT.retirar` / `Cuenta` | L | La subclase añade el rechazo por vencimiento a una operación que la cuenta base permite con saldo suficiente. | El cobro nocturno puede detenerse al encontrar un CDT y dejar cuentas sin procesar. |
| `ProductoBancario` | I | Obliga a todos los productos a ofrecer depósitos, retiros, intereses, pagos y extractos. | Se aceptan operaciones que no hacen nada: el cliente puede creer que movió dinero. |
| `TarjetaCredito.depositar`, `CreditoVivienda.depositar/retirar` | I | Tres métodos vacíos por “no aplica”. | Los errores de uso quedan ocultos en vez de verse en el contrato del producto. |
| `TransaccionService.__init__` | D | Construye `OracleRepositorio` y `SmsGateway` directamente. | Probar una comisión activa también persistencia y mensajería; migrar de proveedor exige modificar el servicio. |
| `CobroCuotaManejo.cobrar_mensual` | L | Recibe cualquier `Cuenta`, incluidos los CDT. | El tipo de entrada promete una capacidad que algunos elementos no tienen. |

### Experimento 1: incluir el CDT en el cobro

Ejecución real: [experimento_cdt.txt](docs/experimento_cdt.txt). Se colocó el CDT
entre Ana y Luis para observar tanto lo ya cobrado como lo que queda pendiente.
Ana queda con $1.987.100; el CDT lanza `NotImplementedError`; Luis conserva
$500.000. No hay reversión del primer cobro. Si el CDT ocupa el lugar 500.000,
las primeras 499.999 cuentas pudieron cobrar y las posteriores quedan pendientes.
Reintentar toda la lista sin un control adicional puede duplicar los cobros.

### Experimento 2: probar la comisión sin Oracle ni SMS

La comisión se pudo comprobar, pero aparecieron mensajes de Oracle y SMS:
[experimento_acoplamiento.txt](docs/experimento_acoplamiento.txt).
En este laboratorio los proveedores son simulados: no hubo conexión real.
El constructor no permite sustituirlos por dobles mediante su interfaz pública.
En Python sería posible usar `patch` o reasignar atributos después de construir;
por eso la prueba no es literalmente imposible, pero dependería de los detalles
internos y el constructor de un proveedor real ya podría tener efectos externos.

### Medición antes de refactorizar

| Métrica | Antes |
|---|---:|
| Líneas de `transferir` | 38 |
| Razones de cambio del servicio | 7 |
| Clases concretas construidas por el servicio | 2 |
| Métodos vacíos o rechazo por “no aplica” | 4 |
| ¿Se prueba sin Oracle ni SMS por inyección pública? | No |
| Archivos de código de producción | 11 |

Se cuentan líneas físicas desde `def` hasta la última sentencia, incluidos
comentarios y blancos internos. Los cuatro métodos problemáticos son los tres
vacíos y el retiro prematuro del CDT; las declaraciones abstractas no cuentan.
Las siete razones de cambio son las siete etapas del método original.
El diagrama original se conserva en `docs/uml_antes.md`.

## Bloque 2. Refactorización por controles

### Control S

`TransaccionService` coordina el procesamiento de una transacción.
La frase no necesita “y”: las reglas se ejecutan en colaboradores separados.
Si cambia el formato legal, se modifica `comprobante_consola.py`.
`Transferencia` mueve el dinero; `Transaccion` conserva los datos del resultado.
El método `ejecutar` centraliza el orden de los pasos y `transferir` es su entrada
para transferencias. Extraer la orquestación no elimina pasos: permite compartir
el mismo flujo con otras operaciones sin duplicarlo.
La comparación automática pasó: `docs/salidas/control-S-comparacion.txt`.

### Control O

Un nuevo tipo necesita una política nueva y su registro en `main.py`.
Ese es el único archivo existente que debe cambiar para conectar el tipo nuevo.
El servicio y el selector `Comisiones` permanecen intactos. El diccionario
sustituye la decisión por tipos; un tipo desconocido todavía se rechaza.
La comparación pasó: `docs/salidas/control-O-comparacion.txt`.

### Control L

`Cuenta` contiene los datos comunes. `CuentaOperable` ofrece depósito, retiro y
cuota; `CuentaAhorros` pertenece a esa rama. `CDT` pertenece solo a `Cuenta` y
ofrece `redimir(hoy)`, con su condición de vencimiento explícita. Un CDT no es
un origen válido ni una cuenta a la que se le cobre la cuota mensual.

Python no verifica anotaciones al ejecutar. Un verificador estático como mypy
puede señalar el uso de `CDT` donde se pide `CuentaOperable`; sin ese verificador,
un uso incorrecto se detecta al ejecutar. No afirmamos una protección de compilación
que Python no ofrece por sí solo. Detectarlo antes de ejecutar evita descubrirlo
en medio del lote. Un `try/except` que ignore CDT ocultaría el contrato incorrecto
y no impediría volver a pasar uno a una transferencia.

La comparación pasó: `docs/salidas/control-L-comparacion.txt`.

### Control I

`GeneraExtracto` permite generar extractos de cuentas, tarjetas y créditos con
el mismo generador. Solo pide `generar_extracto`; no necesita conocer depósitos,
avances ni pagos. En Python los protocolos se cumplen de forma estructural:
la clase no tiene que heredar explícitamente de la interfaz.
`DevengaIntereses`, `RecibeCuotas` y `PermiteAvances` nombran las capacidades
restantes; ningún producto conserva operaciones vacías por “no aplica”.
La comparación pasó: `docs/salidas/control-I-comparacion.txt`.

### Control D

El servicio recibe seis colaboradores mediante protocolos. `main.py` decide
qué repositorio, notificador, comprobante y observador conectar. El servicio
construye **cero proveedores concretos**. Conoce `Transferencia` como operación
de dominio y `Transaccion` como dato de resultado; no sería correcto decir que
no conoce ninguna clase concreta. Construye una `Transferencia` por llamada,
no una conexión ni un proveedor. En Python esta llamada equivale a un `new`
de Java. Esta distinción se mantiene en las métricas finales.

Ahora se puede inyectar un repositorio en memoria y un notificador espía desde
el constructor. No hace falta modificar el servicio ni parchear sus detalles.
La comparación pasó: `docs/salidas/control-D-comparacion.txt`.

## Bloque 3. Pruebas unitarias

```bash
python -m unittest discover -v
```

Las cinco pruebas obligatorias usan `RepositorioMemoria`, `NotificadorEspia`,
`ComprobanteEspia` y `ObservadorEspia`. No importan Oracle ni SMS.
Cubren comisión cero, comisión de $7.500, rechazo por saldo, efectos exactamente
una vez y tipo desconocido. Además de la excepción, verifican saldo y efectos.

El tiempo medido está en [pruebas_bloque_3.txt](docs/pruebas_bloque_3.txt).
Es el tiempo del framework para la suite, no incluye el arranque del intérprete
y puede redondearse a 0,000 s en estas pruebas pequeñas. No es un benchmark.
Se cambiaron **0 líneas de TransaccionService** para escribirlas. En el bloque 1
hubiéramos tenido que ejecutar los proveedores simulados o parchear internos.

## Bloque 4. Requerimientos del negocio

Las estimaciones se escribieron antes de implementar cada cambio. Se comparan
archivos **de producción**: módulos `.py` en la raíz. Las pruebas y la documentación
se contabilizan aparte, para no confundir diseño con evidencia. Los JSON de cada
requerimiento enumeran nombres y permiten contrastarlos con `git show --stat`.

### R1: resultado registrado

Archivos de producción existentes modificados: 1.
Archivos de producción nuevos: 1.
Detalle verificable: `docs/cambios_req_1.json`. La suite completa pasó y
las cinco pruebas originales no cambiaron: `docs/pruebas_req_1.txt`.

Decisiones de R2: “día” significa fecha local del reloj inyectado (en una instalación
colombiana se debe configurar esa zona horaria). Los débitos voluntarios incluyen
monto y comisión; depositar no reinicia el cupo. La cuota administrativa no consume
el límite de retiros y se cobra si hay saldo, aun con el cupo diario agotado.
El enunciado no precisa esas dos reglas; se dejan explícitas y se prueban.
En el código original sería posible agregar una subclase sin arreglar el CDT;
la estimación de tres archivos supone una integración correcta que distinga
cuota administrativa y retiro, no solo hacer pasar el ejemplo mínimo.

### R2: resultado registrado

Archivos de producción existentes modificados: 1.
Archivos de producción nuevos: 1.
Detalle verificable: `docs/cambios_req_2.json`. La suite completa pasó y
las cinco pruebas originales no cambiaron: `docs/pruebas_req_2.txt`.

### R3: resultado registrado

Archivos de producción existentes modificados: 1.
Archivos de producción nuevos: 2.
Detalle verificable: `docs/cambios_req_3.json`. La suite completa pasó y
las cinco pruebas originales no cambiaron: `docs/pruebas_req_3.txt`.

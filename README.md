# Laboratorio L2: SOLID - Banco Andino

Ingeniería de Software II · Universidad Nacional de Colombia, sede Bogotá · 2026.

**Único integrante:** Ronald Arturo Chávez.

## Estado y acceso rápido

La rama `main` incluye R1-R5 y **23 pruebas que pasan**. R6 está preparado
como demostración independiente en `demo-r6`. Faltan la revisión cruzada real
y la publicación en GitHub para cerrar la entrega.

- [Guía de ejecución, GitHub y entrega](docs/GUIA_ENTREGA.md).
- [Comparación visual UML](docs/uml_comparacion.html).
- [Resultados de pruebas finales](docs/pruebas_finales.txt).
- [Verificación reproducible de los controles](docs/verificacion_historial.txt).

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

### R4: resultado registrado

Archivos de producción existentes modificados: 1.
Archivos de producción nuevos: 2.
Detalle verificable: `docs/cambios_req_4.json`. La suite completa pasó y
las cinco pruebas originales no cambiaron: `docs/pruebas_req_4.txt`.

### R5: resultado registrado

Archivos de producción existentes modificados: 1.
Archivos de producción nuevos: 1.
Detalle verificable: `docs/cambios_req_5.json`. La suite completa pasó y
las cinco pruebas originales no cambiaron: `docs/pruebas_req_5.txt`.

### Tabla consolidada del bloque 4

| Req. | Original: existentes estimados | Refactorizado: existentes reales | Producción nueva | Pruebas nuevas | ¿Se rompió alguna? |
|---|---:|---:|---:|---:|---|
| R1 | 2 | 1 | 1 | 1 | No |
| R2 | 3 | 1 | 1 | 1 | No |
| R3 | 1 | 1 | 2 | 1 | No |
| R4 | 1 | 1 | 2 | 1 | No |
| R5 | 1 | 1 | 1 | 1 | No |

En los cinco requerimientos solo cambió `main.py` entre los módulos existentes.
Son **5 modificaciones acumuladas y 1 archivo distinto**. Se crearon 7 módulos
de producción y 5 módulos de pruebas. Se modificaron 0 pruebas del bloque 3.
La estimación original suma 8 intervenciones sobre archivos; es una estimación,
no una medición experimental del costo de implementar allí los cinco cambios.
No se interpreta esa diferencia como una reducción porcentual de horas de trabajo.

R3 conserva el log de conexión del SMS original: hay una línea diagnóstica
`[SMS] Conectando...` y **un solo mensaje al cliente** `[SMS] Para...` por operación.
El notificador compuesto recibe una llamada y la distribuye una vez por canal.
R4 observa las transacciones procesadas por el servicio (transferencias y, en
la demostración, pagos). La cuota administrativa y el retiro directo de la
cuenta no se registran como transacciones de ese servicio en el código base.
Si “cada transacción” incluyera también esos movimientos, habría que ampliar
el alcance e integrarlos al mismo flujo; no se afirma que ya esté implementado.

## Bloque 5. Revisión cruzada

**Pendiente de intercambio real.** La guía exige código ajeno, una rama en ese
repositorio y la lista recibida. No contamos con esos insumos y no inventamos
una revisión. La [plantilla](docs/revision_cruzada_pendiente.md) está lista.
La rama `demo-r6` implementa R6 sobre este diseño como demostración técnica;
no sustituye la actividad evaluada ni su commit `revision-cruzada`.

```bash
git switch demo-r6
python main.py
python -m unittest discover -v
git switch main
```

La rama demuestra reutilización del método `ejecutar` sin cambiar una línea del
servicio. Agrega dos archivos de producción y modifica solo `main.py`.
Paga $184.300 con comisión $1.500, deja la referencia en el comprobante y
utiliza PostgreSQL, SMS, push, auditoría y antifraude. Incluye cinco pruebas extra.

## Bloque 6. Cierre

### UML antes y después

Los diagramas completos editables están en
[UML original](docs/uml_antes.md) y [UML final](docs/uml_despues.md).
La comparación visual se abre en [comparación UML](docs/uml_comparacion.html).

| Antes | Después (vista principal) |
|---|---|
| ![UML original](docs/uml_antes.png) | ![UML final](docs/uml_despues.png) |

### Tabla comparativa


| Métrica | Antes | Después, rama main |
|---|---:|---:|
| Líneas físicas de `transferir` | 38 | 3 |
| Líneas del flujo `transferir` + `ejecutar` | 38 | 13 |
| Razones de cambio de `TransaccionService` | 7 | 1: orquestación |
| Clases concretas que construye el servicio (todas) | 2 | 1: operación `Transferencia` |
| Proveedores concretos que construye el servicio | 2 | 0 |
| Métodos vacíos o rechazo por “no aplica” | 4 | 0 |
| ¿Se prueba sin Oracle ni SMS por inyección pública? | No | Sí |
| Total de archivos de producción | 11 | 28 |
| Total de archivos versionados (incluye evidencia) | 13 | 87 |
| Archivos existentes modificados en bloque 4 | No aplica | 5 intervenciones; 1 archivo distinto |

El conteo de archivos de esta tabla usa el mismo criterio antes/después: módulos
Python de producción en la raíz. No incluye pruebas, evidencias, Git ni diagramas.
El inventario de todos los archivos versionados se entrega en
`docs/inventario_versionado.txt`, separado por categoría, para que “total” no
oculte archivos adicionales. Las interfaces están agrupadas por afinidad;
no se creó un archivo por cada método.

La caída de 38 a 3 líneas no significa que desapareció toda la lógica:
`ejecutar` contiene 10 líneas y llama a colaboradores. Por eso se muestra
también la suma. Se conserva la operación concreta `Transferencia` como entrada
cómoda del caso de uso; extraer una fábrica solo para llegar a cero clases
concretas añadiría una abstracción sin una necesidad observada.

### a) ¿Tener más archivos es un problema?

No por sí solo. Ahora podemos localizar la comisión, la salida del comprobante
y los proveedores sin editar el movimiento del dinero. Sí sería un problema
si separar archivos obligara a saltar entre muchas capas que no tienen una
responsabilidad propia. Por eso se agrupan protocolos relacionados. Tres
capacidades de productos (`DevengaIntereses`, `RecibeCuotas`, `PermiteAvances`)
aún no tienen un consumidor de producción; sirven para explicitar la segregación,
pero en un sistema pequeño se podría esperar a necesitarlas antes de mantenerlas.

### b) ¿Dónde se notó más la diferencia?

En R5 fue fácil de comprobar: agregamos `PostgresRepositorio`, cambiamos el
armado en `main.py` y las cinco pruebas originales pasaron sin modificar sus
archivos. Oracle sigue disponible. R3 y R4 también lo muestran: la notificación
múltiple y el observador múltiple agregaron canales sin editar el servicio.
No decimos que R5 haya ahorrado más archivos que los demás: el conteo real fue
un archivo existente en cada requerimiento.

### c) ¿Qué no aguantó bien el diseño?

R1-R5 pasaron sus criterios y las pruebas. R2 necesitó una decisión que el texto
no precisaba: distinguir retiros voluntarios de la cuota administrativa y definir
si la comisión consume el límite diario. La separación de capacidades permitió
hacerlo en una subclase, pero esas reglas deben acordarse con negocio.

El diseño aún no garantiza atomicidad si un proveedor externo falla después de
mover el dinero. Para un backend real se necesita una transacción de base de datos
que registre movimiento y evento, reintentos con idempotencia y una estrategia
para entregar notificaciones. Tampoco hay concurrencia protegida ni acumulador
general del tope de $5 millones: el original lo verifica por operación aunque
su mensaje diga “diario”. Se conservaron `float` y las validaciones heredadas;
para producción se usaría dinero decimal y se rechazarían `NaN`/infinito en los
límites del dominio. Estas mejoras quedan fuera de la refactorización conservadora.

### d) ¿Qué dijo la otra pareja? ¿Estamos de acuerdo?

Pendiente. No se recibió el repositorio ajeno ni comentarios de otra pareja.
Esta respuesta debe completarse con la lista real; la demostración propia R6
no permite atribuirles una opinión.

### e) ¿Cómo justificar dos semanas de refactorización?

Mostraríamos las evidencias: cinco salidas de control conservaron el comportamiento;
los cinco requerimientos tocaron un solo archivo de producción existente,
`main.py`, en cinco commits; las pruebas iniciales se conservaron sin cambios.
Eso indica menor acoplamiento y facilita revisar una modificación sin tocar el
núcleo de transferencias. No basta para prometer un ahorro fijo de tiempo ni
justificar automáticamente dos semanas: propondríamos un piloto con métricas
de tiempo de cambio, incidentes y retrabajo del sistema real.

## Fuentes y alcance

Enunciados suministrados: `Laboratorio_SOLID.pdf` (bloques 0-6 y rúbrica) y
`Requerimientos_SOLID.pdf` (R1-R6). No se utilizaron reglas bancarias externas.
Oracle, PostgreSQL, SMS, push y antifraude son simulaciones de consola.
No hay credenciales, servidores de producción ni envío real de mensajes.

## Entrega y pasos pendientes

- Rama `main`: bloques 0-4 y cierre documental, código y pruebas.
- Rama `demo-r6`: pago de servicios probado sobre el repositorio propio.
- Único integrante: Ronald Arturo Chávez.
- Revisión cruzada y respuesta 6(d): pendientes de la otra pareja.
- Publicación en GitHub: pendiente de la URL o cuenta de destino.

No se presenta el paquete como entrega completamente cerrada mientras falte
la revisión cruzada. El historial se produjo al ejecutar las etapas; no se
simularon commits vacíos ni se cambiaron sus fechas.

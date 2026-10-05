# R6 - Demostración sobre el repositorio propio

Esta rama **no acredita una revisión cruzada**. Falta recibir el repositorio
asignado por el profesor y su lista de revisión. No se atribuyen comentarios a
una pareja que todavía no ha participado.

Se agregaron `PagoServicio` y `ComisionServicios`; solo se modificó `main.py`
entre los archivos de producción existentes. `TransaccionService` permanece
idéntico al control D. `ejecutar` reutiliza la validación, selección de comisión,
persistencia, comprobante, notificación y observadores. Solo el movimiento
específico de un pago se implementa en la nueva operación.

La prueba de aceptación verifica que $184.300 + $1.500 = $185.800, registra la
referencia como destino y pasa por todos los canales. Se prueban también monto,
saldo insuficiente, CDT y límite infantil. La prueba con CDT es intencionalmente
un uso inválido de tipos para comprobar el rechazo dinámico.

```bash
git switch demo-r6
python main.py
python -m unittest discover -v
git switch main
```

Para realizar la revisión válida se debe trabajar en una rama del repositorio
de la otra pareja, hacer su implementación y registrar allí `revision-cruzada`.

Tras integrar las pruebas de dominio del cierre: 28 pruebas pasando en esta rama.

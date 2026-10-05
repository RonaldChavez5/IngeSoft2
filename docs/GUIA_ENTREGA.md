# Cómo abrir y entregar el proyecto

## Ejecución (Windows, macOS o Linux)

Se requiere Python 3.12+ y Git. No hay `pip install` para ejecutar el laboratorio.
Abra la terminal en `banco-andino`:

```bash
python main.py
python -m unittest discover -v
python scripts/verificar_historial.py
git log --oneline --all --graph
```

En Windows, si `python` no está disponible, use `py -3.12` en su lugar.
La verificación del historial usa etiquetas que apuntan a los commits de cada etapa.

## Historial y copia de respaldo

La carpeta contiene su directorio `.git`: conserve ese directorio para no perder
los commits. El archivo `banco-andino.bundle` permite recuperar el repositorio
si un programa de compresión omite archivos ocultos:

```bash
git clone banco-andino.bundle banco-andino-recuperado
cd banco-andino-recuperado
git switch -c demo-r6 origin/demo-r6
```

Si ya extrajo la carpeta del repositorio, no hace falta clonar el bundle.
No use “subir archivos” en GitHub como sustituto de enviar el historial.

## Publicar en un repositorio nuevo de GitHub

Cree el repositorio vacío (sin README inicial), copie su URL y ejecute:

```bash
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
git push origin demo-r6
git push origin --tags
```

`URL_DEL_REPOSITORIO` es el único valor que debe sustituirse. No incluya una
contraseña o token dentro de un archivo. La autenticación se realiza en Git/GitHub.
Si el repositorio ya existe y tiene cambios, primero se debe revisar su historia;
no use `--force` para resolverlo.

## Para cerrar la entrega académica

1. Agregar al README los nombres completos, códigos y grupo que exija el profesor.
2. Obtener el repositorio asignado de la otra pareja y realizar allí R6, en una rama.
3. Registrar el commit `revision-cruzada` en ese repositorio.
4. Recibir la lista de revisión de la otra pareja y guardarla en este repositorio.
5. Completar el cierre 6(d) con esa retroalimentación y actualizar el cierre.
6. Entregar al profesor la URL del repositorio con acceso de lectura.

El commit de cierre disponible documenta expresamente el estado pendiente de la
revisión. La rama `demo-r6` es preparación y no acredita un intercambio que no ocurrió.

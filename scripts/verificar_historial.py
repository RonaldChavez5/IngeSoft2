"""Reproduce salidas de los controles en copias temporales, sin tocar el checkout."""
from pathlib import Path
import io
import os
import re
import subprocess
import sys
import tarfile
import tempfile

RAIZ = Path(__file__).resolve().parents[1]


def normalizar(s):
    return re.sub(r"\[AUDITORIA\] \S+", "[AUDITORIA] FECHA", s)


def salida(ref):
    archivo = subprocess.check_output(["git", "archive", ref], cwd=RAIZ)
    with tempfile.TemporaryDirectory() as temporal:
        with tarfile.open(fileobj=io.BytesIO(archivo)) as tar:
            tar.extractall(temporal, filter="data")
        return subprocess.check_output([sys.executable, "main.py"], cwd=temporal,
                                       text=True, encoding="utf-8",
                                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})


original = normalizar(salida("bloque-0-codigo-base"))
for ref in ["control-S", "control-O", "control-L", "control-I", "control-D"]:
    assert normalizar(salida(ref)) == original, f"Salida distinta: {ref}"
    print(f"PASS {ref}: salida conservada")
prueba_original = subprocess.check_output(
    ["git", "show", "bloque-3-pruebas:tests/test_transferencias.py"], cwd=RAIZ)
assert prueba_original == (RAIZ / "tests/test_transferencias.py").read_bytes()
print("PASS: cinco pruebas del bloque 3 intactas")

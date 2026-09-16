# Calculadora de Algebra Lineal

Aplicacion de escritorio para practicar operaciones con matrices, vectores, sistemas de ecuaciones, limites y sistemas numericos.

## Requisitos

- Windows 10 u 11
- Python 3.13 de 64 bits
- Git

La aplicacion utiliza `ctypes` para registrar temporalmente las fuentes incluidas en `core/assets/fonts`, por lo que esta version esta preparada principalmente para Windows.

## Instalacion para colaboradores

Desde PowerShell, clona el repositorio y entra en la carpeta del proyecto:

```powershell
git clone URL_DEL_REPOSITORIO
cd Algebra-Lineal
```

Crea el entorno virtual con Python 3.13:

```powershell
py -3.13 -m venv .venv
```

Activa el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell impide la activacion, puedes continuar sin activarlo usando directamente el ejecutable del entorno.

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Ejecuta la aplicacion:

```powershell
python main.py
```

Sin activar el entorno virtual:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Configuracion en VS Code

Selecciona como interprete de Python:

```text
.venv\\Scripts\\python.exe
```

Despues ejecuta `main.py`.

## Dependencias

Las versiones utilizadas estan fijadas en `requirements.txt` para que todos los colaboradores instalen el mismo conjunto de paquetes.

## Recursos incluidos

- `core/assets/Bordes.png`: fondo decorativo.
- `core/assets/fonts/`: fuentes utilizadas por la interfaz.

Las fuentes deben conservarse junto con el proyecto. Antes de redistribuir la aplicacion, verifica que sus licencias permitan incluirlas.

## Estado del entorno

No se debe subir `.venv`, `__pycache__` ni archivos `.pyc`. Cada colaborador debe crear su propio entorno virtual local.

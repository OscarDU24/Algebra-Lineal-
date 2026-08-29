# Programa 1 — Resolución de Sistemas de Ecuaciones Lineales

Programa interactivo en **Python puro** (sin NumPy, SciPy ni funciones de
álgebra lineal de `math`) que resuelve sistemas de ecuaciones lineales
`Ax = b`, mostrando cada paso del proceso y clasificando el sistema según
el número de soluciones. El programa muestra un **menú** para que el
usuario elija con qué método desea resolver el sistema:

1. **Gauss-Jordan** — forma escalonada reducida por filas (RREF).
2. **Gauss** — forma escalonada por filas (REF) + sustitución hacia atrás.
3. **Eliminación** — método clásico de suma y resta de ecuaciones.

---

## 1. Estructura del proyecto

```
Programa1_Grupox/
├── main.py                          # Punto de entrada: menú y flujo del programa
└── sislineal/                        # Paquete con toda la lógica del algoritmo
    ├── __init__.py                   # Expone la API pública del paquete
    ├── entrada.py                    # Lectura de datos y menú de selección de método
    ├── visualizacion.py              # Impresión de la matriz aumentada
    ├── eliminacion_gauss_jordan.py   # Método 1: Gauss-Jordan (RREF)
    ├── eliminacion_gauss.py          # Método 2: Gauss (REF)
    ├── eliminacion_por_eliminacion.py# Método 3: Eliminación (suma y resta)
    ├── clasificacion.py              # Clasifica el sistema (determinado / indeterminado / inconsistente)
    ├── solucion.py                   # Obtiene el valor de las variables (según el método)
    └── verificacion.py               # Comprueba la solución en el sistema original
```

`main.py` no contiene lógica matemática: importa las funciones del
paquete `sislineal`, muestra el menú de método y coordina el flujo
completo del programa.

---

## 2. Requisitos y ejecución

- Python 3.8 o superior. No requiere instalar ninguna librería externa.

Para ejecutar el programa, ubicarse en la carpeta `Programa1_Grupox/` y correr:

```bash
python main.py
```

El programa solicitará por consola:
1. El número de ecuaciones `m`.
2. El número de variables `n`.
3. Los coeficientes de cada ecuación y su término independiente.
4. El **método** con el que se desea resolver el sistema (menú 1/2/3).

> **Nota:** el sistema **no necesita ser cuadrado**. El programa admite
> `m = n`, `m > n` (sobredeterminado) o `m < n` (subdeterminado), en
> cualquiera de los tres métodos.

---

## 3. Los tres métodos disponibles

### 3.1 Gauss-Jordan (`eliminacion_gauss_jordan.py`)
Por cada columna: busca el mejor pivote (pivoteo parcial), **normaliza**
la fila pivote para que el pivote quede en `1`, y **elimina la variable
en todas las demás filas** (arriba y abajo). El resultado es la forma
escalonada reducida (RREF); la solución se lee directamente de la
última columna, sin sustitución hacia atrás.

### 3.2 Gauss (`eliminacion_gauss.py`)
Por cada columna: busca el mejor pivote (pivoteo parcial) y elimina la
variable **solo en las filas de abajo**, sin normalizar el pivote ni
tocar las filas de arriba. El resultado es la forma escalonada (REF);
las variables se obtienen luego mediante **sustitución hacia atrás**.

### 3.3 Eliminación — suma y resta (`eliminacion_por_eliminacion.py`)
El método clásico enseñado "a mano": para eliminar una variable de una
ecuación, se multiplica la ecuación pivote por el factor necesario y el
resultado se suma o resta a la otra ecuación. No usa pivoteo parcial
(usa las ecuaciones en el orden en que fueron ingresadas, reordenando
solo si el pivote actual es cero). El resultado también es una forma
escalonada (REF), por lo que igualmente requiere sustitución hacia atrás.

En los tres casos, cada paso realizado se imprime en pantalla para que
se pueda seguir el procedimiento completo hasta llegar al resultado.

---

## 4. Clasificación del sistema

Con la matriz ya escalonada (RREF o REF, según el método elegido),
`sislineal/clasificacion.py` evalúa:

| Condición                                                                 | Clasificación                                    |
|----------------------------------------------------------------------------|---------------------------------------------------|
| Existe una fila `0 0 ... 0 | k` con `k ≠ 0`                                | **Sistema Inconsistente** — Sin Solución           |
| No hay fila inconsistente y el número de pivotes (rango de A) es igual a `n` | **Sistema Consistente Determinado** — Solución Única |
| No hay fila inconsistente y el número de pivotes es menor que `n`          | **Sistema Consistente Indeterminado** — Infinitas Soluciones |

Esta clasificación funciona igual sin importar el método elegido.

---

## 5. Solución y verificación

- **Gauss-Jordan:** la solución se lee directamente de la RREF
  (`extraer_solucion_rref`).
- **Gauss / Eliminación:** la solución se obtiene mediante sustitución
  hacia atrás sobre la REF (`sustitucion_hacia_atras`).
- **Sistema indeterminado:** se informan las variables dependientes
  (columnas con pivote); las demás son variables libres.
- **Sistema inconsistente:** no se calculan valores numéricos.
- **Verificación:** cuando el sistema es determinado, los valores
  obtenidos se sustituyen en el sistema **original** (antes de la
  eliminación) para comprobar que cada ecuación se satisface
  (`sislineal/verificacion.py`).

---

## 6. Casos de prueba sugeridos (para las capturas de pantalla)

| Caso | m | n | Ejemplo de sistema                          | Resultado esperado           |
|------|---|---|----------------------------------------------|-------------------------------|
| 1    | 2 | 2 | `x1 + x2 = 5` <br> `2x1 - x2 = 1`             | Solución única: x1=2, x2=3    |
| 2    | 2 | 2 | `x1 + x2 = 2` <br> `2x1 + 2x2 = 4`            | Infinitas soluciones          |
| 3    | 2 | 2 | `x1 + x2 = 2` <br> `2x1 + 2x2 = 5`            | Sin solución (inconsistente)  |

Se recomienda repetir al menos un caso con cada uno de los tres métodos
del menú, para evidenciar que las tres opciones funcionan. También se
puede probar con sistemas no cuadrados (por ejemplo `m=3, n=2` o
`m=1, n=2`) para evidenciar que el programa no exige matriz cuadrada.

---

## 7. Portada / datos del grupo

Antes de entregar, completar en `main.py` los marcadores `[...]` con el
nombre de la asignatura, el docente, los integrantes, la carrera y el
número de grupo.

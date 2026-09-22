# Estudio inicial de UI/UX de HeyAlgb

Fecha: 2026-09-21

## Alcance

Este estudio evalua la experiencia actual de HeyAlgb a partir del codigo de `core/ui`,
los flujos de navegacion y los recursos visuales del Dashboard. Se contrasta con
principios de usabilidad y accesibilidad de fuentes publicas, y con patrones visibles
en calculadoras educativas como Desmos y GeoGebra.

No se afirma una comparacion directa con las aplicaciones de companeros porque no se
han recibido sus ejecutables, capturas ni flujos de uso. Para esa comparacion se deja
una matriz comun al final del documento.

## Diagnostico ejecutivo

HeyAlgb tiene una identidad visual reconocible y una intencion pedagogica valiosa:
las calculadoras muestran formulas, pasos de eliminacion y resultados. El problema
principal no es la falta de funciones, sino la discontinuidad entre el Dashboard y
las calculadoras internas.

El Dashboard se percibe como un producto disenado; las vistas internas se perciben
como modulos tecnicos reunidos en una misma aplicacion. Hay diferencias de toolkit,
dimensiones, tipografias, colores, densidad, nomenclatura y forma de presentar errores.
Eso aumenta la carga cognitiva: el estudiante debe reaprender como funciona cada
pantalla antes de poder concentrarse en el problema matematico.

Prioridad general: consolidar un sistema de interfaz antes de agregar muchas mas
operaciones.

## Lo que ya funciona

- El Dashboard organiza el producto por areas matematicas y ahora usa iconos propios.
- Las transiciones entre ventanas ocultan el Dashboard y permiten volver a el al cerrar
  una calculadora.
- Los modulos muestran procedimientos algebraicos, no solamente respuestas finales.
- La calculadora de vectores permite seleccionar formato decimal o fraccionario.
- La interfaz ofrece validaciones de dimensiones y mensajes de entrada en varios flujos.
- La separacion entre logica matematica y vistas facilita mejorar la experiencia sin
  reescribir los algoritmos.
- La paleta blanco, negro y rojo da una base de marca clara en la pantalla principal.

## Hallazgos principales

### P0 - Continuidad visual insuficiente

El Dashboard usa Tkinter clasico, iconografia propia y una composicion fija de 980x780.
Las calculadoras usan principalmente CustomTkinter, pero cada una define sus propias
geometrias, titulos, fuentes y controles. Por ejemplo, las vistas usan 900x700,
980x780, 980x780, 1100x800 y 880x720.

Consecuencia: el usuario no siente que cambio de una seccion a otra del mismo producto,
sino que abrio aplicaciones distintas.

Recomendacion:

- Definir un tema compartido: colores, tipografias, tamanos, espaciado y estilos de
  botones, entradas, selectores y resultados.
- Crear un contenedor comun para las vistas: encabezado, boton Volver, area de entrada,
  barra de acciones y area de procedimiento.
- Mantener una geometria base y permitir solo variaciones justificadas por el modulo.

### P0 - Flujo de salida poco visible

El regreso al Dashboard depende principalmente de la X de la ventana. La vista guarda
la referencia al padre y usa `deiconify()`, pero no ofrece un boton visible de Volver.
Esto es funcional, aunque poco descubrible y menos comodo para estudiantes que no
piensan en cerrar una ventana para navegar.

Recomendacion:

- Añadir un boton `Volver al menu` en la cabecera de cada calculadora.
- Mantener la X como segunda salida.
- Actualizar el estado del Dashboard con el modulo activo y la operacion seleccionada.

### P0 - Pantallas de entrada demasiado generales

En la vista matricial se solicitan simultaneamente filas, columnas y cantidad de
vectores aunque la operacion elegida pueda ser una transpuesta, una matriz por escalar
o una ecuacion `Ax = b`. Esto hace que el usuario complete datos que no necesita.

Recomendacion:

- Elegir primero la tarea y despues mostrar solo los campos requeridos.
- Para `Ax = b`, mostrar A y b.
- Para transpuesta o `cA`, mostrar A y, si corresponde, c.
- Para Leontief, mostrar los sectores y la tabla economica.
- Para flujo de red, mostrar nodos, ramas y balances.

### P1 - Operaciones ocultas dentro de menus largos

Los OptionMenu concentran muchas tareas heterogeneas. En vectores, por ejemplo, se
mezclan operaciones basicas, geometria y analisis en una sola lista. En matriciales se
mezclan productos, propiedades, transpuesta, `Ax = b`, Leontief y flujo de red.

Recomendacion:

- Agrupar por pestañas o botones segmentados: `Basicas`, `Geometria`, `Sistemas`,
  `Aplicaciones`.
- Mantener visible el nombre de la operacion activa y su formula.
- Usar menus solo cuando haya muchas opciones dentro de una misma familia.

### P1 - Falta de estado y previsualizacion del resultado

La aplicacion informa resultados despues de presionar Calcular, pero no siempre deja
claro si la entrada esta completa, que datos se usaran o que paso se esta ejecutando.
La tabla de intercambio y flujo de red son especialmente sensibles a convenciones de
signos y dimensiones.

Recomendacion:

- Deshabilitar Calcular hasta que exista una entrada valida, o indicar que campos
  faltan antes de ejecutar.
- Mostrar una linea de estado: `Listo`, `Calculando`, `Resultado`, `Error de entrada`.
- Presentar una vista previa breve del modelo antes de resolver, por ejemplo
  `(I - A)X = D` o `salidas - entradas = balance`.

### P1 - Errores utiles, pero poco localizados

Varios modulos escriben el error en un Textbox general. El mensaje puede ser correcto,
pero el usuario debe buscar que campo genero el problema.

Recomendacion:

- Marcar el campo concreto con borde rojo y texto breve debajo.
- Mantener el detalle completo en el area de procedimiento.
- Explicar como corregir: `La componente u2 esta vacia`, `Ingresa un numero como 1/3`
  o `b debe tener una componente por cada fila de A`.

### P1 - Accesibilidad y teclado no tratados como requisito

Los controles tienen texto visible, pero no se observa una estrategia explicita para
orden de tabulacion, foco visible, nombres accesibles, escalado de texto o alto
contraste. Los iconos del Dashboard son controles graficos con texto vacio, por lo que
su significado depende de la etiqueta inferior.

Recomendacion:

- Garantizar que cada icono tenga un nombre accesible y un equivalente textual.
- Probar toda la aplicacion usando solo Tab, Shift+Tab, Enter y Escape.
- No comunicar estados solo con rojo o verde; combinar color con texto, icono o forma.
- Evitar que la composicion fija de 980x780 corte controles con escalado de Windows.
- Hacer visible el foco del control activo.

### P2 - Jerarquia visual irregular

Algunas vistas usan titulos grandes y otras controles compactos; algunas tienen texto
explicativo y otras empiezan directamente con campos. Los resultados tambien alternan
entre tablas, vectores verticales y texto monoespaciado sin un marco comun.

Recomendacion:

- Mantener la jerarquia `Titulo -> Contexto -> Entrada -> Accion -> Procedimiento -> Resultado`.
- Reservar el rojo para acciones, errores y estados importantes.
- Usar negro para texto principal y grises solo para informacion secundaria que siga
  siendo legible.
- Separar visualmente resultado final y procedimiento detallado.

## Comparacion con calculadoras educativas publicadas

### Desmos

Desmos presenta una superficie de trabajo centrada en la tarea: expresiones, grafica,
tabla y controles aparecen como partes de un mismo flujo. La interfaz reduce el salto
entre entrada y resultado. HeyAlgb tiene una ventaja didactica en sus explicaciones
algebraicas, pero necesita una relacion mas directa entre el campo que se modifica y
el resultado que cambia.

Patron aprovechable: mantener una zona de trabajo persistente y hacer que el resultado
sea una consecuencia visible de la entrada, no solo una salida posterior en consola.

### GeoGebra

GeoGebra ofrece herramientas agrupadas, iconos reconocibles, historial de acciones,
controles de cerrar y deshacer, y una interfaz que mantiene una logica comun entre
vistas. HeyAlgb ya tiene iconos en el Dashboard, pero todavia no dispone de un sistema
comun de herramientas dentro de los modulos.

Patron aprovechable: agrupar operaciones por objetivo y dar al usuario control claro
para volver, limpiar, repetir o deshacer.

## Referencias de diseño

### Heuristicas de Nielsen

La auditoria utiliza las diez heuristicas de Nielsen Norman Group. Las mas relevantes
para HeyAlgb son:

- Visibilidad del estado del sistema: indicar si los datos estan listos, si se esta
  calculando y que resultado se obtuvo.
- Correspondencia con el mundo real: usar el lenguaje del curso y mostrar formulas
  junto a los controles.
- Control y libertad: ofrecer Volver, Limpiar y, cuando sea posible, deshacer.
- Consistencia y estandares: mantener los mismos controles y ubicaciones en todas las
  calculadoras.
- Prevencion de errores: validar dimensiones y campos antes de intentar resolver.
- Reconocimiento antes que memoria: mostrar formulas, unidades, convenciones de signo
  y ejemplos cerca de la entrada.
- Estetica minimalista: quitar campos que la operacion actual no usa.
- Ayuda y documentacion: ofrecer explicacion contextual, no solo un README externo.

Fuente: [Nielsen Norman Group - 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)

### Accesibilidad de Windows

Microsoft recomienda soporte de teclado, nombres accesibles para controles, texto
legible, compatibilidad con ampliacion y pruebas con tecnologias de asistencia. Esto
es especialmente importante en una aplicacion educativa, donde la lectura de formulas
y resultados es parte central de la tarea.

Fuente: [Microsoft Learn - Accessibility overview for Windows apps](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility)

### Contraste

W3C WCAG 2.2 recomienda una relacion minima de 4.5:1 para texto normal y 3:1 para
texto grande. La paleta blanco, negro y rojo puede funcionar, pero el rojo no debe ser
la unica señal y no conviene usar rojo sobre negro para texto pequeno.

Fuente: [W3C WCAG 2.2 - Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

### Calculadoras de referencia

- [Desmos Graphing Calculator](https://www.desmos.com/calculator)
- [GeoGebra Calculator Suite](https://www.geogebra.org/calculator)

Estas referencias se usan para observar patrones de flujo y organizacion, no para
copiar su apariencia ni su implementacion.

## Matriz de comparacion con companeros

Para comparar HeyAlgb con otras calculadoras, asignar de 0 a 2 por criterio:

| Criterio | 0 | 1 | 2 |
|---|---|---|---|
| Aprendizaje inicial | No se entiende que hacer | Requiere explicacion externa | Se entiende al primer intento |
| Consistencia | Cada pantalla funciona distinto | Hay patrones parciales | Hay un sistema comun |
| Entrada de datos | Confusa o redundante | Funciona con esfuerzo | Solo muestra lo necesario |
| Procedimiento | Solo muestra respuesta | Muestra algunos pasos | Explica el procedimiento completo |
| Errores | Error generico | Indica el problema | Indica problema y solucion |
| Navegacion | Solo depende de cerrar ventanas | Hay alguna salida visible | Volver, limpiar y repetir son claros |
| Teclado | No se puede completar con teclado | Solo algunos controles | Flujo completo con foco visible |
| Legibilidad | Texto pequeno o saturado | Aceptable | Jerarquia y contraste claros |
| Feedback | No confirma el estado | Informa al final | Informa durante toda la tarea |
| Robustez | Casos comunes fallan | Casos basicos funcionan | Casos limite estan explicados |

## Plan de mejora propuesto

### Fase 1 - Sistema comun

- Crear constantes de tema para colores, fuentes, espaciado y tamanos.
- Crear una cabecera comun con titulo, descripcion breve y boton Volver.
- Crear componentes reutilizables para acciones, entradas, selector de formato y visor.
- Unificar nombres: `Generar`, `Calcular`, `Limpiar`, `Volver`.

### Fase 2 - Flujo de tarea

- 
- Mostrar solo los campos que la operacion necesita.
- Introducir ejemplos iniciales no destructivos o placeholders utiles.
- Separar `Resultado` de `Procedimiento` y permitir copiar el resultado.

### Fase 3 - Accesibilidad y validacion

- Revisar orden de tabulacion y foco.
- Revisar contraste y escalado de Windows.
- Usar color mas texto para estados y errores.
- Probar operaciones con entradas vacias, fracciones, dimensiones invalidas y casos
  sin solucion.

### Fase 4 - Pruebas con usuarios

Realizar una prueba moderada con estudiantes que no hayan construido el modulo. Pedir
que completen estas tareas sin ayuda:

1. Abrir la calculadora de vectores y calcular una normalizacion.
2. Resolver `Ax = b` y localizar la solucion en el procedimiento.
3. Resolver una tabla de intercambio abierta.
4. Construir una red de tres nodos y explicar el signo de un flujo.
5. Recuperarse de una entrada invalida.
6. Volver al Dashboard y abrir otro modulo.

Medir tiempo, errores, abandonos, preguntas realizadas y confianza percibida de 1 a 5.
El criterio de exito inicial puede ser: al menos 80% de tareas completadas sin ayuda y
ningun error critico de interpretacion del resultado.

## Conclusion

HeyAlgb no necesita parecerse a Desmos o GeoGebra para competir en calidad. Su ventaja
puede ser otra: explicar el algebra paso a paso dentro de una herramienta sencilla.
Para que esa ventaja se perciba, la siguiente inversion debe estar en la coherencia
entre modulos, la reduccion de carga de entrada, la navegacion visible y la
accesibilidad. La interfaz debe hacer que el estudiante piense en el problema
matematico, no en como domesticar cada ventana.

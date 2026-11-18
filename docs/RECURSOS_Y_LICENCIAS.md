# Recursos incluidos y licencias

Fecha de revisión: 2026-11-18.

Este inventario se elaboró leyendo los **metadatos incrustados** en cada archivo de
`core/assets/`: la tabla `name` de las fuentes, las etiquetas ID3 del audio y los
bloques de texto de los PNG. También se revisó qué archivos usa el código.

No sustituye una revisión legal. Que un archivo esté en el repositorio no implica
que pueda redistribuirse.

## Resumen para la feria y el portafolio

| Estado | Recursos | Acción necesaria antes de distribuir |
|---|---|---|
| **No distribuible según sus metadatos** | `BackgroundMusic.mp3`, los 6 efectos de sonido, `HelveticaNowDisplay-Bold.ttf`, `Democratica Bold.ttf` | Sustituirlos por recursos propios o con una licencia que permita redistribuirlos |
| Licencia por confirmar | `UltraCondensedSansSerif.ttf`, avatares del equipo, fondos, iconos y `UAMICON.png` | Documentar el origen (autoría propia o licencia) |
| Libre con condiciones (SIL OFL 1.1) | Anton, Archivo Black, Alfa Slab One, Caprasimo, Playfair Display, League Spartan, Oswald, Tinos, Abril Fatface, Arsenal | Incluir el texto de la OFL junto con las fuentes; no venderlas por separado |

Una demostración local en la feria no es lo mismo que publicar un ejecutable o un
repositorio público. Antes de **cualquier distribución**, ya sea un ejecutable, un ZIP o un
enlace de portafolio, deben resolverse las filas «No distribuible» y «Por confirmar».

El repositorio ya se aloja en GitHub. Si es público, los archivos marcados como no
distribuibles ya están publicados en su historial. Quitarlos de la rama no los elimina
del historial; el equipo debe decidir cómo proceder.

## Audio (`core/assets/SoundEffects/`)

| Archivo | Uso en el código | Metadatos ID3 encontrados |
|---|---|---|
| `BackgroundMusic.mp3` | Música del lobby (`audio_manager.py`) | Título «Beneath the Mask -rain-», artista «Lyn», álbum «PERSONA5 ORIGINAL SOUNDTRACK», publicado el 2017-01-17 |
| `CalcularAct.mp3` | Efecto «calcular» | `system#172 (cancel)` |
| `ChoiceSelect.mp3` | Efecto «seleccionar» | `system#179 (cutin_select)` |
| `CursorSelect.mp3` | Efecto «cursor» | `system#177 (cursor)` |
| `ErrorDT.mp3` | Efecto «error» | `system#203 (ng)` |
| `InterfacesSwitch.mp3` | Efecto «interfaces» | `system#204 (ok)` |
| `LimpiarAct.mp3` | Efecto «limpiar» | `system#227 (camp_whoosh)` |

- La música es una pista de la banda sonora comercial de Persona 5.
- Los efectos tienen nombres de flujo internos (`system#…`, `stream_name`) propios de bancos de sonido extraídos de un juego.
- No hay ningún documento de licencia.
- El contexto del proyecto indica que la estética de Persona 5 es solo una referencia visual: no autoriza copiar sus recursos.

**Recomendación:** reemplazar los siete archivos por audio propio o con licencia CC0 o
CC BY, y anotar aquí su origen. La aplicación ya funciona en silencio si falta un
archivo (`AudioManager` lo omite), así que se pueden retirar sin romper la interfaz.

## Fuentes (`core/assets/fonts/`)

| Archivo | ¿Se usa? | Copyright o licencia incrustados |
|---|---|---|
| `HelveticaNowDisplay-Bold.ttf` | Sí: Dashboard e inicio | «Copyright © 2019 Monotype Imaging Inc. All rights reserved.» La licencia indica que es propiedad de Monotype. **Comercial.** |
| `Democratica Bold.ttf` | Sí: menú del Dashboard; `FUENTE_CONTROLES` en `tema.py` | «Copyright (C) 1993 Emigre Graphics, Designed by Miles Newlyn». Sin licencia incrustada. Emigre comercializa sus fuentes. **Comercial salvo prueba en contrario.** |
| `UltraCondensedSansSerif.ttf` | Sí: título del Dashboard; `FUENTE_TITULO` | «Copyright (c) Manfred Klein, 2004». Sin licencia incrustada. **Por confirmar** (sus fuentes suelen tener condiciones de uso propias). |
| `Anton-Regular.ttf` | Sí: inicio | SIL OFL 1.1 |
| `ArchivoBlack-Regular.ttf` | Sí: inicio | SIL OFL 1.1 |
| `AlfaSlabOne-Regular.ttf` | Sí: inicio | SIL OFL 1.1 (nombre reservado «Alfa Slab») |
| `Caprasimo-Regular.ttf` | Sí: inicio | SIL OFL 1.1 |
| `PlayfairDisplay-VariableFont_wght.ttf` | Sí: inicio | SIL OFL 1.1 (nombre reservado «Playfair Display») |
| `LeagueSpartan-VariableFont_wght.ttf` | Sí: inicio | SIL OFL 1.1 |
| `Oswald-VariableFont_wght.ttf` | Sí: inicio | SIL OFL 1.1 |
| `Tinos-Bold.ttf` | Sí: inicio | SIL OFL 1.1 |
| `AbrilFatface-Regular.ttf` | Sí: inicio | SIL OFL 1.1 (nombres reservados «Abril», «Abril Fatface») |
| `Arsenal-Bold.ttf` | **No se usa** | SIL OFL 1.1 |

- Las fuentes OFL pueden redistribuirse con la aplicación, siempre que se incluya
  el texto de la licencia (por ejemplo, `core/assets/fonts/OFL.txt`) y no se vendan
  por separado. Ese archivo **aún no existe** en el repositorio.
- Hay sustitutos libres de estilo cercano: Anton u Oswald (ya incluidas) para títulos
  condensados, y Archivo Black o League Spartan (ya incluidas) para Helvetica Now y
  Democratica.

## Imágenes (`core/assets/`)

Ningún PNG ni ICO contiene metadatos de autoría o licencia.

| Archivo | Uso | Observación |
|---|---|---|
| `FondoMAIN.png` | Fondo del inicio | Origen no documentado |
| `BordesFinales.png` | Fondo del Dashboard | Origen no documentado |
| `Bordes.png` | **No se usa** | — |
| `HeyAlgbLogoBlanco.png`, `HeyAlgbICON.ico` | Logo e icono de la ventana | Logo del proyecto; confirmar autoría |
| `HeyAlgbICON.png` | **No se usa** | — |
| `*ICON.png`, `*CON.png` (8 iconos de módulos) | Tarjetas del Dashboard | Origen no documentado |
| `Liang_Amamiya.png`, `Oscar_Sakamoto.png`, `Diego_Kitagawa.png`, `Charly_Sakura.png` | Créditos del inicio | Los nombres usan apellidos de personajes de Persona 5; confirmar que son ilustraciones propias y no derivadas de arte oficial |
| `UAMICON.png` | Créditos del inicio | Logotipo institucional; su uso puede requerir permiso de la universidad |

## Dependencias de Python

Todas se instalan desde PyPI y no se incluyen en el repositorio.

| Paquete (versión instalada) | Licencia declarada en sus metadatos (`METADATA`) |
|---|---|
| customtkinter 6.0.0 | `License: Creative Commons Zero v1.0 Universal`; clasificador MIT |
| Pillow 12.3.0 | `MIT-CMU` |
| prettytable 3.18.0 | `BSD-3-Clause` |
| pygame 2.6.1 | `LGPL` |
| numpy 2.5.4 | `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` |
| scipy 1.18.1 | Clasificador BSD (hoy no se importa en el código) |
| matplotlib 3.11.2 | Licencia propia de matplotlib; clasificador PSF |

Si se crea un ejecutable con PyInstaller, se deben incluir los avisos de licencia de
estas dependencias. pygame usa LGPL, lo que exige permitir que se sustituya la biblioteca.

## Cómo se obtuvo este inventario

Se usó `fontTools` (instalado como dependencia de matplotlib) para leer los
identificadores 0, 1, 8, 9, 13 y 14 de la tabla `name`. Las etiquetas ID3v2 se
leyeron con un lector mínimo, y los bloques de texto de los PNG con Pillow. El uso
de cada archivo se comprobó buscando su nombre en el código.

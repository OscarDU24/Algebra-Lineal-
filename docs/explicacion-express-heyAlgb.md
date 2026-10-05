# HeyAlgb: explicación express

## Presentación oral (1-2 minutos)

> HeyAlgb es una aplicación de escritorio educativa para practicar Álgebra Lineal.
> Al iniciar, aparece una portada con dos opciones: **Iniciar**, que abre el selector
> de calculadoras, y **Ayuda**, que resume para qué sirve cada módulo. Desde el
> selector se puede abrir una calculadora y, al cerrarla, se vuelve al mismo menú.
>
> La aplicación conserva Tkinter como ventana principal y usa CustomTkinter para las
> vistas internas. La portada y el Dashboard pueden redimensionarse; el Dashboard
> recalcula la disposición de sus tarjetas e iconos según el tamaño disponible.
>
> También incorporamos audio opcional. La música se reproduce en la portada y el
> selector, se detiene al entrar a una calculadora y comienza de nuevo al regresar.
> Un interruptor permite apagarla. Los efectos corresponden al hover, acciones,
> limpieza y errores. Si pygame o el dispositivo de audio no están disponibles, la
> aplicación sigue funcionando sin sonido.
>
> La ayuda explica brevemente los módulos. El logo, las capturas de pantalla y los
> nombres reales del equipo siguen siendo placeholders porque todavía faltan esos
> recursos definitivos.

## Cómo está organizado

- `main.py` crea la ventana raíz, instancia `AudioManager` y muestra `VistaInicio`.
- `core/ui/vista_inicio.py` contiene la portada, el control de música y la ventana de
  Ayuda.
- `core/ui/dashboard.py` contiene el selector de módulos y gestiona la transición a
  las calculadoras.
- `core/ui/audio_manager.py` centraliza pygame, la música, los efectos y su manejo
  tolerante a errores.
- `core/assets/SoundEffects/` contiene los cinco MP3 utilizados por la interfaz.
- `requirements.txt` fija pygame junto con las dependencias que ya usaba el proyecto.

## Decisiones técnicas

### Una sola ventana raíz

No se crean ventanas raíz distintas para la portada y el Dashboard. La portada se
retira y el Dashboard se construye dentro de la misma raíz. Las calculadoras siguen
siendo ventanas secundarias. Esto mantiene la navegación existente y evita duplicar
el ciclo de vida de Tkinter.

### Selector adaptable

El Dashboard usa un Canvas para el fondo y para ubicar las tarjetas. Al cambiar el
tamaño se recalculan sus posiciones y dimensiones, y se redimensionan fondo e iconos.
La adaptación se aplica al lobby; cada calculadora conserva por ahora su propio
layout y geometría.

### Audio separado de la interfaz

`AudioManager` carga los MP3 una vez y expone operaciones sencillas para iniciar o
parar la música y reproducir efectos. Las vistas no inicializan pygame por separado.
Si el mixer falla, el error se informa en la terminal y las vistas continúan sin
sonido.

El audio compartido identifica clicks y controles interactivos. Las calculadoras
invocan el efecto de error desde sus visores al mostrar un mensaje de validación. El
hover tiene una pequeña limitación de frecuencia para que no se repita continuamente
al mover el puntero dentro del mismo control.

## Recorrido para una demostración

1. Ejecutar `main.py` y mostrar la portada HeyAlgb.
2. Apagar y volver a encender **Música de fondo**.
3. Abrir **Ayuda** y recorrer la descripción y los módulos.
4. Pulsar **Iniciar** y cambiar el tamaño de la ventana para mostrar cómo se adapta el
   Dashboard.
5. Pasar el puntero por una tarjeta y abrir una calculadora: se escucha el efecto y la
   música se detiene.
6. Cerrar la calculadora: reaparece el Dashboard y la música comienza desde el inicio.
7. Para demostrar el efecto de error, introducir datos inválidos en una calculadora.

## Recursos y límites actuales

Los MP3 de `core/assets/SoundEffects` están integrados. En cambio, el logo oficial no
se encontró en los assets al preparar esta versión; por eso se muestra un recuadro
provisional. Ayuda contiene espacios destinados a las capturas de los módulos y los
nombres temporales **Integrante 1-4** deben reemplazarse cuando el equipo confirme la
información.

El escalado dinámico se ha aplicado al Dashboard. No significa todavía que todas las
ventanas internas sean completamente adaptables. La música y los efectos dependen de
pygame y del soporte de audio del equipo, pero su ausencia no debe impedir el uso de
las calculadoras.

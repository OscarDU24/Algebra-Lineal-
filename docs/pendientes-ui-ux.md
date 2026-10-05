# Pendientes de UI/UX de HeyAlgb

Esta lista conserva propuestas para decidirlas durante una sesion posterior. No son
compromisos de implementacion de la fase actual.

## Implementado recientemente

- [x] Crear una portada HeyAlgb con las acciones **Iniciar** y **Ayuda**.
- [x] Añadir en Ayuda una descripción breve de la aplicación y de sus seis módulos.
- [x] Hacer redimensionable la ventana principal y adaptar tarjetas, iconos y fondo
      del Dashboard al espacio disponible.
- [x] Añadir el control de música de lobby y detener/reiniciar la pista al entrar y
      salir de una calculadora.
- [x] Conectar los efectos de hover, acciones, limpieza y errores con los MP3 de
      `core/assets/SoundEffects`.

## Pendientes de esta implementación

- [ ] Sustituir el recuadro provisional por el logo oficial de la universidad.
- [ ] Reemplazar los cuatro nombres provisionales por los integrantes confirmados.
- [ ] Añadir capturas reales de las calculadoras en la sección Ayuda.
- [ ] Revisar el escalado y la accesibilidad por teclado en las ventanas internas;
      el Dashboard ya adapta su composición, pero las calculadoras conservan tamaños
      y layouts propios.
- [ ] Probar música y efectos con usuarios y ajustar volumen, frecuencia del hover y
      preferencias de audio según sus comentarios.

- [ ] Crear un sistema visual compartido para todas las vistas internas.
- [ ] Unificar dimensiones, espaciado, fuentes y componentes de CustomTkinter.
- [ ] Añadir un boton visible de regreso al Dashboard en cada calculadora.
- [ ] Rediseñar cada calculadora para mostrar solo los campos que requiere la operacion.
- [ ] Sustituir menus largos por grupos de operaciones cuando una prueba con usuarios
      demuestre que mejora la localizacion.
- [ ] Añadir estados de proceso como Listo, Calculando, Resultado y Error.
- [ ] Localizar errores junto al campo que los provoca.
- [ ] Revisar orden de tabulación, foco visible y nombres accesibles de controles.
- [ ] Separar visualmente el resultado final del procedimiento detallado.
- [ ] Permitir copiar resultados y procedimientos.
- [ ] Realizar pruebas moderadas con estudiantes y profesores antes de rediseñar
      controles adicionales.

## Decisiones aplicadas en esta fase

- [x] Aplicar la paleta propuesta a las calculadoras principales.
- [x] Hacer las tarjetas del Dashboard clickeables en toda su superficie.
- [x] Evitar dobles aperturas de calculadoras por doble clic.
- [x] Mostrar una vista previa de la matriz antes de elegir el método.
- [x] Ampliar el desglose de conversiones de bases.
- [x] Usar títulos comprensibles para los módulos.

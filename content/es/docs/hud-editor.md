## Abrir el editor {#open}

Elige **Editar HUD** en la parte inferior del menú de mods, o asigna una tecla a *Abrir el editor del HUD* en Opciones, Controles, Skell Client. La pantalla muestra tus widgets sobre el juego, la barra de **Editar HUD** y el panel **Widgets**.

:::figure hud-editor
Arrastra los widgets. Prueba Shift, las flechas, Supr y R.
:::

## Anclaje {#anchoring}

Al soltar un widget, se ancla al punto más cercano de la pantalla: izquierda, centro o derecha, y arriba, medio o abajo, por tercios. Un widget anclado a la derecha crece hacia la izquierda, así que ya no se sale de la pantalla ni salta cuando cambia su contenido, la resolución o la pantalla completa. El widget elegido muestra su ancla en el panel.

Las posiciones guardadas antes de la versión 0.15 se quedan donde estaban: un widget sin ancla se trata como centrado, que es la fórmula vieja.

## Mover y cambiar de tamaño {#moving}

- **Imán**: los widgets se pegan a los bordes, al centro y a los otros widgets, con guías y una separación de 4 px. Mantén [[Shift]] para soltar el imán.
- **Tamaño**: arrastra la esquina del widget elegido en pasos de 5 %, o usa la rueda del mouse.
- **Teclado**: las flechas mueven un widget 1 px, [[Delete]] lo oculta y [[R]] lo restablece.
- **Clic derecho** en una fila del panel Widgets abre los ajustes de ese widget.

## La barra y el panel {#bar}

La barra de **Editar HUD** se arrastra desde su asa a cualquier parte sin tocar ningún widget. El cliente recuerda su posición, como fracción de la pantalla, y un doble clic en el asa la devuelve abajo al centro. Incluye deshacer, rehacer y restablecer.

El panel **Widgets** lista cada widget por categoría con un switch para mostrarlo u ocultarlo. Un inspector sobre el widget elegido da acceso rápido a sus ajustes, a restablecer y a ocultar.

## Deshacer y rehacer {#undo}

[[Ctrl]] [[Z]] deshace y [[Ctrl]] [[Shift]] [[Z]] o [[Ctrl]] [[Y]] rehace, hasta 60 pasos. Mover, cambiar de tamaño, ocultar y restablecer forman parte del historial.

## Atajos {#shortcuts}

| Acción | Entrada |
|---|---|
| Mover | Arrastrar |
| Soltar el imán | Mantener [[Shift]] |
| Mover 1 px | Flechas |
| Ocultar | [[Delete]] |
| Restablecer el widget | [[R]] |
| Deshacer | [[Ctrl]] [[Z]] |
| Rehacer | [[Ctrl]] [[Shift]] [[Z]] o [[Ctrl]] [[Y]] |
| Devolver la barra | Doble clic en su asa |

En el celular, el editor muestra pistas para el dedo.

## Widgets {#widgets}

:::figure hud-widgets
Una muestra de los widgets del HUD: FPS, coordenadas, teclas, radar, armadura y el reproductor de música.
:::

La página HUD tiene 33 módulos, desde FPS y Coordenadas hasta Radar, Light Meter, Pickup Feed y Performance Monitor. La [Referencia de módulos](docs:modules) los lista todos con sus ajustes.

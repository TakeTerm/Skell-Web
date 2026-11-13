## Abrir y mover el menú {#open}

Pulsa [[Right Shift]] en un mundo o en la pantalla de inicio. La tecla se cambia en Opciones, Controles, Skell Client. La ventana se abre centrada y se arrastra desde su barra superior, la zona del logo y del título. Puede salirse en parte de la pantalla, pero la barra siempre queda a mano: entera en vertical y con al menos 120 px en horizontal, también al cambiar la resolución o la escala del GUI. Los sliders, botones y campos de texto nunca mueven la ventana.

:::figure menu-window
Barra lateral a la izquierda y tarjetas de módulos a la derecha. Cada tarjeta tiene ícono, descripción, botón de ajustes y switch.
:::

## La barra lateral {#sidebar}

La barra lateral agrupa las páginas en cuatro bloques. El contador de cada página de módulos muestra cuántos están activos del total.

| Bloque | Páginas |
|---|---|
| Módulos | HUD, PvP, Utilidades, Efectos visuales |
| Estilo | Cosméticos, Kill Efects |
| Tools | Checkpoints, Macros, Discord |
| Cliente | Perfiles, Cliente |

En ventanas angostas la barra deja solo los íconos, con ayuda al pasar el mouse, y en ventanas bajas se compacta. Abajo están tu perfil y los accesos a Editar HUD, Grabaciones y la carpeta de Skell.

:::note Sobre la demo de este sitio
La demo interactiva recrea las páginas de módulos y la página Cliente con el catálogo real. Las páginas Kill Efects, Checkpoints, Macros, Discord y Perfiles existen en el cliente, pero no se recrean en la web.
:::

## Encontrar un módulo {#find}

Cada página de módulos tiene chips para sus subgrupos, con contador:

- **HUD**: Info, Player, Media, Game UI.
- **PvP**: Combat info, Stats.
- **Utilidades**: Movement, Capture, Inventory, World, System.
- **Efectos visuales**: Combat, World, Camera, Hands & motion, Player, Effects.

El chip *Activado* deja solo lo que está encendido. Lo marcado **NEW** se añadió en la versión actual, y lo nuevo va antes que el resto de su grupo, después de tus favoritos. Marca una tarjeta como favorita para tenerla siempre primero.

Para buscar, pulsa [[Ctrl]] [[F]] o simplemente escribe. [[Enter]] abre el primer resultado y los resultados conservan su categoría.

## Ajustes de un módulo {#settings}

El botón de ajustes de una tarjeta abre sus ajustes con una vista previa en vivo arriba: el widget real del HUD, el cosmético en 3D o la animación del efecto de kill. Debajo hay **Activado**, **Tecla** y la posición en el HUD, y luego todos los ajustes en grupos con una descripción corta. *Restablecer valores* está al final.

Los controles son los mismos en todas partes: switches, sliders con su valor, un selector segmentado para hasta tres opciones o un desplegable para más, un selector de color con saturación, tono, alfa, colores rápidos y hex, y un campo de texto con cursor, pegar y seleccionar todo.

### Dos diseños {#layouts}

Cliente, Menús, Diseño de los ajustes elige dónde aparecen los ajustes. Los dos dibujan el mismo contenido, así que cambiar de modo nunca reinicia nada.

:::figure layouts
Cambia entre la hoja y el panel lateral, y prueba los colores de acento.
:::

- **Hoja** crece desde la tarjeta del módulo y cubre la ventana.
- **Panel lateral** muestra tarjetas anchas en dos columnas y deja los ajustes al lado de la ventana. Un clic en la tarjeta abre sus ajustes. El switch, o el clic derecho, enciende el módulo.

Cuando la ventana es demasiado angosta, el cliente usa la hoja automáticamente.

## Ajustes del cliente {#client}

La página **Cliente** controla el color de acento, el diseño de ajustes, las animaciones y el idioma.

- **Color de acento** tiñe los switches, las selecciones, los bordes y el foco en todo el menú. Admite un color propio.
- **Animaciones** puede ser Completa, Reducida o Desactivado. Reducida acorta los movimientos y Desactivado los quita, incluido el fundido entre menús y la intro.
- **Idioma** es inglés o español. Lo que no tenga traducción se muestra en inglés, y las notificaciones siguen el idioma del cliente.

## Teclado {#keyboard}

| Tecla | Acción |
|---|---|
| [[Right Shift]] | Abrir o cerrar el menú |
| [[Ctrl]] [[F]] o escribir | Buscar módulos |
| [[Enter]] | Abrir el primer resultado |
| [[Tab]] / [[Shift]] [[Tab]] | Página siguiente o anterior |
| [[Esc]] | Cierra en orden: desplegable, hoja, búsqueda, menú |
| [[C]] | Zoom, mientras se mantiene |
| [[Left Alt]] | Freelook, mientras se mantiene |
| [[G]] | Inspeccionar un modelo de espada |
| [[B]] | Rueda de emotes |
| [[F8]] | Guardar los últimos 30 segundos con los clips instantáneos |
| [[Left Shift]] | Shulker Preview, mientras se mantiene sobre una shulker |

Todas las teclas se cambian en Opciones, Controles, Skell Client. Abrir el editor del HUD, la galería de capturas, el cronómetro y las teclas de música no tienen tecla por defecto.

:::tip Dos teclas por módulo
Zoom, Freelook, Sword Models y los clips instantáneos muestran dos filas en sus ajustes: la tecla que mantienes o pulsas para usar la función, y la tecla que solo enciende o apaga el módulo.
:::

## 0.15.1 {#v0-15-1}

Versión actual. Minecraft {{minecraft}}, Fabric Loader {{fabricLoader}}, Fabric API {{fabricApi}}, Java {{java}}.

- **Nombre y emblema nuevos.** Todo se llama Skell Client, con un logo nuevo, y tu configuración anterior, perfiles, checkpoints, macros y teclas se migran en el primer inicio.
- **Dos diseños de ajustes**, Hoja y Panel lateral, que dibujan el mismo contenido. Etiquetas NEW en cada opción añadida en esta versión, mostradas primero en su grupo.
- **La ventana del menú** se abre centrada y se arrastra. La barra de Editar HUD tiene un asa para moverla y recuerda dónde la dejaste.
- **Idiomas** con banderas nítidas, 47 textos que faltaban en español, 10 corregidos y un solo término para «checkpoints» y «kill». Las notificaciones siguen el idioma del cliente.
- **Grabador y clips de 30 segundos**: la copia de cada frame salió del hilo de render, el codificador por hardware se elige bien, los clips se exportan sin recodificar y el codificador corre con prioridad baja.
- **Módulos nuevos**: Click Pulse, No Block Rotation, Name Changer, Headless Korblox, Sword Models, 3D UI, Halloween, Crystal Chams, Crypto Pets, Astral Weapon Trails, Celestial Weather, Line Glyphs, Realistic Water, Waving Foliage, Wet Ground, Snow Ground, Self Visuals, World Color y World Menu, con previews animadas. También llegan Kill Streak, Death Point, Pickup Feed, NPC, Sahur Pet y Larp FPS.
- **Kill effects** con finishers: Execution, Singularity, Soul Pyre, Tung Tung, Tung Tung Floss y Samurai, con una vista previa 3D que usa tu skin.
- **Lyrics Island**, una píldora que se estira con la línea, y un aviso Clip guardado para los clips instantáneos.
- **Checkpoints** reemplaza el nombre anterior en inglés y español, conservando tus datos guardados.
- **Estabilidad**: un widget con error ya no tumba todo el HUD, los módulos que fallan al dibujar se apagan con una notificación y se corrigieron varias fugas.
- **Celular**: barras de scroll arrastrables y desplazamiento táctil en PojavLauncher y MojoLauncher, con estados claros de «no disponible en celular».

## 0.15.0 {#v0-15-0}

Una remodelación de la interfaz.

- **Un solo sistema de diseño** para todo el menú, con barra lateral agrupada, chips de subgrupos, tarjetas más ricas y una hoja de ajustes que crece desde la tarjeta con vista previa en vivo.
- **Editor del HUD** con anclaje al borde más cercano, imán con guías, tamaño en pasos de 5 %, movimiento con flechas, deshacer y rehacer hasta 60 pasos y un panel Widgets.
- **Pantalla de Grabaciones** con el Grabador, los clips instantáneos, una lista de videos con duración, filtros y borrado con confirmación.
- **Radar** con tus checkpoints, los jugadores del locator bar y los jugadores a la vista.
- **Perfiles** con seis espacios y **códigos para compartir** (`SKELL1-…`).
- Ajuste **Animaciones**: Completa, Reducida o Desactivado.
- **Correcciones**: widgets del HUD que saltaban o se salían de la pantalla, video estirado al grabar con F11 y varios textos armados en cada frame. La basura por frame del menú bajó cerca de un 98 % en la lista de módulos del escenario medido.
- Visual FPS (+10) ahora arranca apagado en instalaciones nuevas.

## 0.14.1 {#v0-14-1}

- **Clips instantáneos con audio del escritorio.** Los clips manuales y los guardados al matar incluyen sonido estéreo del dispositivo de salida predeterminado de Windows, nunca el micrófono, como AAC a 160 kbit/s.

## 0.14.0 {#v0-14-0}

- **Performance Monitor** con una gráfica de tiempos por fotograma, mínimos del 1 %, P95 y memoria, y un perfilador opcional de los ticks de los módulos.
- **Vista previa de los kill effects** con tu skin dentro del menú.
- **Clips instantáneos**, un búfer de 30 segundos que se guarda con una tecla o al matar.

## 0.13.2 {#v0-13-2}

- Los kill effects tienen su propia página con opciones exclusivas, y la opción Body Fragments pasa a llamarse Samurai.

## 0.13.1 {#v0-13-1}

- **Optimización** de la generación de geometría. En un benchmark local del motor de efectos, la CPU por escena pasó de 116,2 µs a 83,5 µs y la memoria temporal de 204,1 KiB a 9,3 KiB. Mide la generación de geometría, no el tiempo total de un frame.

## 0.13.0 {#v0-13-0}

- **Módulos nuevos**: Shulker Preview, Item Details, Inventory Alert y Light Meter.
- Modo **Lyrics Compact**.
- **Grabador** que captura la imagen de Minecraft en vez del escritorio, y que es correcto con F11.

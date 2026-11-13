## Instalación {#installation}

:::faq
### El juego no inicia o el mod no aparece
Comprueba que Fabric Loader {{fabricLoader}}, Fabric API {{fabricApi}} y Java {{java}} estén instalados para Minecraft {{minecraft}}. Skell Client necesita Fabric API en la carpeta `mods`. El log del juego dice qué dependencia falta.

### Tengo dos jars de Skell Client
Las versiones viejas son el mismo mod con otro id. Deja un solo jar en la carpeta `mods` y quita los demás.

### ¿Pierdo mi configuración al actualizar?
No. En el primer inicio el cliente copia la configuración, los perfiles, los checkpoints y las macros del nombre anterior al nuevo, y conserva las teclas guardadas. Los archivos viejos no se borran.
:::

## Usar el menú {#menu}

:::faq
### El menú no se abre
La tecla por defecto es [[Right Shift]]. Si otro mod la usa, cambia la tecla en Opciones, Controles, Skell Client.

### Mi HUD se ve igual que el de vanilla
Todos los módulos arrancan apagados. Abre el menú, ve a la página HUD y enciende los widgets que quieras.

### Un widget está fuera de la pantalla o en un lugar equivocado
Abre Editar HUD y usa el botón de restablecer de la barra, o elige el widget y pulsa [[R]]. Los widgets se anclan al borde más cercano, así que siguen los cambios de resolución.

### Asigné una tecla a Zoom o Freelook y el módulo se apaga
La Tecla de un módulo solo lo enciende o lo apaga. La tecla que mantienes para usar Zoom, Freelook, Sword Models o los clips instantáneos es otra fila aparte en sus ajustes.
:::

## Grabación y clips {#recording}

:::faq
### El grabador o los clips instantáneos no hacen nada
Los dos necesitan Windows, porque usan el ejecutable de FFmpeg incluido para Windows. El grabador y los clips instantáneos se usan de uno en uno. Después de encender los clips instantáneos, espera el calentamiento de 30 segundos antes de pulsar [[F8]].

### Los clips instantáneos están apagados cada vez que inicio el juego
Es a propósito: su estado no se restaura desde configuraciones ni perfiles, para que la captura nunca empiece sola.

### El clip dura 31 segundos
La exportación *Fast* copia el video ya codificado y empieza en un fotograma clave, así que un clip dura entre 30 y 31 segundos. Elige *Exact* para 30 segundos justos.

### Mi clip no tiene sonido
El audio es el del dispositivo de salida predeterminado de Windows, nunca el micrófono. Si el dispositivo no se puede abrir o falla durante la captura, el cliente avisa y detiene los clips instantáneos, para que no guardes clips mudos sin saberlo.
:::

## Rendimiento {#performance}

:::faq
### ¿Cómo reduzco el costo del cliente?
Apaga lo que no uses: los módulos apagados no hacen tick ni se dibujan. Performance Monitor muestra los tiempos por fotograma y los mínimos del 1 %, y *Profile module ticks* mide el costo de CPU de cada módulo.

### El número de FPS es más alto que mis FPS reales
Larp FPS cambia solo el número que se muestra. Apágalo para ver el valor real.

### El juego va lento en segundo plano
Unfocused FPS en Performance es 30 por defecto, y el cliente limita el juego a 30 FPS cuando la ventana no tiene foco.
:::

## Celular {#mobile}

:::faq
### ¿Puedo usarlo en PojavLauncher o MojoLauncher?
El cliente detecta los lanzadores basados en Android y añade desplazamiento táctil: arrastra el contenido, con impulso, y arrastra las barras de scroll. Un toque sin mover el dedo sigue funcionando como clic. Para probar el modo táctil en un PC, agrega `-Dskell.touch=true` a los argumentos de Java.

### ¿Qué no funciona en el celular?
Discord Rich Presence no tiene a qué conectarse en un celular, el grabador y los clips instantáneos usan un ejecutable de Windows, y la música de Spotify necesita una conexión a internet mediante Last.fm o la API de Spotify.
:::

## Otras preguntas {#other}

:::faq
### ¿Es público?
Todavía no. Skell Client está en constante desarrollo y será público pronto. Estas guías describen la versión {{version}}.

### ¿Está afiliado a Mojang o Microsoft?
No. Skell Client es un proyecto independiente. Minecraft es una marca de Mojang Studios.

### ¿Qué módulos no se incluyen a propósito?
El cliente deja fuera los módulos que dan ventaja sobre otros jugadores o sirven para engañarlos, como ESP, X-ray, tracers, chams, freecam, listas de staff o pagos falsos. El Radar solo muestra lo que el servidor ya envía y lo que tienes a la vista.
:::

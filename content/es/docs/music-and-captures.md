## Letras {#lyrics}

Lyrics muestra la línea que suena, sincronizada con los tiempos de LRCLIB. Tiene cuatro modos:

- **Island**, el predeterminado en configuraciones nuevas, es una píldora que se estira con resortes según la línea, con un disco que gira, un ecualizador de cuatro barras y la línea revelándose letra a letra. Si la línea no cabe, se desplaza. Sin línea, muestra la canción y el artista.
- **Compact** muestra una línea pequeña con un indicador de reproducción, y puede ir encima del reproductor de música.
- **HUD** pone la línea en el HUD.
- **World** coloca la letra en el mundo.

:::figure lyrics-island
El modo Island, con una línea de ejemplo.
:::

La fuente, el tamaño, el color, el ancho, el desfase de sincronía y el efecto de texto son comunes a los modos.

## Reproductor de música {#music}

El reproductor muestra portada, título y progreso. En Windows el cliente lee la sesión de medios del sistema, así que sigue lo que reproduzcas. Las teclas de medios para reproducir, pausar, siguiente y anterior se asignan en Opciones, Controles, Skell Client. Music Beats reacciona al audio del escritorio en Windows.

:::note Celular
En Android, un juego no puede ver la música de otras apps. El reproductor necesita una conexión a internet con Last.fm o la API de Spotify.
:::

## Capturas de pantalla {#screenshots}

Las capturas se numeran, con una vista previa animada y acciones en el chat, y una galería que se abre con una tecla. La galería prepara las miniaturas fuera del hilo de render y mantiene una caché acotada.

## Grabador {#recorder}

El grabador captura solo la imagen de Minecraft, no el escritorio, desde el framebuffer del juego. Sigue correcto cuando cambia F11 o el tamaño de la ventana: el tamaño del video sale del monitor al empezar y la imagen se acomoda con franjas negras. El escalado se hace en la GPU, y la codificación y la escritura ocurren fuera del hilo de render.

| Opción | Valores |
|---|---|
| Resolución | 720p, 1080p o Full, hasta 4K |
| Audio | Audio del escritorio de Windows con WASAPI, nunca el micrófono |
| Codificador | Por hardware si está disponible, por software si no |
| Salida | MP4 |

En Windows el grabador usa un ejecutable de FFmpeg incluido, como proceso aparte; mira [Créditos y licencias](docs:credits).

## Clips instantáneos {#instant-replay}

Los clips instantáneos (Instant Replay) guardan los últimos 30 segundos para que puedas guardar un clip después del momento.

:::steps
- Enciende Utilidades, Clips instantáneos y espera el calentamiento de 30 segundos.
- Pulsa [[F8]] para guardar los últimos 30 segundos, o activa *Save on player kill*.
- Cuando el archivo está listo, aparece el aviso Clip guardado y el archivo sale en Grabaciones como `Clip-N.mp4`.
:::

:::figure clip-toast
El aviso Clip guardado. Su posición y visibilidad son opciones de los clips instantáneos.
:::

- El búfer guarda segmentos de video comprimidos, no fotogramas sin comprimir, y se recorta a unos 33 segmentos. Se detiene si supera 256 MiB.
- El clip dura entre 30 y 31 segundos con la exportación *Fast* predeterminada, porque empieza en un fotograma clave. *Exact* recodifica a 30 segundos justos.
- El audio es AAC estéreo a 160 kbit/s del dispositivo de salida predeterminado, con su propio hilo y un búfer circular fijo de 40 segundos.
- Al salir de un mundo o servidor el búfer se detiene y libera todo, y se reanuda al entrar a otro.
- Los clips instantáneos arrancan apagados y su estado no se restaura desde configuraciones ni perfiles. El grabador y los clips instantáneos se usan de uno en uno.
- Solo hay una exportación pendiente, con 10 segundos entre peticiones.

## Pantalla de grabaciones {#recordings}

La pantalla de Grabaciones muestra arriba los controles del Grabador y de los clips instantáneos, y debajo la lista de videos, con duración, fecha, peso y tipo.

:::figure recordings
La pantalla de Grabaciones, reconstruida para la web. Prueba grabar, guardar un clip y borrar una fila.
:::

Filtra por Todos, Grabaciones o Clips. De cada archivo puedes reproducirlo, mostrarlo en su carpeta (en Windows queda seleccionado) y borrarlo con confirmación: *¿Borrar?* se mantiene 3 segundos.

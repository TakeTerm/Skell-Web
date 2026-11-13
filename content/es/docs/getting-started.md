## Qué es Skell Client {#what-is}

Skell Client es un mod cliente de Fabric para Minecraft {{minecraft}}. Añade un menú de mods de estilo vidrio, un editor de HUD que recuerda dónde va cada widget, más de 140 módulos, letras sincronizadas, un grabador y clips de 30 segundos. Lo desarrolla Take de forma independiente.

:::soon Lanzamiento público muy pronto
Skell Client está en constante desarrollo y será público pronto. Estas guías describen la versión {{version}}, para que sepas qué esperar antes de que la descarga esté disponible.
:::

:::figure menu-window
La página HUD del menú de mods, reconstruida para la web con los módulos reales del cliente.
:::

## Requisitos {#requirements}

| Componente | Versión |
|---|---|
| Minecraft | {{minecraft}} |
| Fabric Loader | {{fabricLoader}} |
| Fabric API | {{fabricApi}} |
| Java | {{java}} |

El grabador, los clips de 30 segundos y la sesión de música del sistema necesitan Windows. El resto del cliente no depende del sistema operativo. En los lanzadores móviles PojavLauncher y MojoLauncher el cliente detecta el dispositivo y añade desplazamiento táctil; mira [Problemas y preguntas frecuentes](docs:troubleshooting#mobile) para saber qué no está disponible allí.

## Instalación {#install}

:::steps
- Instala Fabric Loader {{fabricLoader}} para Minecraft {{minecraft}} con el instalador de Fabric.
- Pon Fabric API {{fabricApi}} en la carpeta `mods` de tu directorio de Minecraft.
- Pon `skell-client-{{version}}.jar` en la misma carpeta.
- Quita cualquier jar anterior de Skell Client. Las versiones viejas son el mismo mod con otro id y solo puede haber uno instalado.
- Inicia el juego y pulsa [[Right Shift]] para abrir el menú de mods.
:::

La descarga todavía no está publicada. Mientras tanto, esta lista muestra cómo será la instalación.

:::note Tu configuración se conserva
En el primer inicio el cliente copia la configuración, los perfiles, los checkpoints y las macros del nombre anterior al nuevo, y pasa tus teclas guardadas. No se borra nada de la ubicación vieja.
:::

## Primer inicio {#first-launch}

Todos los módulos arrancan apagados, así que el juego se ve igual que Minecraft hasta que eliges qué usar. Una buena primera sesión:

:::steps
- Abre el menú con [[Right Shift]] y mira la página **HUD**. Enciende FPS, Coordenadas o cualquier widget que quieras.
- Abre la pantalla **Editar HUD** desde la parte inferior de la barra lateral y arrastra cada widget a su lugar.
- Pulsa el botón de ajustes de un módulo para ver su vista previa en vivo y todos sus ajustes, agrupados.
- Guarda el resultado como un perfil en **Perfiles**, para restaurarlo o compartirlo después.
:::

## Siguientes pasos {#next}

- [Interfaz y controles](docs:interface) explica el menú, la búsqueda, los atajos y los dos diseños de ajustes.
- [Editor del HUD](docs:hud-editor) cubre el anclaje, el imán, deshacer y todos los atajos.
- [Visuales y cosméticos](docs:visuals), [Música y capturas](docs:music-and-captures) y [Utilidades](docs:utilities) describen las funciones por área.
- La [Referencia de módulos](docs:modules) lista cada módulo y ajuste.

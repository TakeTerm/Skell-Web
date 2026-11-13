## Vistas previas en vivo {#previews}

Cada módulo con un efecto visual muestra una vista previa arriba de sus ajustes, y la vista previa lee esos ajustes, así que mover un slider se nota al instante. Los widgets del HUD se dibujan como el widget real, los cosméticos en 3D con tu propia skin y los módulos animados como pequeñas escenas dibujadas con las primitivas del menú.

Las vistas previas son aproximaciones. No usan el pipeline del mundo, así que el bloom, las partículas suaves y algunos colores pueden diferir un poco del juego.

## Kill effects {#kill-effects}

Después de derrotar a un jugador, se reproduce una animación sobre la víctima. El módulo se llama **Kill Efects** en el menú de la {{version}} y vive en Efectos visuales.

:::figure clip-toast
El mismo estilo de tarjeta se usa en el aviso Clip guardado de los clips instantáneos.
:::

| Efecto | Qué pasa |
|---|---|
| Random | Elige uno de los demás cada vez |
| Execution | Un corte parte la figura en dos |
| Singularity | Un núcleo oscuro absorbe la figura |
| Soul Pyre | La figura se consume en almas que suben |
| Tung Tung, Tung Tung Floss | Finishers de personaje |
| Samurai | El cuerpo de tu jugador se rompe en trozos con los colores del equipo |

Con un finisher elegido, los ajustes son **Colors** (Style, Theme o Custom), **Primary Color**, **Secondary Color**, **Bloom**, **Sound**, **Volume** y **Render Distance**. Samurai conserva sus propios ajustes.

La vista previa de los ajustes reproduce la coreografía real con tu skin sobre una figura 3D. Si el 3D falla una vez, el menú vuelve a una versión 2D dibujada con las regiones de tu skin.

:::note En este sitio
La pestaña de kill effects de la demo es una aproximación 2D hecha para la web con una figura neutra. Tung Tung y Tung Tung Floss forman parte del cliente y no se recrean aquí.
:::

Los efectos solo reaccionan a la muerte de jugadores. Nunca borran entidades reales ni cambian nada en el servidor.

## Efectos del mundo {#world}

La página de Efectos visuales reúne los módulos del mundo. Entre ellos:

- **Agua realista**, **Waving Foliage**, **Wet Ground** y **Snow Ground** cambian cómo se dibuja el terreno. Están escritos para convivir con Sodium e Iris, y el cliente vuelve al dibujo original si una combinación no es compatible.
- **Celestial Weather** añade lluvias de meteoros, polvo estelar flotante y lluvia luminosa, **Halloween** trae una luna de cosecha y brasas a la deriva, y **World Color** y **Sky Shaders** cambian los colores y el cielo.
- **Ambience** controla la hora del día, el clima, la niebla, el lightmap y el color del cielo, y **Motion Blur**, **Aspect** y **No FOV** dan forma a la imagen.

Un módulo de mundo que falla al dibujar se apaga solo y envía una notificación, con el error completo en el log, en vez de cerrar el juego.

## Visuales del jugador {#player}

- **Sahur Pet** te sigue a un lado, detrás o en órbita, con resorte, giro hacia donde caminas y un saludo con salto al golpear.
- **NPC** crea un jugador falso que solo existe en tu cliente. Puedes elegir su nombre, skin, vida, si muere de un golpe, el tiempo de reaparición y si copia tu armadura. El servidor y los demás jugadores nunca lo ven.
- **Self Visuals** estiliza a tu jugador con colores y cometas, **Sword Models** sustituye las espadas por cuchillos, un Ledger o un reloj de pulsera, y **Hand Shaders**, **Click Pulse** y **Player Trails** añaden efectos a tu mano, tus clics y tu movimiento.

## Cosméticos {#cosmetics}

La página Cosméticos agrupa Cape, Wings, Hats, Aura, Accessories, Emotes, Pets, Player Model, Player Trails, Skin Changer, Music Beats y más. Abre la rueda de emotes con [[B]].

:::tip Compara antes de decidir
Abre los ajustes de un cosmético para verlo sobre tu propia skin antes de encenderlo.
:::

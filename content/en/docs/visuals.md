## Live previews {#previews}

Every module with a visual effect shows a preview at the top of its settings, and the preview reads the settings, so moving a slider is visible at once. HUD widgets are drawn as the real widget, cosmetics in 3D with your own skin, and the animated modules as small scenes drawn with the menu primitives.

The previews are approximations. They do not use the world pipeline, so bloom, soft particles and some colors can differ slightly from the game.

## Kill effects {#kill-effects}

After you defeat a player, one animation plays on the victim. The module is called **Kill Efects** in the {{version}} menu and lives in Visuals.

:::figure clip-toast
The same card style is used for the Clip saved notice of Instant Replay.
:::

| Effect | What happens |
|---|---|
| Random | Picks one of the others each time |
| Execution | A cut splits the figure in two |
| Singularity | A dark core pulls the figure in |
| Soul Pyre | The figure burns away into rising souls |
| Tung Tung, Tung Tung Floss | Character finishers |
| Samurai | Your player body breaks into pieces with the colors of the team |

With a finisher selected the settings are **Colors** (Style, Theme or Custom), **Primary Color**, **Secondary Color**, **Bloom**, **Sound**, **Volume** and **Render Distance**. Samurai keeps its own settings.

The preview in the settings plays the real choreography with your skin on a 3D figure. If the 3D preview fails once, the menu falls back to a 2D version drawn with the regions of your skin.

:::note On this site
The kill effects tab of the demo is a 2D approximation built for the web with a neutral figure. Tung Tung and Tung Tung Floss are part of the client and are not recreated here.
:::

Effects only react to player deaths. They never delete real entities and never change anything on the server.

## World effects {#world}

The Visuals page holds the world modules. Among them:

- **Realistic Water**, **Waving Foliage**, **Wet Ground** and **Snow Ground** change how terrain is rendered. They are written to coexist with Sodium and Iris, and the client falls back to the original rendering if a combination is not compatible.
- **Celestial Weather** adds meteor showers, floating stardust and luminous rain, **Halloween** brings a harvest moon and drifting cinders, and **World Color** and **Sky Shaders** change colors and the sky.
- **Ambience** controls time of day, weather, fog, lightmap and sky color, and **Motion Blur**, **Aspect** and **No FOV** shape the image.

A world module that fails while drawing switches itself off and sends a notification, with the full error in the log, instead of closing the game.

## Player visuals {#player}

- **Sahur Pet** follows you at your side, behind you or orbiting, with a spring, a turn toward where you walk and a jump greeting when you hit.
- **NPC** creates a fake player that exists only in your client. You can set its name, skin, health, whether it dies in one hit, respawn time and whether it copies your armor. The server and other players never see it.
- **Self Visuals** styles your player with colors and comets, **Sword Models** replaces held swords with knives, a Ledger or a wristwatch, and **Hand Shaders**, **Click Pulse** and **Player Trails** add effects to your hand, your clicks and your movement.

## Cosmetics {#cosmetics}

The Cosmetics page groups Cape, Wings, Hats, Aura, Accessories, Emotes, Pets, Player Model, Player Trails, Skin Changer, Music Beats and more. Open the emote wheel with [[B]].

:::tip Compare before you commit
Open the settings of a cosmetic to see it on your own skin before switching it on.
:::

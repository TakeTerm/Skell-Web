## What Skell Client is {#what-is}

Skell Client is a Fabric client mod for Minecraft {{minecraft}}. It adds a glass-style mods menu, an HUD editor that remembers where every widget belongs, more than 140 modules, synced lyrics, a recorder and 30-second clips. It is developed independently by Take.

:::soon Public launch coming soon
Skell Client is under constant development and will be public soon. These guides describe version {{version}}, so you can see what to expect before the download is available.
:::

:::figure menu-window
The HUD page of the mods menu, rebuilt for the web from the client's real modules.
:::

## Requirements {#requirements}

| Component | Version |
|---|---|
| Minecraft | {{minecraft}} |
| Fabric Loader | {{fabricLoader}} |
| Fabric API | {{fabricApi}} |
| Java | {{java}} |

The recorder, the 30-second clips and the system music session need Windows. The rest of the client does not depend on the operating system. On the mobile launchers PojavLauncher and MojoLauncher the client detects the device and adds touch scrolling; see [Troubleshooting](docs:troubleshooting#mobile) for what is not available there.

## Installing {#install}

:::steps
- Install Fabric Loader {{fabricLoader}} for Minecraft {{minecraft}} with the Fabric installer.
- Put Fabric API {{fabricApi}} in the `mods` folder of your Minecraft directory.
- Put `skell-client-{{version}}.jar` in the same folder.
- Remove any earlier Skell Client jar. Older builds are the same mod under another id, and only one can be installed.
- Start the game and press [[Right Shift]] to open the mods menu.
:::

The download is not published yet. Until it is, this list shows how the installation will work.

:::note Your settings carry over
On first start the client copies the settings, profiles, checkpoints and macros of the previous name to the new one, and moves your saved keys. Nothing is deleted from the old location.
:::

## First launch {#first-launch}

Every module starts switched off, so the game looks exactly like Minecraft until you choose what to use. A good first session:

:::steps
- Open the menu with [[Right Shift]] and look at the **HUD** page. Switch on FPS, Coordinates or any widget you want.
- Open the **Edit HUD** screen from the bottom of the sidebar and drag each widget where you like it.
- Press the settings button of a module to see its live preview and every setting, grouped.
- Save the result as a profile in **Profiles**, so you can restore or share it later.
:::

## Where to go next {#next}

- [Interface & controls](docs:interface) explains the menu, search, shortcuts and the two settings layouts.
- [HUD editor](docs:hud-editor) covers anchoring, snapping, undo and every shortcut.
- [Visuals & cosmetics](docs:visuals), [Music & captures](docs:music-and-captures) and [Utilities](docs:utilities) describe the features by area.
- The [Module reference](docs:modules) lists every module and setting.

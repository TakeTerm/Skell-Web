## Installation {#installation}

:::faq
### The game does not start or the mod does not appear
Check that Fabric Loader {{fabricLoader}}, Fabric API {{fabricApi}} and Java {{java}} are installed for Minecraft {{minecraft}}. Skell Client needs Fabric API in the `mods` folder. The game log shows which dependency is missing.

### I have two Skell Client jars
Older builds are the same mod under another id. Keep only one jar in the `mods` folder and remove the rest.

### Do I lose my settings when I update?
No. On first start the client copies the settings, profiles, checkpoints and macros of the previous name to the new one, and keeps the saved keys. The old files are not deleted.
:::

## Using the menu {#menu}

:::faq
### The menu does not open
The default key is [[Right Shift]]. If another mod uses it, change the key in Options, Controls, Skell Client.

### My HUD looks the same as vanilla
Every module starts off. Open the menu, go to the HUD page and switch on the widgets you want.

### A widget is outside the screen or in the wrong place
Open Edit HUD and use the reset button of the bar, or select the widget and press [[R]]. Widgets are anchored to the nearest edge, so they follow resolution changes.

### I assigned a key to Zoom or Freelook and the module turns off
The Keybind of a module only switches it on or off. The key you hold to use Zoom, Freelook, Sword Models or Instant Replay is a separate row in their settings.
:::

## Recording and clips {#recording}

:::faq
### The recorder or Instant Replay do nothing
Both need Windows, because they use the FFmpeg executable bundled for Windows. Recorder and Instant Replay are used one at a time. After you switch on Instant Replay, wait for the 30-second warm-up before pressing [[F8]].

### Instant Replay is off every time I start the game
That is intentional: its state is not restored from configurations or profiles, so capture never starts on its own.

### The clip is 31 seconds long
The *Fast* export copies the already encoded video and starts at a keyframe, so a clip lasts between 30 and 31 seconds. Choose *Exact* for precisely 30 seconds.

### My clip has no sound
Audio is the Windows default output device, never the microphone. If the device cannot be opened or fails during capture, the client warns you and stops Instant Replay, so you never save silent clips without knowing.
:::

## Performance {#performance}

:::faq
### How do I lower the cost of the client?
Switch off what you do not use: switched-off modules do not tick and are not drawn. Performance Monitor shows frame times and 1% lows, and *Profile module ticks* measures the CPU cost of each module.

### The FPS number is higher than my real FPS
Larp FPS changes only the number displayed. Switch it off to see the real value.

### The game is slow in the background
Unfocused FPS in Performance is 30 by default, and the client limits the game to 30 FPS when the window has no focus.
:::

## Mobile {#mobile}

:::faq
### Can I use it on PojavLauncher or MojoLauncher?
The client detects Android-based launchers and adds touch scrolling: drag the content, with inertia, and drag the scrollbars. A tap without moving still works as a click. To test touch mode on a computer, add `-Dskell.touch=true` to the Java arguments.

### What does not work on mobile?
Discord Rich Presence has no connection to make on a phone, the recorder and Instant Replay use a Windows executable, and Spotify music needs an internet connection through Last.fm or the Spotify API.
:::

## Other questions {#other}

:::faq
### Is it public?
Not yet. Skell Client is under constant development and will be public soon. These guides describe version {{version}}.

### Is it affiliated with Mojang or Microsoft?
No. Skell Client is an independent project. Minecraft is a trademark of Mojang Studios.

### Which modules are not included on purpose?
The client leaves out modules that give an advantage over other players or help deceive them, such as ESP, X-ray, tracers, chams, freecam, staff lists or fake payments. The Radar only shows what the server already sends and what you can see.
:::

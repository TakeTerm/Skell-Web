## 0.15.1 {#v0-15-1}

Current version. Minecraft {{minecraft}}, Fabric Loader {{fabricLoader}}, Fabric API {{fabricApi}}, Java {{java}}.

- **New name and emblem.** Everything is now Skell Client, with a new logo, and your previous configuration, profiles, checkpoints, macros and keys are migrated on first start.
- **Two settings layouts**, Sheet and Side panel, that draw the same content. NEW badges on every option added in this version, shown first in their group.
- **Menu window** opens centered and can be dragged. The Edit HUD bar has a handle to move it, and remembers where you left it.
- **Languages** with crisp flags, 47 missing Spanish texts, 10 corrected and one term for "checkpoints" and "kill". Notifications follow the language of the client.
- **Recorder and 30-second clips**: the frame copy moved out of the render thread, the hardware encoder is chosen reliably, clips export without re-encoding, and the encoder runs at low priority.
- **New modules**: Click Pulse, No Block Rotation, Name Changer, Headless Korblox, Sword Models, 3D UI, Halloween, Crystal Chams, Crypto Pets, Astral Weapon Trails, Celestial Weather, Line Glyphs, Realistic Water, Waving Foliage, Wet Ground, Snow Ground, Self Visuals, World Color and World Menu, with animated previews. Kill Streak, Death Point, Pickup Feed, NPC, Sahur Pet and Larp FPS also arrive.
- **Kill effects** with finishers: Execution, Singularity, Soul Pyre, Tung Tung, Tung Tung Floss and Samurai, with a 3D preview that uses your skin.
- **Lyrics Island**, a pill that stretches with the line, and a Clip saved notice for Instant Replay.
- **Checkpoints** replaces the old name in English and Spanish, keeping your saved data.
- **Stability**: a widget with an error no longer takes the whole HUD down, modules that fail while drawing switch off with a notification, and several leaks were fixed.
- **Mobile**: draggable scrollbars and touch scrolling on PojavLauncher and MojoLauncher, with clear "not available on mobile" states.

## 0.15.0 {#v0-15-0}

A remodel of the interface.

- **One design system** for the whole menu, with a grouped sidebar, subgroup chips, richer cards and a settings sheet that grows from the card with a live preview.
- **HUD editor** with anchoring to the nearest edge, snapping with guides, resize in 5% steps, arrow nudging, undo and redo up to 60 steps and a Widgets panel.
- **Recordings screen** with the Recorder, Instant Replay, a video list with duration, filters and delete with confirmation.
- **Radar** with your checkpoints, the locator bar players and the players in sight.
- **Profiles** with six slots and **share codes** (`SKELL1-…`).
- **Animations** setting: Full, Reduced or Off.
- **Fixes**: HUD widgets that jumped or left the screen, stretched video when recording with F11, and several texts built on every frame. The garbage per frame of the menu dropped by about 98% on the module list in the measured scenario.
- Visual FPS (+10) now starts off on new installations.

## 0.14.1 {#v0-14-1}

- **Instant Replay with desktop audio.** Manual clips and clips saved on a kill include stereo sound from the Windows default output device, never the microphone, as AAC at 160 kbit/s.

## 0.14.0 {#v0-14-0}

- **Performance Monitor** with a frame-time graph, 1% lows, P95 and memory, and optional profiling of module ticks.
- **Kill effect preview** with your skin inside the menu.
- **Instant Replay**, a 30-second buffer saved with a key or on a kill.

## 0.13.2 {#v0-13-2}

- Kill effects get their own page with exclusive options, and the previous Body Fragments option becomes Samurai.

## 0.13.1 {#v0-13-1}

- **Optimization** of geometry generation. In a local benchmark of the effects engine, CPU per scene went from 116.2 µs to 83.5 µs and temporary memory from 204.1 KiB to 9.3 KiB. It measures geometry generation, not total frame time.

## 0.13.0 {#v0-13-0}

- **New modules**: Shulker Preview, Item Details, Inventory Alert and Light Meter.
- **Lyrics Compact** mode.
- **Recorder** that captures the Minecraft image instead of the desktop, and is correct with F11.

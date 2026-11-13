## Open the editor {#open}

Choose **Edit HUD** at the bottom of the mods menu, or assign a key to *Open HUD Editor* in Options, Controls, Skell Client. The screen shows your widgets over the game, the **Edit HUD** bar and the **Widgets** panel.

:::figure hud-editor
Drag the widgets. Try Shift, the arrow keys, Delete and R.
:::

## Anchoring {#anchoring}

When you release a widget, it anchors to the nearest point of the screen: left, center or right, and top, middle or bottom, by thirds. A widget anchored to the right grows toward the left, so it no longer leaves the screen or jumps when its content, the resolution or the fullscreen mode changes. The selected widget shows its anchor in the panel.

Positions saved before version 0.15 keep their place: a widget without an anchor is treated as centered, which is the old formula.

## Moving and resizing {#moving}

- **Snapping**: widgets snap to the edges, the center and the other widgets, with guides and a 4 px gap. Hold [[Shift]] to release the snap.
- **Resize**: drag the corner of the selected widget in 5% steps, or use the mouse wheel.
- **Keyboard**: the arrow keys move a widget 1 px, [[Delete]] hides it and [[R]] resets it.
- **Right click** on a row of the Widgets panel opens the settings of that widget.

## The bar and the panel {#bar}

The **Edit HUD** bar can be dragged from its handle to any place without touching a widget. The client remembers its position, as a fraction of the screen, and a double click on the handle returns it to the bottom center. It contains undo, redo and reset.

The **Widgets** panel lists every widget by category with a switch to show or hide it. An inspector over the selected widget gives quick access to its settings, reset and hide.

## Undo and redo {#undo}

[[Ctrl]] [[Z]] undoes and [[Ctrl]] [[Shift]] [[Z]] or [[Ctrl]] [[Y]] redoes, up to 60 steps. Moving, resizing, hiding and resetting are all part of the history.

## Shortcuts {#shortcuts}

| Action | Input |
|---|---|
| Move | Drag |
| Release the snap | Hold [[Shift]] |
| Nudge 1 px | Arrow keys |
| Hide | [[Delete]] |
| Reset the widget | [[R]] |
| Undo | [[Ctrl]] [[Z]] |
| Redo | [[Ctrl]] [[Shift]] [[Z]] or [[Ctrl]] [[Y]] |
| Return the bar | Double click on its handle |

On a phone, the editor shows hints for touch input.

## Widgets {#widgets}

:::figure hud-widgets
A sample of the HUD widgets: FPS, coordinates, keystrokes, radar, armor and the music player.
:::

The HUD page has 33 modules, from FPS and Coordinates to Radar, Light Meter, Pickup Feed and Performance Monitor. The [Module reference](docs:modules) lists them all with their settings.

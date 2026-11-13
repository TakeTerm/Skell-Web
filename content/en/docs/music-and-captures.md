## Lyrics {#lyrics}

Lyrics shows the line that is playing, synced with the timing of LRCLIB. It has four modes:

- **Island**, the default for new configurations, is a pill that stretches with springs to the length of the line, with a spinning disc, a four-bar equalizer and the line revealed letter by letter. If the line does not fit, it scrolls. With no line it shows the song and the artist.
- **Compact** shows a small line with a playback indicator, and can sit above the music player.
- **HUD** puts the line on the HUD.
- **World** places the lyrics in the world.

:::figure lyrics-island
The Island mode, with a sample line.
:::

Font, size, color, width, sync offset and text effect are shared across the modes.

## Music player {#music}

The music player shows cover, title and progress. On Windows the client reads the system media session, so it follows whatever you play. Media keys for play, pause, next and previous can be assigned in Options, Controls, Skell Client. Music Beats reacts to desktop audio on Windows.

:::note Mobile
On Android, a game cannot see the music of other apps. The player needs an internet connection with Last.fm or the Spotify API there.
:::

## Screenshots {#screenshots}

Screenshots are numbered, with an animated preview and actions in the chat, and a gallery that can be opened with a key. The gallery prepares thumbnails away from the render thread and keeps a bounded cache.

## Recorder {#recorder}

The recorder captures only the Minecraft image, not the desktop, from the game framebuffer. It stays correct when F11 or the window size changes: the video size comes from the monitor when recording starts, and the image is letterboxed with black bars. Scaling happens on the GPU, and encoding and writing happen off the render thread.

| Option | Values |
|---|---|
| Resolution | 720p, 1080p or Full, up to 4K |
| Audio | Windows desktop audio through WASAPI, never the microphone |
| Encoder | Hardware encoder when available, software otherwise |
| Output | MP4 |

On Windows the recorder uses a bundled FFmpeg executable as a separate process; see [Credits & licenses](docs:credits).

## Instant Replay {#instant-replay}

Instant Replay keeps the last 30 seconds so you can save a clip after the moment.

:::steps
- Switch on Utility, Instant Replay and wait for the 30-second warm-up.
- Press [[F8]] to save the last 30 seconds, or enable *Save on player kill*.
- When the file is ready, a Clip saved notice appears and the file shows up in Recordings as `Clip-N.mp4`.
:::

:::figure clip-toast
The Clip saved notice. Position and visibility are options of Instant Replay.
:::

- The buffer holds compressed video segments, not raw frames, and is trimmed to about 33 segments. It stops if it exceeds 256 MiB.
- The clip lasts between 30 and 31 seconds in the default *Fast* export, because it starts at a keyframe. *Exact* re-encodes to precisely 30 seconds.
- Audio is stereo AAC at 160 kbit/s from the default output device, with its own thread and a fixed circular buffer of 40 seconds.
- Leaving a world or server stops the buffer and frees everything, and it resumes on entering another.
- Instant Replay starts off and its state is not restored from configurations or profiles. Recorder and Instant Replay are used one at a time.
- Only one export is pending, with 10 seconds between requests.

## Recordings screen {#recordings}

The Recordings screen shows the Recorder and Instant Replay controls on top and a list of videos below, with duration, date, size and type.

:::figure recordings
The Recordings screen, rebuilt for the web. Try recording, saving a clip and deleting a row.
:::

Filter by All, Recordings or Clips. For each file you can play it, show it in its folder (on Windows it stays selected) and delete it with a confirmation: *Delete?* stays for 3 seconds.

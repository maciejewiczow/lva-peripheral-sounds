# lva-perpiheral-sounds
Linux voice assistant peripheral that allows attaching additional sounds to any LVA event.

## Sound configuration

Set `LVA_SOUNDS_<EVENT>` to a glob pattern matching WAV files or directories
containing WAV files, for example:

```env
LVA_SOUNDS_WAKE_WORD_DETECTED=/path/to/wake-sounds
LVA_SOUNDS_TIMER_RINGING=/path/to/timer-sounds/*.wav
LVA_SOUNDS_LISTENING=/path/to/sound-sets/*
```

Event names are listed in [lva/events.py](lva/events.py). An unset event is
silent. Each time an event occurs, a random `.wav` file (case-insensitive
extension) is selected from the matching files and the files directly inside
any matching directories. Multiple directories share one pool of sounds.
Directory contents are not searched recursively, but patterns may use `**` to
match recursively. Glob matching is case-sensitive on Linux, so `*.wav` does not
match `.WAV`. Changes are picked up on the next event. Patterns with no matching
WAV files are silent; invalid or unreadable WAV files are logged when selected.
WAV files must be readable, uncompressed PCM files.

When running in Docker, mount the sound directories into the container and use
their container paths in the patterns.

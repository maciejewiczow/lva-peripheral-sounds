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

## Docker audio

The example Compose configuration connects to the host user's PipeWire or
PulseAudio server. Set `LVA_USER_ID`, `LVA_USER_GROUP`, and
`LVA_XDG_RUNTIME_DIR` to the audio user's UID, primary GID, and runtime
directory. If the PulseAudio socket or cookie is elsewhere, also set
`LVA_PULSE_SERVER` and `LVA_PULSE_COOKIE` to their host paths and mount them
into the container at those same paths. These variables configure Compose
interpolation, so set them in the shell or the Compose `.env` file.
If the runtime directory differs from `/run/user/1000`, set the PulseAudio
socket and cookie paths explicitly as well.

Make sure the host audio server is running and the user can play audio on the
host first. Apply the example settings to your deployed Compose file and rebuild
or update the image to include the Dockerfile changes. Recreate the container
after changing its configuration:

```sh
docker compose up -d --force-recreate sounds-peripheral
docker compose exec sounds-peripheral pw-play /app/sounds/startup.wav
docker compose logs sounds-peripheral
```

Replace the example WAV path with a file mounted in your container. If playback
still fails, check that the host runtime directory contains `pipewire-0` for
PipeWire or `pulse/native` for PulseAudio, and that the configured user can
access the socket and any required cookie. The application prefers `pw-play`
when installed; player errors appear in the container logs.

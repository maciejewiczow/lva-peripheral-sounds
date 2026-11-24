#!/usr/bin/env python3

import asyncio
import glob
import json
import logging
import random
import shutil
import subprocess
from pathlib import Path

import websockets
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from lva.events import LVAEvent


def play_random_sound(pattern: str | None):
    if pattern is None:
        return

    sounds: set[Path] = set()
    for match in glob.iglob(pattern, recursive=True):
        path = Path(match)
        if path.is_dir():
            try:
                sounds.update(
                    child for child in path.iterdir()
                    if child.suffix.lower() == ".wav" and child.is_file()
                )
            except OSError:
                log.exception("Failed to read sounds directory: %s", path)
        elif path.suffix.lower() == ".wav" and path.is_file():
            sounds.add(path)

    if not sounds:
        log.info("No WAV files matched sound pattern: %s", pattern)
        return

    sound = random.choice(tuple(sounds))

    player = shutil.which("pw-play") or shutil.which("paplay")

    if player is None:
        log.error("Cannot play sound: neither pw-play nor paplay is installed")
        return

    log.info(f"Playing sound: {sound}")
    try:
        subprocess.Popen(
            [player, str(sound)],
            stdout=subprocess.DEVNULL,
        )
    except OSError:
        log.exception("Failed to start sound player")


class Env(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LVA_SOUNDS_')

    ws_url: str = Field(default="ws://0.0.0.0:6055", validation_alias="WS_URL")

    WAKE_WORD_DETECTED: str | None = None
    LISTENING: str | None = None
    STT_TEXT: str | None = None
    THINKING: str | None = None
    TTS_TEXT: str | None = None
    TTS_SPEAKING: str | None = None
    TTS_FINISHED: str | None = None
    PIPELINE_ERROR: str | None = None
    DISCONNECTED: str | None = None
    IDLE: str | None = None
    MUTED: str | None = None
    TIMER_TICKING: str | None = None
    TIMER_UPDATED: str | None = None
    TIMER_RINGING: str | None = None
    MEDIA_PLAYER_PLAYING: str | None = None
    VOLUME_CHANGED: str | None = None
    VOLUME_MUTED: str | None = None
    ZEROCONF: str | None = None
    LIGHT_COMMAND: str | None = None
    BUTTON_LOCK_CHANGED: str | None = None

    STARTUP: str | None = None


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

env = Env()


async def websocket_loop():
    play_random_sound(env.STARTUP)

    while True:
        try:
            async with websockets.connect(env.ws_url) as websocket:
                log.info(f"Connected to LVA at {env.ws_url}")

                while True:
                    data = await websocket.recv()
                    log.debug(f"Event from lva: {data}")

                    event = json.loads(data)["event"]

                    try:
                        current_state = LVAEvent(event)
                    except ValueError:
                        log.error(
                            f"current state is not a valid event: {event}")
                        continue

                    log.info(f"Event received: {current_state}")
                    match current_state:
                        case LVAEvent.WAKE_WORD_DETECTED:
                            play_random_sound(env.WAKE_WORD_DETECTED)
                        case LVAEvent.LISTENING:
                            play_random_sound(env.LISTENING)
                        case LVAEvent.STT_TEXT:
                            play_random_sound(env.STT_TEXT)
                        case LVAEvent.THINKING:
                            play_random_sound(env.THINKING)
                        case LVAEvent.TTS_TEXT:
                            play_random_sound(env.TTS_TEXT)
                        case LVAEvent.TTS_SPEAKING:
                            play_random_sound(env.TTS_SPEAKING)
                        case LVAEvent.TTS_FINISHED:
                            play_random_sound(env.TTS_FINISHED)
                        case LVAEvent.PIPELINE_ERROR:
                            play_random_sound(env.PIPELINE_ERROR)
                        case LVAEvent.DISCONNECTED:
                            play_random_sound(env.DISCONNECTED)
                        case LVAEvent.IDLE:
                            play_random_sound(env.IDLE)
                        case LVAEvent.MUTED:
                            play_random_sound(env.MUTED)
                        case LVAEvent.TIMER_TICKING:
                            play_random_sound(env.TIMER_TICKING)
                        case LVAEvent.TIMER_UPDATED:
                            play_random_sound(env.TIMER_UPDATED)
                        case LVAEvent.TIMER_RINGING:
                            play_random_sound(env.TIMER_RINGING)
                        case LVAEvent.MEDIA_PLAYER_PLAYING:
                            play_random_sound(env.MEDIA_PLAYER_PLAYING)
                        case LVAEvent.VOLUME_CHANGED:
                            play_random_sound(env.VOLUME_CHANGED)
                        case LVAEvent.VOLUME_MUTED:
                            play_random_sound(env.VOLUME_MUTED)
                        case LVAEvent.ZEROCONF:
                            play_random_sound(env.ZEROCONF)
                        case LVAEvent.LIGHT_COMMAND:
                            play_random_sound(env.LIGHT_COMMAND)
                        case LVAEvent.BUTTON_LOCK_CHANGED:
                            play_random_sound(env.BUTTON_LOCK_CHANGED)

        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("fatal error in lva loop")
            await asyncio.sleep(1)


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(websocket_loop())


if __name__ == "__main__":
    asyncio.run(main())

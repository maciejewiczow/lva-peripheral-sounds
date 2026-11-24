from enum import Enum


class LVAEvent(str, Enum):
    """Events broadcast from LVA to peripheral clients."""

    WAKE_WORD_DETECTED = "wake_word_detected"
    LISTENING = "listening"
    STT_TEXT = "stt_text"
    THINKING = "thinking"
    TTS_TEXT = "tts_text"
    TTS_SPEAKING = "tts_speaking"
    TTS_FINISHED = "tts_finished"
    PIPELINE_ERROR = "pipeline_error"
    DISCONNECTED = "disconnected"
    IDLE = "idle"
    MUTED = "muted"
    TIMER_TICKING = "timer_ticking"
    TIMER_UPDATED = "timer_updated"
    TIMER_RINGING = "timer_ringing"
    MEDIA_PLAYER_PLAYING = "media_player_playing"
    VOLUME_CHANGED = "volume_changed"
    VOLUME_MUTED = "volume_muted"
    ZEROCONF = "zeroconf"
    LIGHT_COMMAND = "light_command"
    BUTTON_LOCK_CHANGED = "button_lock_changed"

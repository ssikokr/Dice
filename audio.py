"""Cross-platform audio engine for Dice Arcade.

Supports asynchronous, non-blocking sound playback across:
- Windows (native winsound)
- macOS (afplay CLI)
- Linux (paplay, aplay, play CLI)
- Silent fallback for headless/CI environments.
"""

import os
import shutil
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_SOUND_ENABLED = True


def toggle_sound(enabled=None):
    """Toggle or set sound playback state.

    Args:
        enabled: Optional bool. If None, toggles current state.

    Returns:
        bool: The new sound enabled state.
    """
    global _SOUND_ENABLED
    if enabled is None:
        _SOUND_ENABLED = not _SOUND_ENABLED
    else:
        _SOUND_ENABLED = bool(enabled)
    return _SOUND_ENABLED


def is_sound_enabled():
    """Return whether sound is currently enabled."""
    return _SOUND_ENABLED


def play_sound(filename):
    """Play an audio file asynchronously across Windows, macOS, and Linux.

    Silently ignores missing files, disabled sound, or unsupported environments.
    """
    if not _SOUND_ENABLED:
        return

    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        return

    # Windows native winsound (non-blocking)
    if sys.platform.startswith("win"):
        try:
            import winsound  # pylint: disable=import-outside-toplevel
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
        except (ImportError, OSError, RuntimeError):
            pass

    # macOS native afplay (non-blocking background process)
    if sys.platform == "darwin" and shutil.which("afplay"):
        try:
            subprocess.Popen(
                ["afplay", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        except (OSError, ValueError):
            pass

    # Linux native players: paplay (PulseAudio), aplay (ALSA), play (SoX)
    if sys.platform.startswith("linux"):
        for player in ("paplay", "aplay", "play"):
            if shutil.which(player):
                try:
                    subprocess.Popen(
                        [player, path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return
                except (OSError, ValueError):
                    pass

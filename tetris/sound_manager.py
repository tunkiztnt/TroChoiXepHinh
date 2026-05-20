"""
Sound manager - generates and plays game sounds + background music using pygame.
All audio is generated programmatically (no external files needed).
"""
import pygame
import numpy as np
import threading


# ---------------------------------------------------------------------------
# Music note frequencies (Hz)
# ---------------------------------------------------------------------------
NOTE = {
    "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61,
    "G3": 196.00, "A3": 220.00, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46,
    "G5": 783.99, "A5": 880.00, "B5": 987.77,
    "C6": 1046.50,
    "R":  0.0,   # rest
}

# Korobeiniki (Tetris Theme A) — melody + bass
# Each entry: (note_name, duration_in_beats)
TETRIS_MELODY = [
    ("E5", 1), ("B4", 0.5), ("C5", 0.5),
    ("D5", 1), ("C5", 0.5), ("B4", 0.5),
    ("A4", 1), ("A4", 0.5), ("C5", 0.5),
    ("E5", 1), ("D5", 0.5), ("C5", 0.5),
    ("B4", 1.5), ("C5", 0.5),
    ("D5", 1), ("E5", 1),
    ("C5", 1), ("A4", 1),
    ("A4", 2),

    ("R",  0.5), ("D5", 0.5),
    ("F5", 1), ("A5", 1),
    ("G5", 0.5), ("F5", 0.5),
    ("E5", 1.5), ("C5", 0.5),
    ("E5", 1), ("D5", 0.5), ("C5", 0.5),
    ("B4", 1), ("B4", 0.5), ("C5", 0.5),
    ("D5", 1), ("E5", 1),
    ("C5", 1), ("A4", 1),
    ("A4", 2),
]

TETRIS_BASS = [
    ("A3", 0.5), ("E3", 0.5), ("A3", 0.5), ("E3", 0.5),
    ("E3", 0.5), ("B3", 0.5), ("E3", 0.5), ("B3", 0.5),
    ("A3", 0.5), ("E3", 0.5), ("A3", 0.5), ("E3", 0.5),
    ("E3", 0.5), ("B3", 0.5), ("E3", 0.5), ("B3", 0.5),
    ("G3", 0.5), ("D3", 0.5), ("G3", 0.5), ("D3", 0.5),
    ("G3", 0.5), ("D3", 0.5), ("G3", 0.5), ("D3", 0.5),
    ("A3", 0.5), ("E3", 0.5), ("A3", 0.5), ("E3", 0.5),
    ("A3", 0.5), ("E3", 0.5), ("A3", 0.5), ("E3", 0.5),

    ("D3", 0.5), ("A3", 0.5), ("D3", 0.5), ("A3", 0.5),
    ("D3", 0.5), ("A3", 0.5), ("D3", 0.5), ("A3", 0.5),
    ("E3", 0.5), ("B3", 0.5), ("E3", 0.5), ("B3", 0.5),
    ("E3", 0.5), ("B3", 0.5), ("E3", 0.5), ("B3", 0.5),
    ("A3", 0.5), ("E3", 0.5), ("A3", 0.5), ("E3", 0.5),
    ("E3", 0.5), ("B3", 0.5), ("E3", 0.5), ("B3", 0.5),
    ("G3", 0.5), ("D3", 0.5), ("G3", 0.5), ("D3", 0.5),
    ("A3", 0.5), ("E3", 0.5), ("A3", 0.5), ("E3", 0.5),
    ("A3", 0.5), ("E3", 0.5), ("A3", 0.5), ("E3", 0.5),
]

SAMPLE_RATE = 44100
BPM = 160  # beats per minute


class SoundManager:
    """Manages all game sounds and background music."""

    def __init__(self):
        pygame.mixer.pre_init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)

        self.sounds = {}
        self.sound_enabled = True
        self.music_enabled = True
        self._music_channel = None
        self._music_sound = None

        self._generate_sounds()
        self._generate_music()

    # ------------------------------------------------------------------
    # Internal audio helpers
    # ------------------------------------------------------------------

    def _make_wave(self, freq, duration, volume=0.3, wave_type="sine", vibrato=False):
        """Return a numpy float32 mono array for a single note."""
        n = int(SAMPLE_RATE * duration)
        if n == 0:
            return np.zeros(1, dtype=np.float32)
        t = np.linspace(0, duration, n, endpoint=False)

        if freq == 0:
            wave = np.zeros(n, dtype=np.float32)
        else:
            if vibrato:
                freq_mod = freq * (1 + 0.003 * np.sin(2 * np.pi * 5.5 * t))
                phase = np.cumsum(2 * np.pi * freq_mod / SAMPLE_RATE)
                wave = np.sin(phase).astype(np.float32)
            elif wave_type == "sine":
                wave = np.sin(2 * np.pi * freq * t).astype(np.float32)
            elif wave_type == "square":
                wave = np.sign(np.sin(2 * np.pi * freq * t)).astype(np.float32)
            elif wave_type == "sawtooth":
                wave = (2 * (t * freq - np.floor(0.5 + t * freq))).astype(np.float32)
            elif wave_type == "triangle":
                wave = (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1).astype(np.float32)
            else:
                wave = np.sin(2 * np.pi * freq * t).astype(np.float32)

            # ADSR-style envelope
            attack  = int(n * 0.02)
            decay   = int(n * 0.08)
            sustain = int(n * 0.80)
            release = n - attack - decay - sustain
            env = np.concatenate([
                np.linspace(0, 1,   attack,  endpoint=False),
                np.linspace(1, 0.7, decay,   endpoint=False),
                np.full(sustain, 0.7),
                np.linspace(0.7, 0, max(release, 1)),
            ])
            env = env[:n]
            wave = wave * env

        return (wave * volume).astype(np.float32)

    def _to_sound(self, mono: np.ndarray) -> pygame.mixer.Sound:
        """Convert a mono float32 array to a pygame Sound (stereo int16)."""
        clipped = np.clip(mono, -1.0, 1.0)
        int16 = (clipped * 32767).astype(np.int16)
        stereo = np.column_stack((int16, int16))
        return pygame.sndarray.make_sound(stereo)

    def _beat_duration(self, beats: float) -> float:
        """Convert beats to seconds at current BPM."""
        return beats * 60.0 / BPM

    # ------------------------------------------------------------------
    # Sound effects
    # ------------------------------------------------------------------

    def _generate_sounds(self):
        """Generate all SFX."""
        self.sounds["move"]       = self._to_sound(self._make_wave(220, 0.05, 0.18, "sine"))
        self.sounds["rotate"]     = self._to_sound(self._make_wave(440, 0.07, 0.22, "sine"))
        self.sounds["drop"]       = self._to_sound(self._make_wave(110, 0.14, 0.38, "square"))
        self.sounds["hard_drop"]  = self._to_sound(self._make_wave(80,  0.18, 0.45, "square"))
        self.sounds["pause"]      = self._to_sound(self._make_wave(330, 0.18, 0.20, "sine"))

        self.sounds["line_clear"] = self._to_sound(self._build_melody(
            [("C5", 0.08), ("E5", 0.08), ("G5", 0.08), ("C6", 0.16)], 0.28, "sine"))

        self.sounds["tetris"] = self._to_sound(self._build_melody(
            [("C5", 0.07), ("E5", 0.07), ("G5", 0.07), ("C6", 0.07),
             ("E6", 0.07), ("C6", 0.07), ("E6", 0.07), ("G6", 0.14)], 0.35, "sine"))

        self.sounds["level_up"] = self._to_sound(self._build_melody(
            [("A4", 0.09), ("C5", 0.09), ("E5", 0.09),
             ("A5", 0.09), ("C6", 0.09), ("E6", 0.18)], 0.30, "triangle"))

        self.sounds["game_over"] = self._to_sound(self._build_melody(
            [("A4", 0.18), ("G4", 0.18), ("F4", 0.18), ("E4", 0.18),
             ("D4", 0.18), ("C4", 0.18), ("B3", 0.18), ("A3", 0.36)], 0.40, "sawtooth"))

        self.sounds["win"] = self._to_sound(self._build_melody(
            [("C5", 0.10), ("E5", 0.10), ("G5", 0.10), ("C6", 0.10),
             ("G5", 0.10), ("C6", 0.10), ("E6", 0.10), ("G6", 0.20)], 0.38, "sine"))

    def _build_melody(self, note_dur_pairs, total_vol, wave_type):
        """Build a melody from (note_name, duration_sec) pairs."""
        parts = []
        for name, dur in note_dur_pairs:
            freq = NOTE.get(name, 0)
            parts.append(self._make_wave(freq, dur, total_vol, wave_type))
        return np.concatenate(parts).astype(np.float32)

    # ------------------------------------------------------------------
    # Background music (Korobeiniki / Tetris Theme A)
    # ------------------------------------------------------------------

    def _generate_music(self):
        """
        Synthesise the full Tetris theme loop as a pygame Sound.
        Melody uses a triangle wave (bright, chiptune-ish).
        Bass uses a sine wave (warm, low).
        """
        beat = self._beat_duration(1.0)

        # --- melody ---
        mel_parts = []
        for name, beats in TETRIS_MELODY:
            dur = beat * beats
            freq = NOTE.get(name, 0)
            mel_parts.append(self._make_wave(freq, dur, 0.30, "triangle", vibrato=(freq > 0)))
        melody_arr = np.concatenate(mel_parts).astype(np.float32)

        # --- bass ---
        bass_parts = []
        for name, beats in TETRIS_BASS:
            dur = beat * beats
            freq = NOTE.get(name, 0)
            bass_parts.append(self._make_wave(freq, dur, 0.18, "sine"))
        bass_arr = np.concatenate(bass_parts).astype(np.float32)

        # Pad shorter track to match length
        max_len = max(len(melody_arr), len(bass_arr))
        if len(melody_arr) < max_len:
            melody_arr = np.pad(melody_arr, (0, max_len - len(melody_arr)))
        if len(bass_arr) < max_len:
            bass_arr = np.pad(bass_arr, (0, max_len - len(bass_arr)))

        # Mix
        mixed = np.clip(melody_arr + bass_arr, -1.0, 1.0)

        # Slight fade-in / fade-out at loop boundaries to avoid clicks
        fade = min(int(SAMPLE_RATE * 0.05), len(mixed) // 4)
        mixed[:fade]  *= np.linspace(0, 1, fade)
        mixed[-fade:] *= np.linspace(1, 0, fade)

        self._music_sound = self._to_sound(mixed)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def play(self, sound_name: str):
        """Play a one-shot sound effect."""
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()

    def start_music(self):
        """Start looping background music."""
        if not self.music_enabled or self._music_sound is None:
            return
        if self._music_channel and self._music_channel.get_busy():
            return  # already playing
        self._music_channel = self._music_sound.play(loops=-1)  # -1 = loop forever

    def stop_music(self):
        """Stop background music immediately."""
        if self._music_channel:
            self._music_channel.stop()

    def pause_music(self):
        """Pause background music."""
        if self._music_channel and self._music_channel.get_busy():
            self._music_channel.pause()

    def resume_music(self):
        """Resume paused background music."""
        if self._music_channel:
            self._music_channel.unpause()

    def toggle_music(self) -> bool:
        """Toggle background music on/off. Returns new state."""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.start_music()
        else:
            self.stop_music()
        return self.music_enabled

    def toggle_sound(self) -> bool:
        """Toggle SFX on/off. Returns new state."""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def cleanup(self):
        """Release mixer resources."""
        self.stop_music()
        pygame.mixer.quit()

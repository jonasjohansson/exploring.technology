# Circuit Playground 808 Drum machine
import time
from adafruit_circuitplayground import cp

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

bpm = 120  # Beats per minute, change this to suit your tempo

# The seven files assigned to the touchpads
audiofiles = ["fB_bd_tek.wav", "fB_elec_hi_snare.wav", "fB_elec_cymbal.wav",
               "fB_elec_blip2.wav", "fB_bd_zome.wav", "fB_bass_hit_c.wav",
               "fB_drum_cowbell.wav"]

def play_file(filename):
    cp.play_file(filename)
    time.sleep(bpm / 960)  # Sixteenth note delay


while True:
    if cp.touch_A1:
        play_file(audiofiles[0])
    if cp.touch_A2:
        play_file(audiofiles[1])
    if cp.touch_A3:
        play_file(audiofiles[2])
    if cp.touch_A4:
        play_file(audiofiles[3])
    if cp.touch_A5:
        play_file(audiofiles[4])
    if cp.touch_A6:
        play_file(audiofiles[5])
    if cp.touch_TX:
        play_file(audiofiles[6])
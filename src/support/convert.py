#!/usr/bin/env python

import subprocess, os, glob

## Rename wav files using frequency and pitch detection:
## GTR_08.wav ---> automated pitch detection & file renaming ---> C - 130.81 Hz - GTR_08.wav


WAV_DIR = r"C:/Conversion"
AUBIO_DIR = r"C:/Conversion"


def get_values(values):
    result = []
    for line in values.split("\n"):
        val = float(line.split()[1]) if line else 0
        if val > 0:
            result.append(val)
    return result


def average(values):
    return sum(values)/len(values)


def midi_to_note(midi):
    notes = "c c# d d# e f f# g g# a a# b".split()
    int_midi = int(round(midi))
    pitch = int_midi % 12
    return notes[pitch]


def get_freq_and_note(filename):
    filename = os.path.join(WAV_DIR, filename)
    aubiopitch = os.path.join(AUBIO_DIR, "aubiopitch")
    freqs = subprocess.check_output([aubiopitch, "-i", filename])
    midis = subprocess.check_output([aubiopitch, "-u", "midi", "-i", filename])
    freq = average(get_values(freqs))
    note = midi_to_note(average(get_values(midis)))
    return freq, note.upper()


def rename_file(filename):
    freq, note = get_freq_and_note(filename)
    newfile = "{0} - {1:0.2f} - {2}".format(note, freq, filename)
    full_old = os.path.join(WAV_DIR, filename)
    full_new = os.path.join(WAV_DIR, newfile)
    print "renaming", newfile
    os.rename(full_old, full_new)


for filename in glob.glob("*.wav"):
    rename_file(filename)

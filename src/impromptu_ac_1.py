# import unittest
import midi
import itertools
import math
from Tune import *

# turns ticks to time in seconds
# The formula used is:
# (# ticks * 60) / (BPM * resolution)
def ticksToTime(ticks, bpm, resolution):
	return (ticks * 60) / (bpm * resolution)

# takes in a duration in seconds, returns Duration enum value
# 1 second = quarter note
def secondsToDuration(dur):
	approx_power = math.log(1/dur, 2)
	note_val = 4 - (round(approx_power) + 2)
	return note_val

# Reads a MIDI file in, returns a list of Notes
# Notes are populated with onset and duration
# assumes a one line MIDI file with notes chronologically
def computeOnset(myfile):
	pattern = midi.read_midifile(myfile)
	NotesList = []
	index = 0
	bpm = 0
	resolution = pattern.resolution
	duration = 0;

	pattern.make_ticks_abs() # changes ticks to cumulative values
	# print pattern

	for track in pattern:
		for event in track:
			if isinstance(event, midi.SetTempoEvent):
				bpm = event.bpm
			if isinstance(event, midi.NoteEvent):
				if (isinstance(event, midi.NoteOffEvent) or (isinstance(event, midi.NoteOnEvent) and event.data[1] == 0)):
					endset = ticksToTime(event.tick, bpm, resolution)
					currNote = NotesList[index]
					duration = endset - currNote.onset
					currNote.duration = secondsToDuration(duration)
					index += 1
				else:
					onset = ticksToTime(event.tick, bpm, resolution)
					newNote = Note(onset = onset)
					NotesList.append(newNote)
	
	return NotesList		

# Takes a list of Notes, fills each Note in with Pitch information
# def calculateNotes(list_of_notes):
	# for note in list_of_notes:


# Takes a list of Notes, returns a list of Notes that are rests
def calculateRests(list_of_notes):
	n_notes = len(list_of_notes)
	RestsList = []

	for i in range(0, n_notes-2):
		pitch = Pitch(letter='r', octave=None, accidental=None)
		onset = list_of_notes[i].onset + list_of_notes[i].duration
		s_duration = list_of_notes[i+1].onset - onset
		duration = secondsToDuration(s_duration)
		rest = Note(duration=duration, frequency = 0.0, onset = onset, pitch = pitch)
		RestsList.append(rest)

	return RestsList

# Takes two lists of Notes (notes and rests), orders them by onset
# returns the merged list
# def computeNoteOrder(notes, rests)

list_of_notes = computeOnset("c-major-scale-treble.mid")
for note in list_of_notes:
	note.NotetoString
list_of_rests = calculateRests(list_of_notes)
for rest in list_of_rests:
	rest.NotetoString
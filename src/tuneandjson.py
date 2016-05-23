import math
import itertools
import sys
import abc
import json
import pprint
from TuneIter2 import *

#def TunetoJSON(tune):

def pitchJSONtoTune(pitch):
	if pitch['accidental'] != '':
		ksig_pitch_accidental = int(pitch['accidental'])
	else:
		ksig_pitch_accidental = ''
	ksig_pitch_letter = str(pitch['letter'])
	if pitch['octave'] != '':
		ksig_pitch_octave = int(pitch['octave'])
	else:
		ksig_pitch_octave = ''
	pitch = Pitch(accidental=ksig_pitch_accidental, letter=ksig_pitch_letter, octave=ksig_pitch_octave)
	return pitch

def durationJSONtoTune(dur_str):
	if dur_str == 'SIXTEENTH':
		dur = Duration.SIXTEENTH
	elif dur_str == 'EIGHTH':
		dur = Duration.EIGHTH
	elif dur_str == 'QUARTER':
		dur = Duration.QUARTER
	elif dur_str == 'HALF':
		dur = Duration.HALF
	elif dur_str =='WHOLE':
		dur = Duration.WHOLE
	return dur

def eventJSONtoTune(event):
	onset = float(event['onset'])
	duration = durationJSONtoTune(str(event['duration']))	
	#new_event = Event(duration=duration, onset=onset)

	if event['class'] == 'note':
		new_event = Note(duration=duration, onset=onset)
		n_frequency = float(event['frequency'])
		n_pitch = pitchJSONtoTune(event['pitch'])
		new_event.frequency = n_frequency
		new_event.setPitch(n_pitch)
	elif event['class'] == 'rest':
		new_event = Rest(duration=duration, onset=onset)
		r_pitch = pitchJSONtoTune(event['pitch'])
		new_event.setPitch(r_pitch)
	elif event['class'] == 'chord':	
		new_event = Chord(duration=duration, onset=onset)
		pitches = []
		for p in event['pitches']:
			pch = pitchJSONtoTune(p)
			pitches.append(p)
		new_event.setPitch(pitches)
	return new_event
		

def JSONtoTune(json_file):
	json_data = json.load(json_file)
	pprint.pprint(json_data)
	json_tune = json_data['tune']

	tune_title = json_tune['title']
	
	tune_contributors = []
	for contri in json_tune['contributors']:
		tune_contributors.append(str(contri))

	tune_clef = int(json_tune['clef'])

	tune_tsig1 = int(json_tune['timeSignature'][0])
	tune_tsig2 = int(json_tune['timeSignature'][1])
	tune_tsig = (tune_tsig1, tune_tsig2)

	tune_ksig_pitch = pitchJSONtoTune(json_tune['keySignature']['pitch'])
	iMflag = str(json_tune['keySignature']['isMajor'])
	iMflag.lower()
	if iMflag == 'true':
		ksig_isMajor = True
	if iMflag == 'false':
		ksigisMajor = False
	tune_ksig = Key(pitch=tune_ksig_pitch, isMajor=iMflag)

	tune_events = []
	for event in json_tune['events']:
		new = eventJSONtoTune(event)
		tune_events.append(new)

	tune = Tune()
	tune.setTitle(tune_title)
	tune.setContributors(tune_contributors)
	tune.clef = tune_clef
	tune.setTimeSignature(tune_tsig)
	tune.setKey(tune_ksig)
	tune.setEventsList(tune_events)

	tune.TunetoString()

fp = open("../tests/MIDITestFiles/tune.json")
JSONtoTune(fp)
#file1 = '../tests/MIDITestFiles/tune-with-chord-rest-note.mid'
#tune = Tune.TuneWrapper(file1)
#print tune.TunetoString()
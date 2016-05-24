import math
import itertools
import sys
import abc
import json
import pprint
from TuneIter2 import *

def durationTunetoJSON(tup):
	if tup == (1,1):
		return 'WHOLE'
	elif tup == (1,2):
		return 'HALF'
	elif tup == (1,4):
		return 'QUARTER'
	elif tup == (1,8):
		return 'EIGHTH'
	elif tup == (1,16):
		return 'SIXTEENTH'

def writePitchtoFile(pitch, myfile):
	letter = ''
	octave = ''
	accidental = ''
	if pitch.letter != None:
		letter = pitch.letter
	if pitch.octave != None:
		octave = str(pitch.octave)
	if pitch.accidental != None:
		accidental = str(pitch.accidental)
	myfile.write('\t\t\t\t"pitch":{\n\t\t\t\t\t"letter":"%c",\n\t\t\t\t\t"octave":"%s",\n\t\t\t\t\t"accidental":"%s"\n\t\t\t\t}\n' %(letter, octave, accidental))

def TunetoJSON(tune):
	if tune.title != None:
		filename = 'tune-' + tune.title + '.json'
	else:
		filename = 'tune-generic.json'
	f = open(filename, 'w')
	
	f.write('{\n')
	f.write('\t"tune": {\n')
	
	f.write('\t\t"timeSignature": ["%d","%d"],\n' %(tune.timeSignature[0], tune.timeSignature[1]))
	
	f.write('\t\t"clef": "%d",\n' %(tune.clef))
	
	if tune.title != None:
		f.write('\t\t"title": "%s",\n' %(tune.title))
	else:
		f.write('\t\t"title": "",\n')

	f.write('\t\t"contributors": [')
	if tune.contributors != None:
		n_contributors = len(tune.contributors)
		for num in (0, n_contributors - 1):
			f.write('"%s"' %(tune.contributors[num]))
			if num != n_contributors - 1:
				f.write(',')
	f.write('],\n')

	f.write('\t\t"events":[\n')
	events = tune.getEventsList()
	e_len = len(events)
	for x in range(0, e_len):
		event = events[x]
		f.write('\t\t\t{\n')
		if isinstance(event, Chord):
			f.write('\t\t\t\t"class":"chord",\n')
			f.write('\t\t\t\t"duration":"%lf",\n' %(event.duration))
			f.write('\t\t\t\t"s_duration":"%lf",\n' %(event.s_duration))
			f.write('\t\t\t\t"frequency":"%lf",\n' %(event.frequency))
			f.write('\t\t\t\t"onset":"%lf",\n' %(event.onset))
			
			f.write('\t\t\t\t"pitches":[\n')
			pitches = event.getPitch()
			n_pitches = len(pitches)
			for n in range(0, n_pitches):
				f.write('\t\t\t\t\t{\n')
				f.write('\t\t\t\t\t"letter":"%c",\n' %(pitches[n].letter))
				f.write('\t\t\t\t\t"octave":"%d",\n' %(pitches[n].octave))
				f.write('\t\t\t\t\t"accidental":"%d",\n' %(pitches[n].accidental))
				f.write('\t\t\t\t\t}')
				if n != n_pitches-1:
					f.write(',\n')
				else:
					f.write('\n')
			f.write('\t\t\t\t],\n')
			f.write('\t\t\t}')
		elif isinstance(event, Note) or isinstance(event, Rest):
			if isinstance(event, Note):
				f.write('\t\t\t\t"class":"note",\n')
			if isinstance(event, Rest):
				f.write('\t\t\t\t"class":"rest",\n')

			if event.duration != None:
				dur_str = durationTunetoJSON(event.duration)

				f.write('\t\t\t\t"duration":"%s",\n' %(dur_str))
			else:
				f.write('\t\t\t\t"duration":"",\n')
			if event.duration != None:
				f.write('\t\t\t\t"s_duration":"%lf",\n' %(event.s_duration))
			else:
				f.write('\t\t\t\t"s_duration":"",\n')
			if isinstance(event, Note) and event.frequency != None:
				f.write('\t\t\t\t"frequency":"%lf",\n' %(event.frequency))
			else:
				f.write('\t\t\t\t"frequency":"",\n')
			f.write('\t\t\t\t"onset":"%lf",\n' %(event.onset))
			if isinstance(event, Note):
				writePitchtoFile(event.pitch, f)


		f.write('\t\t\t}')
		if x != e_len-1:
			f.write(',\n')
		else:
			f.write('\n')			

	f.write('\t\t],\n')

	keysig = tune.keySignature
	if keysig == None:
		f.write('\t\t"keySignature": {}\n')
	else:
		f.write('\t\t"keySignature": {\n')
		if keysig.isMajor != None:
			f.write('\t\t\t"isMajor":"%s",\n' %(keysig.isMajor))
		else:
			f.write('\t\t\t"isMajor":"",\n')
		f.write('\t\t\t')
		writePitchtoFile(keysig.pitch, f)
		f.write('\t\t}\n')

	f.write('\t}\n')
	f.write('}\n')

	f.close

tune = Tune.TuneWrapper('../tests/MIDITestFiles/c-major-scale-treble.mid')
print tune.TunetoString()
tune.TunetoJSON()
pprint.pprint(tune.events)

###########################################################################
def pitchJSONtoTune(pitch):
	if str(pitch['accidental']) != '':
		ksig_pitch_accidental = int(pitch['accidental'])
	else:
		ksig_pitch_accidental = ''
	ksig_pitch_letter = str(pitch['letter'])
	if str(pitch['octave']) != '':
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
		#r_pitch = pitchJSONtoTune(event['pitch'])
		#new_event.setPitch(r_pitch)
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

	#tune.TunetoString()

#fp = open("../tests/MIDITestFiles/tune.json")
#JSONtoTune(fp)
file1 = '../tests/MIDITestFiles/tune-with-chord-rest-note.mid'
tune = Tune.TuneWrapper(file1)
print tune.TunetoString()



import unittest
import midi
import sys
sys.path.insert(0, '../src')
import os 
from TuneIter2 import *

#Please refer to class diagram for reference on parameter values for constructors and methods
class TestImpromptuBackend(unittest.TestCase):

	def testChordequal(self):
	    pitch1 = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
	    pitch2 = Pitch(letter='c', octave=4, accidental=Accidental.NATURAL)
	    pitch3 = Pitch(letter='a', octave=4, accidental=Accidental.FLAT)
	    chord = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.QUARTER, onset=0.5)
	    
	    pitchComp1 = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
	    pitchComp2 = Pitch(letter='c', octave=4, accidental=Accidental.NATURAL)
	    pitchComp3 = Pitch(letter='a', octave=4, accidental=Accidental.FLAT)
	    chordSame = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.QUARTER, onset=0.5)
	    chordSameDiffOrder = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.QUARTER, onset=0.5)

	    self.assertTrue(chord.chordEqual(chordSame))
	    self.assertTrue(chord.chordEqual(chordSameDiffOrder))

	    pitch4 = Pitch(letter='e', octave=4, accidental=Accidental.FLAT)
	    chordDiffNotes = Chord(pitches=[pitch1,pitch2,pitch4],duration=Duration.QUARTER, onset=0.5)
	    chordExtraNote = Chord(pitches=[pitch1,pitch2,pitch3, pitch4],duration=Duration.QUARTER, onset=0.5)
	    chordDiffDuration = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.HALF, onset=0.5)
	    chordDiffOnset = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.QUARTER, onset=0.0)

	    self.assertFalse(chord.chordEqual(chordDiffNotes))
	    self.assertFalse(chord.chordEqual(chordExtraNote))
	    self.assertFalse(chord.chordEqual(chordDiffDuration))
	    self.assertFalse(chord.chordEqual(chordDiffOnset))


	def testpitchequal(self):
		#Testing equality of the same note
		pitch = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
		samePitch = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
		self.assertTrue(pitch.pitchEqual(samePitch))
		
		#Testing equality of different notes
		differentLetter = Pitch(letter='c', octave=4, accidental=Accidental.FLAT)
		differentOctave = Pitch(letter='b', octave=5, accidental=Accidental.FLAT)
		differentAccidental = Pitch(letter='b', octave=4, accidental=Accidental.NATURAL)
		self.assertFalse(pitch.pitchEqual(differentLetter))
		self.assertFalse(pitch.pitchEqual(differentOctave))
		self.assertFalse(pitch.pitchEqual(differentAccidental))
	
	def testPitchGetterSetter(self):
		pitch = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
		note = Note(frequency=493.88, onset=0.0)
		note.setPitch(pitch)
		self.assertTrue(pitch.pitchEqual(note.getPitch()))

	def testIsRest(self):
		#Testing rest
		restPitch = Pitch(letter='r')
		rest = Event()
		rest.setPitch(restPitch)
		self.assertTrue(rest.isRest())
		
		#testing note
		notePitch = Pitch(letter='b', octave=4, accidental=Accidental.NATURAL)
		note = Event()
		note.setPitch(notePitch)
		self.assertFalse(note.isRest())
	
	def testNoteEqual(self):
		#Testing same notes
	    notePitch = Pitch(letter='b', octave=4, accidental=Accidental.NATURAL)
	    note = Note(frequency=493.88, onset=0.0, duration=Duration.QUARTER, pitch=notePitch)

	    samePitch = Pitch (letter='b', octave=4, accidental=Accidental.NATURAL)
	    sameNote = Note(frequency=493.88, onset=0.0, duration=Duration.QUARTER, pitch=samePitch)
	    self.assertTrue(note.noteEqual(sameNote))

	    #Testing different notes
	    differentPitch = Pitch (letter='c', octave=5, accidental=Accidental.FLAT)
	    diffPitchNote = Note(frequency=493.88, onset=0.0, duration=Duration.QUARTER, pitch=differentPitch)
	    self.assertFalse(note.noteEqual(diffPitchNote))

	    diffFreqNote = Note(frequency=350.0, onset=0.0, duration=Duration.QUARTER, pitch=samePitch)
	    self.assertFalse(note.noteEqual(diffFreqNote))
	        
	    diffOnsetNote = Note(frequency=493.88, onset=40.0, duration=Duration.QUARTER, pitch=samePitch)
	    sameNote.setPitch(samePitch)
	    self.assertTrue(note.noteEqual(diffOnsetNote)) # changed from assertFalse because notes with different onsets should still be the same note

	    diffDurationNote = Note(frequency=493.88, onset=0.0, duration=Duration.EIGHTH, pitch=samePitch)
	    sameNote.setPitch(samePitch)
	    self.assertFalse(note.noteEqual(diffDurationNote))

	    rest = Pitch (letter='r')
	    restNote = Note(frequency=0, onset=0.0)
	    note.setPitch(rest)

	    samerest = Pitch (letter='r')
	    samerestNote = Note(frequency=0, onset=0.0)
	    note.setPitch(samerest)
	    self.assertTrue(samerestNote.noteEqual(samerestNote))

	# This test is unnecessary because we do not need to read Frequencies from MIDI files to compute note pitches.
	# This instead will be needed for iteration 2 with audio files.
	# def testComputeFrequency(self):
	# 	# check frequencies are calculated correctly from computeFrequency
	# 	# import midi file: first 3 notes of C major scale as all quarter notes (refer to TestComputePitches)
	# 	# Use Python MIDI library https://github.com/vishnubob/python-midi
	# 	# MIDI files are an array of integers with a header
	# 	TuneMIDI = midi.read_midifile("../tests/MIDITestFiles/c-major-scale-treble.mid")
	# 	frequencies = [261.63, 293.66, 329.63]
	# 	# check frequencies and onsets calculated correctly from generateTune
	# 	for i in xrange(0, 3):
	# 		self.assertEqual(readFrequency(), frequencies[i])

	def testcomputeOnset(self):
		# check onsets are calculated correctly from computeOnset
		TuneMIDI = midi.read_midifile("../tests/MIDITestFiles/c-major-scale-treble.mid")
		for i in xrange(0, 3):
			self.assertEqual(computeOnset(TuneMIDI[i]), i)

	def testcreateTune(self):
		# --- tests if MIDI files are successfully converted to a Tune object ---
		# import midi file: C major scale with all quarter notes (refer to TestComputePitches)
		# Use Python MIDI library https://github.com/vishnubob/python-midi
		# MIDI files are an array of integers with a header
		TuneMIDI = midi.read_midifile("../tests/MIDITestFiles/c-major-scale-treble.mid")
		# ---- Fail Tune Parameter Constraints ---
		self.assertFalse(Tune("wrongFileType.txt"), Clef.TREBLE, "", [""])
		#  timeSignature has to be (int, int) where int > 0
		self.assertFalse(Tune(TuneMIDI), (-1, 0), Clef.BASS, "Title", ["Contributor"])
		self.assertFalse(Tune(TuneMIDI, (2.5, 3), Clef.BASS, "Title", ["Contributor"]))
		tune = Tune(TuneMIDI, (3,4), Clef.TREBLE, "Title", ["Contributor"])
		# --- test Tune setters and getters ---
		# If bad input, leave field unchanged
		tune.setTimeSignature((4,4))
		self.assertEqual(tune.getTimeSignature(), (4,4))
		tune.setTimeSignature((-1, 0))
		self.assertEqual(tune.getTimeSignature(), (4,4))
		tune.setTitle("new title")
		self.assertEqual(tune.getTitle(), "new title")
		tune.setTitle("this is toooooooooooooooooooooooooooooooooooooooooooo long title")
		self.assertEqual(tune.getTitle(), "new title")
		tune.setContributors(["person1, person2, person3"])
		self.assertEqual(tune.getContributors(), ["person1, person2, person3"])
		tune.setContributors(["this is tooooooooooooooooooooooooooooooooo long contributor name"])
		self.assertEqual(tune.getContributors(), ["person1, person2, person3"])

		frequencies = [261.63, 293.66, 329.63]
		# check frequencies and onsets calculated correctly from generateTune
		for i in xrange(0, 3):
			self.assertEqual(tune[i].getFrequency(), frequencies[i])
			self.assertEqual(tune[i].getOnset(), i)
			self.assertTrue(samerest.noteEqual(samerestNote))
		
	# This test is unnecessary because we do not need to read Frequencies from MIDI files to compute note pitches.
	# This instead will be needed for iteration 2 with audio files.
	# def testcomputeFrequency(self):
	# 	# check frequencies are calculated correctly from computeFrequency
		
	# 	# import midi file: first 3 notes of C major scale as all quarter notes (refer to TestComputePitches)
	# 	# Use Python MIDI library https://github.com/vishnubob/python-midi
	# 	# MIDI files are an array of integers with a header
	# 	TuneMIDI = midi.read_midifile("../tests/MIDITestFiles/c-major-scale-treble.mid")
		
	# 	frequencies = [261.63, 293.66, 329.63]
	# 	# check frequencies and onsets calculated correctly from generateTune
	# 	for i in xrange(0, 3):
	# 		self.assertEqual(readFrequency(TuneMIDI[i]), frequencies[i])
		
	def testcomputeOnset(self):
		# check onsets are calculated correctly from computeOnset
		TuneMIDI = Tune.TuneWrapper("../tests/MIDITestFiles/c-major-scale-treble.mid")
		for i in xrange(0, 3):
			self.assertEqual(round(TuneMIDI.getEventsList()[i].onset), i)
		
	def testcreateTune(self):
		# --- tests if MIDI files are successfully converted to a Tune object ---
		
		# import midi file: C major scale with all quarter notes (refer to TestComputePitches)
		# Use Python MIDI library https://github.com/vishnubob/python-midi
		# MIDI files are an array of integers with a header
		TuneMIDI = Tune.TuneWrapper("../tests/MIDITestFiles/c-major-scale-treble.mid")
		
		# ---- Fail Tune Parameter Constraints ---
		self.assertTrue(Tune(midi = "wrongFileType.txt").midifile == None)
		# ---- Pass Tune Parameter Constraints ---
		self.assertFalse(Tune(midi = "wrongFileType.mp3").midifile == None)

		#  timeSignature has to be (int, int) where int > 0
		self.assertTrue(Tune(timeSignature = (-1, 0)).timeSignature == (4,4))
		self.assertTrue(Tune(timeSignature = (2.5, 3)).timeSignature == (4,4))
			
		# --- test Tune setters and getters ---
		# If bad input, leave field unchanged
		TuneMIDI.setTimeSignature((4,4))
		self.assertEqual(TuneMIDI.getTimeSignature(), (4,4))
		TuneMIDI.setTimeSignature((-1, 0))
		self.assertEqual(TuneMIDI.getTimeSignature(), (4,4))
		TuneMIDI.setTitle("new title")
		self.assertEqual(TuneMIDI.getTitle(), "new title")
		TuneMIDI.setTitle("this is toooooooooooooooooooooooooooooooooooooooooooo long title")
		self.assertEqual(TuneMIDI.getTitle(), "new title")
		TuneMIDI.setContributors(["person1, person2, person3"])
		self.assertEqual(TuneMIDI.getContributors(), ["person1, person2, person3"])
		TuneMIDI.setContributors(["this is toooooooooooooooooooooooooooooooooooooooooooooooooo long contributor name"])
		self.assertEqual(TuneMIDI.getContributors(), [])
		
	def testcalculateRests(self):
		tune = Tune()
		PitchC = Pitch (letter='b', octave=4, accidental=Accidental.NATURAL)
					
		q1_C4 = Note(frequency=261.63, onset=0, s_duration=1.0, duration=Duration.QUARTER, pitch=PitchC)
		q_rest = Pitch (letter='r')
		q_restNote = Note(frequency=0, onset=0.0, s_duration=1.0, duration=Duration.QUARTER)
		q_restNote.setPitch(q_rest)
		q2_C4 = Note(frequency=261.63, onset=2, s_duration=1.0, duration=Duration.QUARTER, pitch=PitchC)
		
		CRestC = [q1_C4, q2_C4]
		rest = tune.calculateRests([q1_C4, q2_C4])
		self.assertTrue(tune.notesListEquals(rest, CRestC))


	def testKeyEqual(self):
		pitch = Pitch(letter = 'b',accidental=Accidental.FLAT)
		key = Key(isMajor=True, pitch=Pitch(letter='b', accidental=Accidental.FLAT))
		sameKey = Key(isMajor=True, pitch=Pitch(letter='b', accidental=Accidental.FLAT))
		
		self.assertTrue(key.keyEqual(sameKey))
		
		diffLetter = Key(isMajor=True, pitch=Pitch(letter='e', accidental=Accidental.FLAT))
		diffAccidental = Key(isMajor=True, pitch=Pitch(letter='b', accidental=Accidental.NATURAL))
		diffIsMajor = Key(isMajor=False, pitch=Pitch(letter='b', accidental=Accidental.FLAT))
		
		self.assertFalse(key.keyEqual(diffLetter))
		self.assertFalse(key.keyEqual(diffAccidental))
		self.assertFalse(key.keyEqual(diffIsMajor))


	def testEventequal(self):
		note = Note(frequency=261.63,onset= 0.0)
		diffnote = Note(frequency=241.63,onset= 0.0)
		sameNote = Note(frequency=261.63,onset= 0.0)
		rest = Rest(onset=4.0)
		sameRest = Rest(onset=4.0)
		diffRest=Rest(onset=3.0)
		pitch1 = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
		pitch2 = Pitch(letter='c', octave=4, accidental=Accidental.NATURAL)
		pitch3 = Pitch(letter='a', octave=4, accidental=Accidental.FLAT)
		pitch4 = Pitch(letter='a', octave=4, accidental=Accidental.NATURAL)
		chord = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.QUARTER, onset=5.0)
		sameChord = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.QUARTER, onset=5.0)
		diffChord = Chord(pitches=[pitch1,pitch2,pitch4],duration=Duration.QUARTER, onset=5.0)

		# self.assertTrue(note.eventEqual(sameNote))
		# self.assertTrue(rest.eventEqual(sameRest))
		# self.assertTrue(chord.eventEqual(sameChord))

		# self.assetFalse(note.eventEqual(rest))
		# self.assetFalse(note.eventEqual(chord))
		# self.assetFalse(note.eventEqual(diffNote))
		# self.assetFalse(rest.eventEqual(diffRest))
		# self.assetFalse(chord.eventEqual(diffChord))
		self.assertTrue(Event.eventEqual(sameNote))
		self.assertTrue(Event.eventEqual(sameRest))
		self.assertTrue(Event.eventEqual(sameChord))

		self.assetFalse(Event.eventEqual(rest))
		self.assetFalse(Event.eventEqual(chord))
		self.assetFalse(Event.eventEqual(diffNote))
		self.assetFalse(Event.eventEqual(diffRest))
		self.assetFalse(Event.eventEqual(diffChord))



	def testeventsListEquals(self):
		event1 = Note(frequency=261.63,onset= 0.0)
		event2 = Note(frequency=293.66,onset= 1.0)
		event3 = Note(frequency=329.63,onset= 2.0)
		event4 = Note(frequency=349.23,onset= 3.0)
		event5 = Rest(onset=4.0)
		pitch1 = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
		pitch2 = Pitch(letter='c', octave=4, accidental=Accidental.NATURAL)
		pitch3 = Pitch(letter='a', octave=4, accidental=Accidental.FLAT)
		event6 = Chord(pitches=[pitch1,pitch2,pitch3],duration=Duration.QUARTER, onset=5.0)

		events = [event1, event2, event3, event4, event5, event6]

		sameevent1 = Note(frequency= 261.63,onset= 0.0)
		sameevent2 = Note(frequency= 293.66,onset= 1.0)
		sameevent3 = Note(frequency= 329.63,onset= 2.0)
		sameevent4 = Note(frequency= 349.23,onset= 3.0)
		sameevent5 = Rest(onset=4.0)
		spitch1 = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
		spitch2 = Pitch(letter='c', octave=4, accidental=Accidental.NATURAL)
		spitch3 = Pitch(letter='a', octave=4, accidental=Accidental.FLAT)
		sameevent6 = Chord(pitches=[spitch1,spitch2,spitch3],duration=Duration.QUARTER, onset=5.0)
		sameEvents = [sameevent1, sameevent2, sameevent3, sameevent4, sameevent5, sameevent6]
		diffOrderEvents = [sameevent1, sameevent3, sameevent4, sameevent2, sameevent5, sameevent6]
		lessEvents = [sameevent1, sameevent2, sameevent4, sameevent5, sameevent6]
		event7 = Note(frequency= 320.0,onset= 5.0)
		diffEvents = [sameevent1, sameevent2, sameevent3, sameevent4, sameevent5, sameevent6, event7]

		tune = Tune()

		tune.setNotesList(events)
		self.assertTrue(tune.eventsListEquals(tune.getNotesList(), sameEvents))
		self.assertTrue(tune.eventsListEquals(tune.getNotesList(), diffOrderEvents))
		self.assertFalse(tune.eventsListEquals(tune.getNotesList(), lessEvents))
		self.assertFalse(tune.eventsListEquals(tune.getNotesList(), diffEvents))

	def testNotesListToChords(self):
		event1 = Note(frequency=261.63,onset= 0.0)
		event2 = Note(frequency=293.66,onset= 1.0)
		event3 = Note(frequency=329.63,onset= 2.0)
		event4 = Note(frequency=349.23,onset= 3.0)
		event5 = Rest(onset=4.0)
		event6 = Note(pitch=Pitch(letter='b', octave=4, accidental=Accidental.FLAT), onset=5.0,duration=Duration.QUARTER)
		event7 = Note(pitch=Pitch(letter='c', octave=4, accidental=Accidental.NATURAL), onset=5.0,duration=Duration.QUARTER)
		event8 = Note(pitch=Pitch(letter='a', octave=4, accidental=Accidental.FLAT), onset=5.0,duration=Duration.QUARTER)

		events = [event1, event2, event3, event4, event5, event6, event7,event8]

		sameevent1 = Note(frequency= 261.63,onset= 0.0)
		sameevent2 = Note(frequency= 293.66,onset= 1.0)
		sameevent3 = Note(frequency= 329.63,onset= 2.0)
		sameevent4 = Note(frequency= 349.23,onset= 3.0)
		sameevent5 = Rest(onset=4.0)
		spitch1 = Pitch(letter='b', octave=4, accidental=Accidental.FLAT)
		spitch2 = Pitch(letter='c', octave=4, accidental=Accidental.NATURAL)
		spitch3 = Pitch(letter='a', octave=4, accidental=Accidental.FLAT)
		sameevent6 = Chord(pitches=[spitch1,spitch2,spitch3],duration=Duration.QUARTER, onset=5.0)
		sameEvents = [sameevent1, sameevent2, sameevent3, sameevent4, sameevent5, sameevent6]
		tune=Tune()

		self.assertTrue(tune.eventsListEquals(tune.noteListToChords(events), sameEvents))
		self.assertFalse(tune.eventsListEquals(tune.noteListToChords(events), events))


	def testTuneGetterSetter(self):
		pitch = Pitch(letter='b', accidental=Accidental.FLAT)
		key = Key(isMajor=True, pitch=pitch)
		tune = Tune()
		tune.setKey(key)
		
		expectedKey = Key(isMajor=True, pitch=Pitch(letter='b', accidental=Accidental.FLAT))
		
		self.assertTrue(tune.getKey().keyEqual(expectedKey))

	def testTunetoJSON(self):
		tune = Tune.TuneWrapper("../tests/MIDITestFiles/tune-with-chord-rest-note.mid")

	def testJSONtoTune(self):
		# Test a tune with two notes
		tune = Tune.JSONtoTune("../tests/MIDITestFiles/tune.json")
		tune_keysig = tune.getKey()
		tune_keysig_pitch = Pitch(letter="b", octave=2, accidental=Accidental.FLAT)
		tune_keysig_key = Key(isMajor=True, pitch=tune_keysig_pitch)
		self.assertTrue(isinstance(tune_keysig, Key))
		self.assertTrue(tune_keysig.keyEqual(tune_keysig_key))

		tune_title = tune.getTitle()
		self.assertEqual(tune_title, "tune title!")

		tune_contributors = tune.getContributors()
		self.assertEqual(len(tune_contributors), 2)
		self.assertEqual(tune_contributors[0], "contributor one")
		self.assertEqual(tune_contributors[1], "contributor two")

		tune_timeSignature = tune.getTimeSignature()
		self.assertEqual(tune_timeSignature, (3, 4))

		self.assertEqual(tune.clef, Clef.TREBLE)

		tune_events = tune.getEventsList()
		pitch1 = Pitch(letter='b', octave=2, accidental=2)
		note1 = Note(duration=Duration.QUARTER, frequency=25.0, onset=5.67, pitch=pitch1)
		pitch2 = Pitch(letter='r')
		note2 = Note(duration=Duration.WHOLE, frequency=105.0, onset=6.67, pitch=pitch2)
		self.assertTrue(note.eventEqual(tune_events[0]))
		self.assertTrue(note.eventEqual(tune_events[1]))

if __name__ == '__main__':
	unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestImpromptuBackend)
	unittest.TextTestRunner(verbosity=3).run(suite)
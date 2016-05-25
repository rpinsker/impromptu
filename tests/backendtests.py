import unittest
import midi
import sys
sys.path.insert(0, '../src')
import os 
from Tune import *


#Please refer to class diagram for reference on parameter values for constructors and methods
class TestImpromptuBackend(unittest.TestCase):

	def testChordEqual(self):
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


	def testPitchEqual(self):
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
		print pitch, note.getPitch()[0]
		self.assertTrue(pitch.pitchEqual(note.getPitch()[0]))

	def testIsRest(self):
		#Testing rest
		rest = Rest()
		self.assertTrue(rest.isRest())
		
		#testing note
		notePitch = Pitch(letter='b', octave=4, accidental=Accidental.NATURAL)
		note = Note(pitch = notePitch)
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
		# noteEqual does not compare against different frequencies
		self.assertTrue(note.noteEqual(diffFreqNote))

		diffOnsetNote = Note(frequency=493.88, onset=40.0, duration=Duration.QUARTER, pitch=samePitch)
		sameNote.setPitch(samePitch)
		self.assertTrue(note.noteEqual(diffOnsetNote)) # changed from assertFalse because notes with different onsets should still be the same note

		diffDurationNote = Note(frequency=493.88, onset=0.0, duration=Duration.EIGHTH, pitch=samePitch)
		sameNote.setPitch(samePitch)
		self.assertFalse(note.noteEqual(diffDurationNote))

		restNote = Rest(onset=0, pitch = 'r')
		samerestNote = Rest(onset=0.0)
		self.assertTrue(restNote.eventEqual(samerestNote))
		
		notePitch = Pitch(letter='b', octave=4, accidental=Accidental.NATURAL)
		note = Note(frequency=493.88, onset=0.0, duration=Duration.QUARTER, pitch=notePitch)

		samePitch = Pitch (letter='b', octave=4, accidental=Accidental.NATURAL)
		sameNote = Note(frequency=493.88, onset=0.0, duration=Duration.QUARTER, pitch=samePitch)
		self.assertTrue(note.noteEqual(sameNote))


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
		# print "RUNNING: testcomputeOnset ..."
		# check onsets are calculated correctly from computeOnset
		TuneMIDI = Tune.TuneWrapper("../tests/MIDITestFiles/c-major-scale-treble.mid")
		for i in xrange(0, 15):
			self.assertEqual(round(TuneMIDI.getEventsList()[i].onset, 5), round(i*0.50505, 5))

	def testcreateTunefromMIDI(self):
		# --- tests if MIDI files are successfully converted to a Tune object ---
		
		# ---- Fail Tune Parameter Constraints ---
		self.assertTrue(Tune(midi = "wrongFileType.txt").midifile == None)
		# ---- Pass Tune Parameter Constraints ---
		self.assertFalse(Tune(midi = "../tests/MIDITestFiles/c-major-scale-treble.mid").midifile == None)

		# import midi file: C major scale with all quarter notes (refer to TestComputePitches)
		# Use Python MIDI library https://github.com/vishnubob/python-midi
		# MIDI files are an array of integers with a header
		TuneMIDI = Tune.TuneWrapper("../tests/MIDITestFiles/c-major-scale-treble.mid")
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
		
		# frequencies = [261.63, 293.66, 329.63]
		# # check frequencies and onsets calculated correctly from generateTune
		# for i in xrange(0, 3):
		# 	self.assertEqual(TuneMIDI.get[i].getFrequency(), frequencies[i])
		# 	self.assertEqual(tune[i].getOnset(), i)

    #These functions weren't written and are not necessary for execution 
    # because we didn't need the frequency attribute
#	def testeventsListEquals(self):
# 		note1 = Note(frequency = 261.63, onset = 0.0)
# 		note2 = Note( frequency = 293.66, onset = 1.0)
# 		note3 = Note(frequency = 329.63, onset = 2.0)
# 		note4 = Note(frequency = 349.23, onset = 3.0)
		
# 		notes = [note1, note2, note3, note4]
		
# 		samenote1 = Note( frequency = 261.63, onset =  0.0)
# 		samenote2 = Note( frequency = 293.66, onset = 1.0)
# 		samenote3 = Note( frequency = 329.63, onset = 2.0)
# 		samenote4 = Note( frequency = 349.23, onset = 3.0)
		
# 		sameNotes = [samenote1, samenote2, samenote3, samenote4]
		
# 		midifile = "../tests/MIDITestFiles/c-major-scale-treble.mid"
# 		tune = Tune(midi = midifile, timeSignature = (4, 4), clef = Clef.TREBLE, titel = "firstTune", contributor = ["me", "you"])
		
# 		self.assertTrue(tune.eventsListEquals(notes,sameNotes))
		
# 		diffNote3 = Note( frequency = 300.0, onset =  2.0)
# 		diff3rdNote = [samenote1, samenote2, diffNote3, samenote4]
# 		self.assertFalse(tune.eventsListEquals(notes,diff3rdNote))
		
# 		diffNoteOrder = [samenote1, samenote3, samenote2, samenote4]
# 		self.assertFalse(tune.eventsListEquals(notes,diffNoteOrder))
#		note1 = Note( 261.63, 0.0)
#		note2 = Note( 293.66, 1.0)
#		note3 = Note(329.63, 2.0)
#		note4 = Note(349.23, 3.0)
#		
#		notes = [note1, note2, note3, note4]
#		
#		samenote1 = Note( 261.63, 0.0)
#		samenote2 = Note( 293.66, 1.0)
#		samenote3 = Note( 329.63, 2.0)
#		samenote4 = Note( 349.23, 3.0)
#		
#		sameNotes = [samenote1, samenote2, samenote3, samenote4]
#		
#		midifile = midi.read_midifile("miditest.midi")
#		tune = Tune(midifile, (4, 4), treble, "firstTune", ["me", "you"])
#		
#		self.assertTrue(tune.eventsListEquals(notes,sameNotes))
#		
#		diffNote3 = Note( 300.0, 2.0)
#		diff3rdNote = [samenote1, samenote2, diffNote3, samenote4]
#		self.assertFalse(tune.eventsListEquals(notes,diff3rdNote))
#		
#		diffNoteOrder = [samenote1, samenote3, samenote2, samenote4]
#		self.assertFalse(tune.eventsListEquals(notes,diffNoteOrder))
#
#
#	def testNotesListGetterSetter(self):
#		note1 = Note(frequency=261.63,onset= 0.0)
#		note2 = Note(frequency=293.66,onset= 1.0)
#		note3 = Note(frequency=329.63,onset= 2.0)
#		note4 = Note(frequency=349.23,onset= 3.0)
#		
#		notes = [note1, note2, note3, note4]
#		
#		samenote1 = Note(frequency= 261.63,onset= 0.0)
#		samenote2 = Note(frequency= 293.66,onset= 1.0)
#		samenote3 = Note(frequency= 329.63,onset= 2.0)
#		samenote4 = Note(frequency= 349.23,onset= 3.0)
#		
#		sameNotes = [samenote1, samenote2, samenote3, samenote4]
#		
#		tune = Tune()
#		
#		tune.setNotesList(notes)
#		self.assertTrue(tune.eventsListEquals(tune.getNotesList(), sameNotes))

	# This test is unnecessary because we do not need to covert frequencies from MIDI files to compute note pitches.
	# This instead will be needed for iteration 2 with audio files.
	# def testComputeNotes(self):
	# 	tune = Tune((4, 4), Clef.TREBLE, "title1", ["a", "b"])
		
	# 	#testing C major scale with all quarter notes
	# 	q_C4 = Note(261.63, 0)
	# 	q_D4 = Note(293.66, 1)
	# 	q_E4 = Note(329.63, 2)
	# 	q_F4 = Note(349.23, 3)
	# 	q_G4 = Note(392.00, 4)
	# 	q_A4 = Note(440.00, 5)
	# 	q_B4 = Note(493.88, 6)
	# 	q_C5 = Note(523.25, 7)
	# 	CMajor1 = [q_C4, q_D4, q_E4, q_F4, q_G4, q_A4, q_B4, q_C5]
	# 	CMajor1_notes = tune.computeNotes(CMajor1)
	# 	self.assertTrue(tune.eventsListEquals(CMajor1, CMajor1_notes))
		
	# 	#testing for C major scale of different note lengths
	# 	w_C4 = Note(261.63, 0)
	# 	h_D4 = Note(293.66, 4)
	# 	q_E4 = Note(329.63, 6)
	# 	e_F4 = Note(349.23, 7)
	# 	s_G4 = Note(392.00, 7.5)
	# 	e_A4 = Note(440.00, 7.75)
	# 	q_B4 = Note(493.88, 8.25)
	# 	h_C5 = Note(523.25, 9.25)
	# 	CMajor2 = [w_C4, h_D4, q_E4, e_F4, s_G4, e_A4, q_B4, h_C5]
	# 	CMajor2_notes = tune.computeNotes(CMajor2)
	# 	self.assertTrue(tune.eventsListEquals(CMajor2, CMajor2_notes))
	# 	self.assertFalse(tune.eventsListEquals(CMajor2, CMajor1))

	# aubio does this functionality for us
	# def testExtractOnset(self):
	# 	# mp3 file with 8 note onsets at 0, 2, 3, ..., 7
	# 	mp3Onset = Tune.extractOnset("../tests/MP3TestFiles/c-major-scale-treble.mp3")
	# 	for i in range(0, 8):
	# 		self.assertEqual(mp3Onset[i], i)

	# aubio does this functionality for us
	# def testExtractDuration(self):
	# 	# mp3 file with 8 note durations, each a quarter note long

	# 	# first get duration in seconds
	# 	mp3Duration = Tune.extract_s_Duration("../tests/MP3TestFiles/c-major-scale-treble.mp3")
	# 	# convert to duration enum
	# 	for i in xrange(0, 8):
	# 		mp3Duration[i] = Tune.secondsToDuration(mp3Duration[i])
	# 		self.assertEqual(mp3Duration[i], Duration.QUARTER)

	def testFrequencyEqual(self):
		# equal
		self.assertTrue(Note.frequencyEqual(360, 360))
		# in range
		self.assertTrue(Note.frequencyEqual(363, 360))
		# out of range
		self.assertFalse(Note.frequencyEqual(365, 360))
		# frequency out of lower bound 20
		self.assertFalse(Note.frequencyEqual(19, 18))
		# frequency out of upper bound 4200
		self.assertFalse(Note.frequencyEqual(4201, 4201))

	# aubio does this functionality for us
	# def testExtractFrequency(self):
	# 	# mp3 file of c major chord on treble clef
	# 	mp3Frequency = Tune.extractFrequency("../tests/MP3TestFiles/c-major-scale-treble.mp3")
	# 	# refer to http://www.phy.mtu.edu/~suits/notefreqs.html
	# 	frequency = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
	# 	for i in xrange(0, 8):
	# 		self.assertTrue(Note.frequencyEqual(mp3Frequency[i], frequency[i]))

	def testComputePitchFromFrequency(self):
		# mp3 file of c major chord on treble clef
		mp3Pitch = Tune.convertFreqToPitch([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25])
		pitchC = Pitch(letter='c', octave=4, accidental=Accidental.NATURAL)
		pitchD = Pitch(letter='D', octave=4, accidental=Accidental.NATURAL)
		pitchE = Pitch(letter='E', octave=4, accidental=Accidental.NATURAL)
		pitchF = Pitch(letter='F', octave=4, accidental=Accidental.NATURAL)
		pitchG = Pitch(letter='G', octave=4, accidental=Accidental.NATURAL)
		pitchA = Pitch(letter='A', octave=4, accidental=Accidental.NATURAL)
		pitchB = Pitch(letter='B', octave=4, accidental=Accidental.NATURAL)
		pitchC5 = Pitch(letter='C', octave=5, accidental=Accidental.NATURAL)

		pitchList = [pitchC, pitchD, pitchE, pitchF, pitchG, pitchA, pitchB, pitchC5]
		for i in xrange(0, 8):
			self.assertTrue(pitchList[i].pitchEqual(mp3Pitch[i]))

#Support one-track/single-instrument mp3 audio file by generating Tune object directly from audio file
	def testcreateTunefromWav(self):
		# --- tests if MP3 files are successfully converted to a Tune object ---
		
		# import wav file: C major scale with all quarter notes (refer to TestComputePitches)


		TuneWAV = Tune.TuneWrapper("../tests/WAVTestFiles/eqt-chromo-sc.wav")
		
	def testcomputeOnset(self):
		# check onsets are calculated correctly from computeOnset
		TuneMIDI = Tune.TuneWrapper("../tests/MIDITestFiles/c-major-scale-treble.mid")
		for i in xrange(0, 15):
			self.assertEqual(round(TuneMIDI.getEventsList()[i].onset, 5), round(i*0.50505, 5))
				
	def testcalculateRests(self):
		tune = Tune()
		PitchC = Pitch (letter='b', octave=4, accidental=Accidental.NATURAL)
					
		q1_C4 = Note(frequency=261.63, onset=0, s_duration=1.0, duration=Duration.QUARTER, pitch=PitchC)
		q_restNote = Rest(frequency=0, onset=1.0, s_duration=1.0, duration=Duration.QUARTER)
		q2_C4 = Note(frequency=261.63, onset=2, s_duration=1.0, duration=Duration.QUARTER, pitch=PitchC)
		
		CRestC = [q1_C4, q_restNote, q2_C4]
		# rest = tune.calculateRests([q1_C4, q2_C4])

		# self.assertTrue(tune.eventsListEquals(rest, CRestC))
		# self.assertFalse(tune.eventsListEquals(rest, [q1_C4, q2_C4]))

		tune.setEventsList(tune.calculateRests([q1_C4, q2_C4]))

		self.assertTrue(tune.eventsListEquals(CRestC))
		self.assertFalse(tune.eventsListEquals([q1_C4, q2_C4]))

    #self.assertFalse(tune.eventsListEquals(rest, [q1_C4, q2_C4]))

	# We put computeNoteOrder functionality into the calculateRests method so this 
	# test is not relevant 		
#	def testcomputeNoteOrderTest(self):
#		#testing notes with no rests
#		t1note1 = Note(frequency = 261.63, onset = 0.0)
#		t1note2 = Note( frequency = 293.66,onset =  1.0)
#		t1note3 = Note( frequency = 329.63, onset = 2.0)
#		t1note4 = Note( frequency = 349.23,onset =  3.0)
#		t1notes = [t1note2,t1note3,t1note1,t1note4]
#		t1notesOrdered = computeNoteOrder(t1notes, [])
#		t1expectedNotesOrdered = [t1note1,t1note2,t1note3,t1note4]
#		
#		midifile = midi.read_midifile("miditest.midi")
#		tune = Tune(midi = midifile, timeSignature = (4,4), clef = Clef.TREBLE, title = "firstTune", contributor = ["me", "you"])
#		
#		self.assertTrue(tune.eventsListEquals(t1notesOrdered, t1expectedNotesOrdered))
#		
#		#testing notes with equal length rests
#		t21note1 = Note(frequency = 261.63,onset =  0.0)
#		t2note2 = Note(frequency = 293.66, onset = 1.0)
#		t2rest1 = Note(frequency = 0,onset =  2.0)
#		t2note3 = Note(frequency = 329.63,onset =  3.0)
#		t2note4 = Note(frequency = 349.23, onset = 4.0)
#		t2rest2 = Note(frequency = 0, onset = 5.0)
#		t2note5 = Note(frequency = 392.00,onset =  6.0)
#		t2notes = [t2note5, t2note2,t2note3,t2note1,t2note4]
#		t2rests = [t2rest2, t2rest1]
#		
#		t2notesOrdered = computeNoteOrder(t2notes, t2rests)
#		t2expectedNotesOrdered = [t2note1,t2note2,t2rest1, t2note3,t2note4, t2rest2, t2note5]
#		
#		self.assertTrue(tune.eventsListEquals(t2notesOrdered, t2expectedNotesOrdered))
#		
#		#testing notes with different length rests and notes
#		t3note1 = Note(261.63, 0.0)
#		t3rest1 = Note(0, 1.0)
#		t3note2 = Note(293.66, 3.0)
#		t3rest2 = Note(0, 3.5)
#		t3note3 = Note(329.63, 4.0)
#		t3note4 = Note(349.23, 8.0)
#		t3rest3 = Note(0, 10.0)
#		t3note5 = Note(392.00, 14.0)
#		
#		t3notes = [t3note5, t3note3, t3note2,t3note1,t3note4]
#		t3rests = [t3rest2, t3rest3m, t3rest1]
#		
#		t3notesOrdered = computeNoteOrder(t3notes, t3rests)
#		t3expectedNotesOrdered = [t3note1,t3rest1, t3note2, t3rest2, t3note3, t3note4, t3rest3, t3note5]
#		
#		self.assertTrue(tune.eventsListEquals(t3notesOrdered, t3expectedNotesOrdered))

		


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
	
	# we did not implement a tuneEquals method in the Tune class	
	# def testtuneEquals(self):
	# 	midifile = midi.read_midifile("miditest.midi")
	# 	tune = Tune(midifile, (4,4), treble, "firstTune", ["me", "you"], Key (true, Pitch('e', None, flat)))
	# 	note1 = Note( 261.63, 0.0)
	# 	note2 = Note( 293.66, 1.0)
	# 	note3 = Note( 329.63, 2.0)
	# 	note4 = Note( 349.23, 3.0)
	# 	notes = [t1note2,t1note3,t1note1,t1note4]
	# 	tune.setNotesList(notes)
		
	# 	sameMidifile = midi.read_midifile("miditest.midi")
	# 	sametune = Tune(sameMidifile, (4,4), treble, "firstTune", ["me", "you"], Key (true, Pitch('e', None, flat)))
	# 	sametune.setNotesList(notes)
	# 	self.assertTrue(tune.tuneEquals(sametune))
		
	# 	diffTimeSig = Tune(sameMidifile, (3,4), treble, "firstTune", ["me", "you"], Key (true, Pitch('e', None, flat)))
	# 	diffTimeSig.setNotesList(notes)
	# 	self.assertFalse(tune.tuneEquals(diffTimeSig))
		
	# 	diffClef = Tune(sameMidifile, (4,4), bass, "firstTune", ["me", "you"], Key (true, Pitch('e', None, flat)))
	# 	diffClef.setNotesList(notes)
	# 	self.assertFalse(tune.tuneEquals(diffClef))
		
	# 	diffName = Tune(sameMidifile, (4,4), treble, "name", ["me", "you"], Key (true, Pitch('e', None, flat)))
	# 	diffName.setNotesList(notes)
	# 	self.assertFalse(tune.tuneEquals(diffName))
		
	# 	diffCollab = Tune(sameMidifile, (4,4), treble, "firstTune", ["us", "you"], Key (true, Pitch('e', None, flat)))
	# 	diffCollab.setNotesList(notes)
	# 	self.assertFalse(tune.tuneEquals(diffCollab))
		
	# 	diffMidiFile = midi.read_midifile("diffmiditest.test")
	# 	tune = Tune(diffMidiFile, (4,4), treble, "firstTune", ["me", "you"], Key (true, Pitch('e', None, flat)))
	# 	diffMidiFile.setNotesList(notes)
	# 	self.assertFalse(tune.tuneEquals(diffMidiFile))
		
	# 	diffKey = Tune(sameMidifile, (4,4), treble, "firstTune", ["me", "you"], Key (true, Pitch('b', None, flat)))
	# 	diffKey.setNotesList(notes)
	# 	self.assertFalse(tune.tuneEquals(diffKey))
		
	# 	t2note1 = Note( 261.63, 0.0)
	# 	t2note2 = Note( 293.66, 1.0)
	# 	t2rest1 = Note( 0, 2.0)
	# 	t2note3 = Note( 329.63, 3.0)
	# 	t2note4 = Note( 349.23, 4.0)
	# 	t2rest2 = Note( 0, 5.0)
	# 	t2note5 = Note( 392.00, 6.0)
	# 	t2notes = [t2note5, t2note2,t2note3,t2note1,t2note4]
	# 	diffNotesList = Tune(sameMidifile, (4,4), treble, "firstTune", ["me", "you"])
	# 	diffNotesList.setNotes(t2note1)
	# 	self.assertFalse(tune.tuneEquals(diffNotesList))

	def testEventequal(self):
		note = Note(frequency=261.63,onset= 0.0)
		diffNote = Note(frequency=241.63,onset= 0.0)
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
		self.assertTrue(note.eventEqual(sameNote))
		self.assertTrue(rest.eventEqual(sameRest))
		self.assertTrue(chord.eventEqual(sameChord))

		self.assertFalse(rest.eventEqual(diffRest))
		self.assertFalse(chord.eventEqual(diffChord))
		self.assertFalse(note.eventEqual(diffNote))
		self.assertFalse(rest.eventEqual(diffRest))
		self.assertFalse(note.eventEqual(diffChord))

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

		tune.setEventsList(events)
		self.assertTrue(tune.eventsListEquals(sameEvents))
		self.assertFalse(tune.eventsListEquals(diffOrderEvents))
		self.assertFalse(tune.eventsListEquals(lessEvents))
		self.assertFalse(tune.eventsListEquals(diffEvents))

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
		tune=Tune(events = events)
		tune.eventListToChords()

		self.assertTrue(tune.eventsListEquals(sameEvents))
		self.assertFalse(tune.eventsListEquals(events))

	def testNotesListGetterSetter(self):
		# print "RUNNING: testNotesListGetterSetter ..."
		note1 = Note(frequency=261.63,onset= 0.0)
		note2 = Note(frequency=293.66,onset= 1.0)
		note3 = Note(frequency=329.63,onset= 2.0)
		note4 = Note(frequency=349.23,onset= 3.0)
		
		notes = [note1, note2, note3, note4]
		
		samenote1 = Note(frequency= 261.63,onset= 0.0)
		samenote2 = Note(frequency= 293.66,onset= 1.0)
		samenote3 = Note(frequency= 329.63,onset= 2.0)
		samenote4 = Note(frequency= 349.23,onset= 3.0)
		
		sameNotes = [samenote1, samenote2, samenote3, samenote4]
		
		tune = Tune()
		
		tune.setEventsList(notes)

		self.assertTrue(tune.eventsListEquals(sameNotes))

	def testTuneGetterSetter(self):
		pitch = Pitch(letter='b', accidental=Accidental.FLAT)
		key = Key(isMajor=True, pitch=pitch)
		tune = Tune()
		tune.setKey(key)
		
		expectedKey = Key(isMajor=True, pitch=Pitch(letter='b', accidental=Accidental.FLAT))
		
		self.assertTrue(tune.getKey().keyEqual(expectedKey))

	def testTunetoJSON(self):
		tune = Tune.TuneWrapper("../tests/MIDITestFiles/tune-with-chord-rest-note.mid")
		json_str = tune.TunetoJSON()
		f = open(json_str, 'r')
		l1 = f.readline()
		self.assertEqual(l1, "{\n")
		l2 = f.readline()
		self.assertEqual(l2, '\t"tune":{\n')
		l3 = f.readline()
		self.assertEqual(l3, '\t\t"timeSignature":["4","4"],\n')
		l4 = f.readline()
		self.assertEqual(l4, '\t\t"clef":"0",\n')
		l5 = f.readline()
		self.assertEqual(l5, '\t\t"title":"",\n')
		l6 = f.readline()
		self.assertEqual(l6, '\t\t"contributors":[],\n')
		l7 = f.readline()
		self.assertEqual(l7, '\t\t"events":[\n')
		l8 = f.readline()
		self.assertEqual(l8, '\t\t\t{\n')
		l9 = f.readline()
		self.assertEqual(l9, '\t\t\t\t"class":"chord",\n')
		l10 = f.readline()
		self.assertEqual(l10, '\t\t\t\t"duration":"SIXTEENTH",\n')
		l11 = f.readline()
		self.assertEqual(l11, '\t\t\t\t"s_duration":"0.136363",\n')
		l13 = f.readline()
		self.assertEqual(l13, '\t\t\t\t"onset":"0.136363",\n')
		l14 = f.readline()
		self.assertEqual(l14, '\t\t\t\t"pitches":[\n')
		l15 = f.readline()
		self.assertEqual(l15, '\t\t\t\t\t{\n')
		l16 = f.readline()
		self.assertEqual(l16, '\t\t\t\t\t"letter":"e",\n')
		l17 = f.readline()
		self.assertEqual(l17, '\t\t\t\t\t"octave":"3",\n')
		l18 = f.readline()
		self.assertEqual(l18, '\t\t\t\t\t"accidental":"0"\n')
		l19 = f.readline()
		self.assertEqual(l19, '\t\t\t\t\t},\n')
		l20 = f.readline()
		self.assertEqual(l20, '\t\t\t\t\t{\n')
		l21 = f.readline()
		self.assertEqual(l21, '\t\t\t\t\t"letter":"g",\n')
		l22 = f.readline()
		self.assertEqual(l22, '\t\t\t\t\t"octave":"3",\n')
		l23 = f.readline()
		self.assertEqual(l23, '\t\t\t\t\t"accidental":"1"\n')
		l24 = f.readline()
		self.assertEqual(l24, '\t\t\t\t\t}\n')	
		l25 = f.readline()
		self.assertEqual(l25, '\t\t\t\t]\n')
		l26 = f.readline()
		self.assertEqual(l26, '\t\t\t},\n')
		l27 = f.readline()
		self.assertEqual(l27, '\t\t\t{\n')
		l28 = f.readline()	
		self.assertEqual(l28, '\t\t\t\t"class":"rest",\n')
		l29 = f.readline()
		self.assertEqual(l29, '\t\t\t\t"duration":"QUARTER",\n')
		l30 = f.readline()
		self.assertEqual(l30, '\t\t\t\t"s_duration":"0.818181",\n')
		l32 = f.readline()
		self.assertEqual(l32, '\t\t\t\t"onset":"0.272727",\n')
		l33 = f.readline()
		self.assertEqual(l33, '\t\t\t\t"pitch":{\n')
		l34 = f.readline()
		self.assertEqual(l34, '\t\t\t\t\t"letter":"r",\n')
		l35 = f.readline()
		self.assertEqual(l35, '\t\t\t\t\t"octave":"",\n')
		l36 = f.readline()
		self.assertEqual(l36, '\t\t\t\t\t"accidental":""\n')
		l37 = f.readline()
		self.assertEqual(l37, '\t\t\t\t}\n')
		l38 = f.readline()
		self.assertEqual(l38, '\t\t\t},\n')
		l39 = f.readline()
		self.assertEqual(l39, '\t\t\t{\n')	
		l40 = f.readline()
		self.assertEqual(l40, '\t\t\t\t"class":"note",\n')
		l41 = f.readline()
		self.assertEqual(l41, '\t\t\t\t"duration":"SIXTEENTH",\n')
		l42 = f.readline()
		self.assertEqual(l42, '\t\t\t\t"s_duration":"0.136364",\n')
		l43 = f.readline()
		self.assertEqual(l43, '\t\t\t\t"frequency":"",\n')
		l44 = f.readline()
		self.assertEqual(l44, '\t\t\t\t"onset":"1.090908",\n')
		l45 = f.readline()
		self.assertEqual(l45, '\t\t\t\t"pitch":{\n')
		l46 = f.readline()
		self.assertEqual(l46, '\t\t\t\t\t"letter":"a",\n')
		l47 = f.readline()
		self.assertEqual(l47, '\t\t\t\t\t"octave":"3",\n')
		l48 = f.readline()
		self.assertEqual(l48, '\t\t\t\t\t"accidental":"0"\n')
		l49 = f.readline()
		self.assertEqual(l49, '\t\t\t\t}\n')
		l50 = f.readline()
		self.assertEqual(l50, '\t\t\t}\n')
		l51 = f.readline()
		self.assertEqual(l51, '\t\t],\n')
		l52 = f.readline()
		self.assertEqual(l52, '\t\t"keySignature":{\n')
		l53 = f.readline()
		self.assertEqual(l53, '\t\t\t"isMajor":"True",\n')
		l54 = f.readline()
		self.assertEqual(l54, '\t\t\t\t"pitch":{\n')
		l55 = f.readline()
		self.assertEqual(l55, '\t\t\t\t\t"letter":"c",\n')
		l56 = f.readline()
		self.assertEqual(l56, '\t\t\t\t\t"octave":"0",\n')
		l57 = f.readline()
		self.assertEqual(l57, '\t\t\t\t\t"accidental":"0"\n')
		l58 = f.readline()
		self.assertEqual(l58, '\t\t\t\t}\n')
		l59 = f.readline()
		self.assertEqual(l59, '\t\t}\n')
		l60 = f.readline()
		self.assertEqual(l60, '\t}\n')
		l61 = f.readline()
		self.assertEqual(l61, '}\n')


	def testJSONtoTune(self):
		# Test a tune with two notes
		tune = Tune()
		tune.JSONtoTune("../tests/MIDITestFiles/tune.json")
		tune_keysig = tune.getKey()
		tune_keysig_pitch = Pitch(letter="b", octave='', accidental=Accidental.FLAT)
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
		rest1 = Rest(duration=Duration.WHOLE, onset=6.67, pitch=pitch2)
		self.assertTrue(note1.eventEqual(tune_events[0]))
		self.assertTrue(rest1.eventEqual(tune_events[1]))

if __name__ == '__main__':
	unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestImpromptuBackend)
	unittest.TextTestRunner(verbosity=3).run(suite)

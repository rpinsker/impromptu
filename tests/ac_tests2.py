import unittest
import midi
import sys
sys.path.insert(0, '../src')
import os 
from TuneIter2 import *

class TestImpromptuBackend2(unittest.TestCase):
	def TestTunetoJSON(self):
		tune = TuneWrapper("../tests/MIDITestFiles/tune-with-chord-rest-note.mid")
		

	def TestJSONtoTune(self):
		# Test a tune with two notes
		tune = JSONtoTune("../tests/MIDITestFiles/tune.json")
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
	suite = unittest.TestLoader().loadTestsFromTestCase(TestImpromptuBackend2)
	unittest.TextTestRunner(verbosity=3).run(suite)
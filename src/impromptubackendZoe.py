'''Note(frequency, onset): Note
+ isRest(): boolean
+ freqToPitch(frequency): Pitch
+ noteEqual(Note): boolean
+ getPitch(): void
+ setPitch(Pitch): void


+ getKey(): Key
+ setKey(Key): void

+ computeNoteOrder(list<Note>, list<Note>): list<Note>


+ getPitch(): Pitch
'''
import unittest
import math

class Accidental:
    NATURAL, SHARP, FLAT = range(3)


#should refactor later to make variables private and use getters and setters instead
#should be refactored so notes that don't exist cannot be created i.e. b sharp
class Pitch(object):
    
    def __init__(self, **kwargs):
        self.letter = kwargs.get('letter', None)
        self.octave = kwargs.get('octave', None)
        self.accidental = kwargs.get('accidental', Accidental.NATURAL)


    def pitchEqual(self, p):
        equal = False
        if p.letter == self.letter:
            if p.accidental == self.accidental:
                if p.octave == self.octave:
                    equal = True
        return equal

class Key(object):
    isMajor = True
    pitch = Pitch()

    def __init__(self, isMajor, pitch):
        self.isMajor = isMajor
        self.pitch = pitch

    def keyEqual(self, k):
        equal = False
        if k.isMajor == self.isMajor:
            if Pitch.pitchEqual(self.pitch, k.pitch):
                equal = True
        return equal

class Duration(object):
    sixteenth = 0
    eighth = 1
    quarter = 2
    half = 3
    whole = 4


class Note(object):
    frequency = 0.0
    onset = 0.0
    duration = Duration.quarter
    pitch = Pitch()
    
    def __init__(self, frequency, onset):
        self.frequency = frequency
        self.onset = onset
        #duration needs to be calculated somewhere

    def noteEqual(self, n):
        equal = False
    #if math.isclose (n.frequency, self.frequency):
    #if math.isclose (n.onset, self.onset):
        if n.duration == self.duration:
            if Pitch.pitchEqual(self.pitch, n.pitch):
                equal = True
        return equal


class TestImpromptuBackend(unittest.TestCase):
    
    def testpitchequal(self):
        #Testing equality of the same note
        pitch = Pitch(**dict(letter='b', octave=4, accidental=Accidental.FLAT))
        samePitch = Pitch(**dict(letter='b', octave=4, accidental=Accidental.FLAT))
        self.assertTrue(pitch.pitchEqual(samePitch))
        
        #Testing equality of different notes
        differentLetter = Pitch(**dict(letter='c', octave=4, accidental=Accidental.FLAT))
        differentOctave = Pitch(**dict(letter='b', octave=5, accidental=Accidental.FLAT))
        differentAccidental = Pitch(**dict(letter='b', octave=4, accidental=Accidental.NATURAL))
        self.assertFalse(pitch.pitchEqual(differentLetter))
        self.assertFalse(pitch.pitchEqual(differentOctave))
        self.assertFalse(pitch.pitchEqual(differentAccidental))
    
    '''
    def pitchSetterGetterTest(self):
        pitch = Pitch(**dict(letter='b', octave=4, accidental=Accidental.FLAT))
            note = Note(493.88, 0.0)
            note.setPitch(pitch)
            self.assertTrue(pitch.pitchEqual(note.getPitch()))
'''



suite = unittest.TestLoader().loadTestsFromTestCase(TestImpromptuBackend)
unittest.TextTestRunner(verbosity=3).run(suite)


#key1 = Key(False, Pitch('a', 0, Accidental.flat))
#key2 = Key(False, Pitch('b', 0, Accidental.flat))


#print Key.keyEqual(key1, key2)

               #note1 = Note(1.7, 0.7)
               #note2 = Note(1.7, 0.7)
               #print Note.noteEqual(note1, note2)


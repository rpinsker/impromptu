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

NATURAL, SHARP, FLAT = range(3)


SIXTEENTH = (1,16)
EIGHTH = (1,8)
QUARTER = (1,4)
HALF = (1,2)
WHOLE = (1,1)

#should refactor later to make variables private and use getters and setters instead
#should be refactored so notes that don't exist cannot be created i.e. b sharp
class Pitch(object):
    
    def __init__(self, **kwargs):
        self.letter = kwargs.get('letter', None)
        self.octave = kwargs.get('octave', None)
        self.accidental = kwargs.get('accidental', NATURAL)


    def pitchEqual(self, p):
        equal = False
        if p.letter == self.letter:
            if p.accidental == self.accidental:
                if p.octave == self.octave:
                    equal = True
        return equal



class Note(object):
    def __init__(self, **kwargs):
        self.frequency = kwargs.get('frequency', None)
        self.duration = kwargs.get('duration', QUARTER)
        self.onset = kwargs.get('onset', None)
        self.pitch = kwargs.get('pitch', Pitch())
    #duration needs to be calculated somewhere
    
    def noteEqual(self, n):
        equal = False
        #if math.isclose (n.frequency, self.frequency):
        #if math.isclose (n.onset, self.onset):
        if n.duration == self.duration:
            if Pitch.pitchEqual(self.pitch, n.pitch):
                equal = True
        return equal

'''

class Key(object):
    def __init__(self, **kwargs):
        self.isMajor = kwargs.get('isMajor', True)
        self.pitch = kwargs.get('pitch', Pitch())

    def keyEqual(self, k):
        equal = False
        if k.isMajor == self.isMajor:
            p = self.pitch
            if p.pitchEqual(self.pitch, k.pitch):
                equal = True
        return equal
'''


class TestImpromptuBackend(unittest.TestCase):
    
    def testpitchequal(self):
        #Testing equality of the same note
        pitch = Pitch(letter='b', octave=4, accidental=FLAT)
        samePitch = Pitch(letter='b', octave=4, accidental=FLAT)
        self.assertTrue(pitch.pitchEqual(samePitch))
        
        #Testing equality of different notes
        differentLetter = Pitch(letter='c', octave=4, accidental=FLAT)
        differentOctave = Pitch(letter='b', octave=5, accidental=FLAT)
        differentAccidental = Pitch(letter='b', octave=4, accidental=NATURAL)
        self.assertFalse(pitch.pitchEqual(differentLetter))
        self.assertFalse(pitch.pitchEqual(differentOctave))
        self.assertFalse(pitch.pitchEqual(differentAccidental))
    
    '''

    def testKeyEqual(self):
        pitch = Pitch(letter = 'b',accidental=FLAT)
        key = Key(isMajor=True, pitch=FLAT)
        sameKey = Key(isMajor=True, pitch=Pitch(letter='b', accidental=FLAT))
        
        self.assertTrue(key.keyEqual(sameKey))
        
        diffLetter = Key(isMajor=True, pitch=Pitch(letter='e', accidental=FLAT))
        diffAccidental = Key(isMajor=True, pitch=Pitch(letter='b', accidental=NATURAL))
        diffIsMajor = Key(isMajor=True, pitch=Pitch(letter='b', accidental=FLAT))
        
        self.assertFalse(key.keyEqual(diffLetter))
        self.assertFalse(key.keyEqual(diffAccidental))
        self.assertFalse(key.keyEqual(diffIsMajor))

'''
'''
    def pitchSetterGetterTest(self):
        pitch = Pitch(**dict(letter='b', octave=4, accidental=FLAT))
            note = Note(493.88, 0.0)
            note.setPitch(pitch)
            self.assertTrue(pitch.pitchEqual(note.getPitch()))
'''



suite = unittest.TestLoader().loadTestsFromTestCase(TestImpromptuBackend)
unittest.TextTestRunner(verbosity=3).run(suite)


#key1 = Key(False, Pitch('a', 0, flat))
#key2 = Key(False, Pitch('b', 0, flat))


#print Key.keyEqual(key1, key2)

note1 = Note(frequency=1.7, onset=0.7, duration=(1,4))
note2 = Note(frequency=1.7, onset=0.7, duration= QUARTER)
note3 = Note(frequency=1.7, onset=0.7, duration=(1,16))
print Note.noteEqual(note1, note2)
print Note.noteEqual(note1, note3)


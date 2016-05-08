'''
+ isRest(): boolean
+ can do next iterfreqToPitch(frequency): Pitch


+ getKey(): Key
+ setKey(Key): void

+ computeNoteOrder(list<Note>, list<Note>): list<Note>


'''
import unittest

NATURAL, SHARP, FLAT = range(3)


SIXTEENTH = (1,16)
EIGHTH = (1,8)
QUARTER = (1,4)
HALF = (1,2)
WHOLE = (1,1)

class Helper(object):
    def floatComp(self,a,b):
        if(abs((a-b)) < 0.00005):
            return True
        else:
            return False


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
    def setPitch(self, p):
        self.pitch=p
    
    def getPitch(self):
        return self.pitch
    
    def noteEqual(self, n):
        math = Helper()
        equal = False
        if math.floatComp (n.frequency, self.frequency):
            if math.floatComp(n.onset, self.onset):
                if n.duration == self.duration:
                    if Pitch.pitchEqual(self.pitch, n.pitch):
                        equal = True
        return equal



class Key(object):
    def __init__(self, **kwargs):
        self.isMajor = kwargs.get('isMajor', True)
        self.pitch = kwargs.get('pitch', Pitch())

    def keyEqual(self, k):
        equal = False
        if k.isMajor == self.isMajor:
            if self.pitch.pitchEqual(k.pitch):
                equal = True
        return equal



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

    def testKeyEqual(self):
        pitch = Pitch(letter = 'b',accidental=FLAT)
        key = Key(isMajor=True, pitch=Pitch(letter='b', accidental=FLAT))
        sameKey = Key(isMajor=True, pitch=Pitch(letter='b', accidental=FLAT))
        
        self.assertTrue(key.keyEqual(sameKey))
        
        diffLetter = Key(isMajor=True, pitch=Pitch(letter='e', accidental=FLAT))
        diffAccidental = Key(isMajor=True, pitch=Pitch(letter='b', accidental=NATURAL))
        diffIsMajor = Key(isMajor=False, pitch=Pitch(letter='b', accidental=FLAT))
        
        self.assertFalse(key.keyEqual(diffLetter))
        self.assertFalse(key.keyEqual(diffAccidental))
        self.assertFalse(key.keyEqual(diffIsMajor))

  
    def testNoteEqual(self):
        #Testing same notes
        notePitch = Pitch(letter='b', octave=4, accidental=NATURAL)
        note = Note(frequency=493.88, onset=0.0, duration=QUARTER, pitch=notePitch)
        
        samePitch = Pitch (letter='b', octave=4, accidental=NATURAL)
        sameNote = Note(frequency=493.88, onset=0.0, duration=QUARTER, pitch=samePitch)
        self.assertTrue(note.noteEqual(sameNote))
        
        #Testing different notes
        differentPitch = Pitch (letter='c', octave=5, accidental=FLAT)
        diffPitchNote = Note(frequency=493.88, onset=0.0, duration=QUARTER, pitch=differentPitch)
        self.assertFalse(note.noteEqual(diffPitchNote))
        
        diffFreqNote = Note(frequency=350.0, onset=0.0, duration=QUARTER, pitch=samePitch)
        self.assertFalse(note.noteEqual(diffFreqNote))
        
        diffOnsetNote = Note(frequency=493.88, onset=40.0, duration=QUARTER, pitch=samePitch)
        sameNote.setPitch(samePitch)
        self.assertFalse(note.noteEqual(diffOnsetNote))
        
        diffDurationNote = Note(frequency=493.88, onset=0.0, duration=EIGHTH, pitch=samePitch)
        sameNote.setPitch(samePitch)
        self.assertFalse(note.noteEqual(diffDurationNote))
        
        rest = Pitch (letter='r')
        restNote = Note(frequency=0, onset=0.0)
        note.setPitch(rest)
        
        samerest = Pitch (letter='r')
        samerestNote = Note(frequency=0, onset=0.0)
        note.setPitch(samerest)
        self.assertTrue(samerestNote.noteEqual(samerestNote))






#
#    def pitchSetterGetterTest(self):
#        pitch = Pitch(**dict(letter='b', octave=4, accidental=FLAT))
#            note = Note(493.88, 0.0)
#            note.setPitch(pitch)
#            self.assertTrue(pitch.pitchEqual(note.getPitch()))
#
#


suite = unittest.TestLoader().loadTestsFromTestCase(TestImpromptuBackend)
unittest.TextTestRunner(verbosity=3).run(suite)



#note1 = Note(frequency=1.7, onset=0.7, duration=(1,4))
#note2 = Note(frequency=1.7, onset=0.7, duration= QUARTER)
#note3 = Note(frequency=1.7, onset=0.7, duration=(1,16))
#print Note.noteEqual(note1, note2)
#print Note.noteEqual(note1, note3)


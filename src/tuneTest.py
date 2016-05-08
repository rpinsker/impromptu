import midi
import math

class Duration(object):
    SIXTEENTH, EIGHTH, QUARTER, HALF, WHOLE = range(5)

class Clef(object):
	TREBLE, BASS = range(2)

class Accidental(object):
    NATURAL, SHARP, FLAT = range(3)

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

class Note(object):
    def __init__(self, **kwargs):
        self.frequency = kwargs.get('frequency', None)
        self.duration = kwargs.get('duration', Duration.QUARTER)
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

class Key(object):
    def __init__(self, **kwargs):
        self.isMajor = kwargs.get('isMajor', True)
        self.pitch = kwargs.get('pitch', Pitch())

    def keyEqual(self, k):
        equal = False
        if k.isMajor == self.isMajor:
            if Pitch.pitchEqual(self.pitch, k.pitch):
                equal = True
        return equal

# refer to vartec's answer at http://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
class Tune(object):
    def __init__(self, **kwargs):
        if 'midi' not in kwargs:
            print "No MIDI file"
            self.midi = None
        self.timeSignature = kwargs.get('timeSignature', (4, 4))
        note1 = Note(duration = Duration.QUARTER, pitch = Pitch(letter='a', octave=4, accidental=Accidental.SHARP))
        note2 = Note(duration = Duration.QUARTER, pitch = Pitch(letter='c', octave=4))
        self.notes = [note1, note2]
        
        self.keySignature = kwargs.get('keySignature', Key(isMajor = True, pitch = Pitch(letter='c', octave = 0)))
        self.clef = kwargs.get('clef', Clef.TREBLE)
        self.title = kwargs.get('title', 'Insert Title')
        self.contributors = kwargs.get('contributors', ['Add Contributors'])

    @classmethod
    def TuneWrapper(cls, midifile):
        return cls(midi=midifile)

tune = Tune.TuneWrapper(midi.read_midifile("c-major-scale-treble.mid")) 

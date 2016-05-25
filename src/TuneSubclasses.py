# install midi library here: https://github.com/vishnubob/python-midi/
import midi
import math
import itertools
import sys
import abc
import json
#sys.path.insert(0, '../tests/WAVTestFiles/Test1')
sys.path.insert(0, '/support/')
import os
import subprocess

class Duration(object):
    SIXTEENTH = (1,16)
    EIGHTH = (1,8)
    QUARTER = (1,4)
    HALF = (1,2)
    WHOLE = (1,1)

class Clef(object):
    TREBLE, BASS = range(2)

class Accidental(object):
    NATURAL, SHARP, FLAT = range(3)

class Helper(object):
    @staticmethod
    def floatComp(a,b, threshold):
        if(abs((a-b)) < threshold):
            return True
        else:
            return False

class Pitch(object):

    # Column index for Note Number, refer to http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
    # where C4 is 60, not 72, that is shift octaves down one
    # also refer to https://usermanuals.finalemusic.com/Finale2012Mac/Content/Finale/MIDI_Note_to_Pitch_Table.htm
    letterNotes = {0 : 'c', 1 : 'c#', 2 : 'd', 3 : 'd#', 4 : 'e', 5 : 'f', 6 : 'f#', 7 : 'g', 8 : 'g#', 9 : 'a', 10 : 'a#', 11 : 'b'}

    def __init__(self, **kwargs):
        MIDINote = kwargs.get('MIDINote', None)
        if MIDINote:
            returnPitch = self.MIDInotetoPitch(MIDINote) 
            self.letter = returnPitch.letter
            self.octave = returnPitch.octave
            self.accidental = returnPitch.accidental

        else:
            self.letter = kwargs.get('letter', None)
            if self.letter != None:
                self.letter = self.letter.lower()
            self.octave = kwargs.get('octave', None)
            self.accidental = kwargs.get('accidental', Accidental.NATURAL)

    def pitchEqual(self, p):
        if (p.letter == self.letter) and (p.accidental == self.accidental) and (p.octave == self.octave):
            return True
        return False

    def setLetter(self, letter):
        self.letter = letter

    def setOctave(self, octave):
        self.octave = octave

    def setAccidental(self, accidental):
        self.accidental = accidental

    @classmethod
    # takes a MIDI note and generates a Pitch instance (e.g. MIDI note 60 is pitch C4)
    # one to one mapping between MIDI notes and pitches on the piano
    def MIDInotetoPitch(cls, MIDIint):
        octaveTemp = int(MIDIint-12)/12
        letterTemp = cls.letterNotes.get(int(MIDIint-12)%12)
        if '#' in letterTemp:
            letterTemp = letterTemp.strip('#')
            accidentalTemp = Accidental.SHARP
        else:
            accidentalTemp = Accidental.NATURAL
        return cls(octave=octaveTemp, letter=letterTemp, accidental = accidentalTemp)

    def toString(self):
        acc = {Accidental.NATURAL: '', Accidental.SHARP: '#', Accidental.FLAT: 'Flat'}.get(self.accidental)
        return "Pitch: " + str(self.letter) + str(self.octave) + acc

class Event(object):
    def __init__(self, **kwargs):
        self.duration = kwargs.get('duration', Duration.QUARTER)
        if (kwargs.get('onset') != None) and (kwargs.get('onset') >= 0):
            self.onset = kwargs.get('onset')
        else:
            self.onset = None
        self.duration = kwargs.get('duration', Duration.QUARTER)
        # duration in seconds
        self.s_duration = kwargs.get('s_duration', None)

    @abc.abstractmethod
    def getPitch(self):
        """Method that should be implemented in subclasses."""

    def combineEvent(self, event):
        if isinstance(event, Rest):
            return self
        if isinstance(self, Chord):
            self.setPitch(self.getPitch() + event.getPitch())
            return self
        elif isinstance(self, Note):
            newChord = Chord(pitches = self.getPitch() + event.getPitch(), s_duration = self.s_duration, duration = self.duration, onset = self.onset)
            return newChord
        else: # is rest
            return event

    def eventEqual(self, event):
        if self.duration != event.duration or self.onset != event.onset:
            return False
        if type(self) == type(event):
            if isinstance(self, Chord):
                return self.chordEqual(event)
            if isinstance(self, Note):
                return self.noteEqual(event)
            else: # is rest
                return True

    def editEvent(self, event):
        if event.duration != None:
            self.duration = event.duration
        if type(self) == type(event):
            if isinstance(self, Chord) and isinstance(event, Chord):
                return self.editChord(event)
            if isinstance(self, Note) and isinstance(event, Note):
                return self.editNote(event)

    def isRest(self):
        if isinstance(self, Rest):
            return True
        return False

    def setDuration(self, duration):
        self.duration = duration

    def setOnset(self, onset):
        if onset >= 0: self.onset = onset

    @abc.abstractmethod
    def setPitch(self, pitch):
        """Method that should be implemented in subclasses."""

    @abc.abstractmethod
    def toString(self):
        """Method that should be implemented in subclasses."""

class Chord(Event):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.pitches = kwargs.get('pitches', [])
    
    def getPitch(self):
        return self.pitches

    def chordEqual(self, chord):
        if self.duration != chord.duration or self.onset != chord.onset:
            return False
        if len(chord.pitches) != len(self.pitches):
            return False
        for i in range(0, len(chord.pitches)):
            if self.pitches[i].pitchEqual(chord.pitches[i]) == False:
                return False
        return True

    def editChord(self, chord):
        if chord.getPitch != None:
            self.setPitches(chord.getPitch)

    # def addPitch(self, event):
    #     if isinstance(self, Chord):
    #         self.setPitch(self.getPitch().extend(event.getPitch()))
    #         return self
    #     elif isinstance(self, Note):
    #         return Chord(pitches = list(self.getPitch()).extend(event.getPitch), duration = self.duration, onset = self.onset)
    #     else:
    #         return event
        # print self, event
        # if self.getPitch() != None:
        #     self.setPitch()
        # else:
        #     self.setPitch(event.getPitch())
        #     print '\n\nempty chord\n\n'

    def setPitch(self, listofPitches):
        self.pitches = listofPitches

    def toString(self):
        durationstring = {Duration.SIXTEENTH: 'Sixteenth', Duration.EIGHTH: 'Eighth', Duration.QUARTER: 'Quarter', Duration.HALF: 'Half', Duration.WHOLE: 'Whole' }.get(self.duration)
        pitchstr = "Chord: Duration (seconds) - %s, Duration - %s, Onset - %s, \n" %(str(self.s_duration), durationstring, str(self.onset))
        if self.pitches != None:
            for pitch in self.pitches:
                pitchstr += '>>>>>>>' + pitch.toString() + "\n"
        else:
            pitchstr += "no pitches \n"
        return pitchstr


class Rest(Event):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
    def getPitch(self):
        return [Pitch(letter= 'r')]
    def setPitch(self, pitch):
        print "Cannot change pitch of a rest. Please delete event."
        return
    def toString(self):
        durationstring = {Duration.SIXTEENTH: 'Sixteenth', Duration.EIGHTH: 'Eighth', Duration.QUARTER: 'Quarter', Duration.HALF: 'Half', Duration.WHOLE: 'Whole' }.get(self.duration)
        return "Rest: Duration (seconds) - %s, Duration - %s, Onset - %s \n" %(str(self.s_duration), durationstring, str(self.onset))        

class Note(Event):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.pitch = kwargs.get('pitch', None)
        self.frequency = kwargs.get('frequency', None)
        if self.pitch == None and self.frequency != None:
            self.pitch = self.convertFreqToPitch(self.frequency)
    
    def getPitch(self):
        return [self.pitch]

    # wrapper constructor to create Rest Note
    @classmethod
    def Rest(cls, **kwargs):
        return cls(duration = kwargs.get('duration'), s_duration = kwargs.get('s_duration'), frequency = 0.0, onset = kwargs.get('onset'), pitch = Pitch(letter = 'r'))

    def setPitch(self, p):
        self.pitch = p

    def editNote(self, note):
        if note.pitch != None:
            self.setPitch(note.pitch)

    def toString(self):
        durationstring = {Duration.SIXTEENTH: 'Sixteenth', Duration.EIGHTH: 'Eighth', Duration.QUARTER: 'Quarter', Duration.HALF: 'Half', Duration.WHOLE: 'Whole' }.get(self.duration)
        return "Note: Freq - %s, Duration (seconds) - %s, Duration - %s, Onset - %s \n \t %s" %(str(self.frequency), str(self.s_duration), durationstring, str(self.onset), self.pitch.toString())

    def isRest(self):
        if self.pitch.letter == 'r':
            return True
        else:
            return False

    @staticmethod
    def convertFreqToPitch(freq):
        # refer to http://stackoverflow.com/questions/20730133/extracting-pitch-features-from-audio-file
        MIDINote = round(12*math.log(freq/440.0, 2) + 69)
        return Pitch(MIDINote=MIDINote)

    @staticmethod
    def frequencyEqual(freq1, freq2):
        # frequency bounded in [20, 4200] because in human hearing range
        if min(freq1, freq2) < 20 or max(freq1, freq2) > 4200:
            return False
        return Helper.floatComp(freq1, freq2, 4)

    def noteEqual(self, n):
        #if math.isclose (n.frequency, self.frequency):
        #if math.isclose (n.onset, self.onset):
        if Pitch.pitchEqual(self.pitch, n.pitch) and (self.duration == n.duration):# and (self.onset == n.onset):
            return True
        return False

    def isRest(self):
        if self.getPitch()[0].letter == 'r':
            return True
        return False

class Key(object):
    def __init__(self, **kwargs):
        self.isMajor = kwargs.get('isMajor', True)
        self.pitch = kwargs.get('pitch', Pitch())

    def keyEqual(self, k):
        if (k.isMajor == self.isMajor) and Pitch.pitchEqual(self.pitch, k.pitch):
            return True
        return False

    def toString(self):
        buf = 'Key Signature - %s ' %(self.pitch.toString())
        if (self.isMajor):
            buf = buf + 'Major'
        else:
            buf = buf + 'Minor'
        return buf

# install midi library here: https://github.com/vishnubob/python-midi/
import midi
import math
import itertools
# from tuneTest import *

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
    def floatComp(self,a,b):
        if(abs((a-b)) < 0.00005):
            return True
        else:
            return False

#should refactor later to make variables private and use getters and setters instead
#should be refactored so notes that don't exist cannot be created i.e. b sharp
class Pitch(object):

    # Column index for Note Number, refer to http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
    # where C4 is 60, not 72, that is shift octaves down one
    # also refer to https://usermanuals.finalemusic.com/Finale2012Mac/Content/Finale/MIDI_Note_to_Pitch_Table.htm
    letterNotes = {0 : 'c', 1 : 'c#', 2 : 'd', 3 : 'd#', 4 : 'e', 5 : 'f', 6 : 'f#', 7 : 'g', 8 : 'g#', 9 : 'a', 10 : 'a#', 11 : 'b'}

    def __init__(self, **kwargs):
        self.letter = kwargs.get('letter', None)
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
    def MIDInotetoPitch(cls, MIDIint):
        octaveTemp = int(MIDIint-12)/12
        letterTemp = cls.letterNotes.get(int(MIDIint-12)%12)
        if '#' in letterTemp:
            letterTemp = letterTemp.strip('#')
            accidentalTemp = Accidental.SHARP
        else:
            accidentalTemp = Accidental.NATURAL
        print letterTemp, octaveTemp, accidentalTemp
        return cls(octave=octaveTemp, letter=letterTemp, accidental = accidentalTemp)

    def PitchtoString(self):
        acc = {Accidental.NATURAL: '', Accidental.SHARP: '#', Accidental.FLAT: 'Flat'}.get(self.accidental)
        return "Pitch: " + str(self.letter) + str(self.octave) + acc

# Should have Rest as subclass
class Note(object):

    def __init__(self, **kwargs):
        # second argument to get is default value
        self.frequency = kwargs.get('frequency', None)
        self.duration = kwargs.get('duration', Duration.QUARTER)
        self.onset = kwargs.get('onset', None)
        self.pitch = kwargs.get('pitch', Pitch())
    
    # wrapper constructor to create Rest Note
    @classmethod
    def Rest(cls, **kwargs):
        return cls(duration = kwargs.get('duration'), frequency = 0.0, onset = kwargs.get('onset'), pitch = Pitch(letter = 'r'))

    def setDuration(self, d):
        self.duration = d

    def setOnset(self, o):
        self.onset = o

    def setPitch(self, p):
        self.pitch = p
    
    def getPitch(self):
        return self.pitch

    def NotetoString(self):
        return "Note: Freq - %s, Duration - %s, Onset - %s \n \t %s" %(str(self.frequency), str(self.duration), str(self.onset), self.pitch.PitchtoString())

    def isRest(self):
        if self.pitch.letter == 'r':
            return True
        else:
            return False

    # def noteEqual(self, n):
    #     math = Helper()
    #     equal = False
    #     if math.floatComp (n.frequency, self.frequency):
    #         if math.floatComp(n.onset, self.onset):
    #             if n.duration == self.duration:
    #                 if Pitch.pitchEqual(self.pitch, n.pitch):
    #                     equal = True

    def noteEqual(self, n):
        #if math.isclose (n.frequency, self.frequency):
        #if math.isclose (n.onset, self.onset):
        if (n.duration == self.duration) and Pitch.pitchEqual(self.pitch, n.pitch):
            return True
        return False

    def isRest(self):
        if self.pitch.letter == 'r':
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

# refer to vartec's answer at http://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
class Tune(object):

    def __init__(self, **kwargs):
        self.timeSignature = (4,4) # default time Signature
        self.keySignature = kwargs.get('keySignature', Key(isMajor = True, pitch = Pitch(letter='c', octave = 0)))
        self.clef = kwargs.get('clef', Clef.TREBLE)
        self.title = kwargs.get('title', 'Insert Title')
        self.contributors = kwargs.get('contributors', ['Add Contributors'])
        self.midifile = kwargs.get('midi')
        if self.midifile != None: # midi file passed as parameter
            pattern = midi.read_midifile(self.midifile)
            for event in pattern[0]: # looking through midi header
                if isinstance(event, midi.TimeSignatureEvent):
                # [nn dd cc bb] refer to http://www.blitter.com/~russtopia/MIDI/~jglatt/tech/midifile/time.htm
                    self.timeSignature = (event.data[0], 2<<event.data[1])
            # override time sig in MIDI file
            if 'timeSignature' in kwargs:
                self.timeSignature = kwargs.get('timeSignature')
            # first compute onset of Notes to construct list of Notes
            self.notes = self.computeOnset(self.midifile)
            # then compute pitches of Notes
            i = 0
            for track in pattern:
                for event in track: # looking through first track
                    if isinstance(event, midi.NoteOnEvent):
                        self.notes[i].setPitch(Pitch.MIDInotetoPitch(event.get_pitch()))
                        i += 1

            self.notes = self.calculateRests(self.notes)

        
    # wrapper constructor with only MIDI file as parameter
    @classmethod
    def TuneWrapper(cls, midifile):
        return cls(midi=midifile)

    def getKey(self):
        return self.keySignature

    def setKey(self, k):
        self.keySignature = k

    def setNotesList(self, lst):
        self.notes = lst

    def getNotesList(self):
        return self.notes

    # turns ticks to time in seconds
    # The formula used is:
    # (# ticks * 60) / (BPM * resolution)
    def ticksToTime(self, ticks, bpm, resolution):
        return (ticks * 60) / (bpm * resolution)

    # takes in a duration in seconds, returns Duration enum value
    # 1 second = quarter note
    def secondsToDuration(self, dur):
        print "dur is", dur
        approx_power = math.log(1/dur, 2)
        print "approx power is", approx_power
        note_val = 4 - (round(approx_power) + 2)
        print "note_val is", note_val
        return note_val

    # Reads a MIDI file in, returns a list of Notes
    # Notes are populated with onset and duration
    # assumes a one track MIDI file with notes in chronological order
    def computeOnset(self, myfile):
        pattern = midi.read_midifile(myfile)
        NotesList = []
        index = 0
        bpm = 0
        resolution = pattern.resolution
        duration = 0
        # changes ticks to cumulative values
        pattern.make_ticks_abs() 
        for track in pattern:
            for event in track:
                if isinstance(event, midi.SetTempoEvent):
                    bpm = event.bpm
                if isinstance(event, midi.NoteEvent):
                    if (isinstance(event, midi.NoteOffEvent) or (isinstance(event, midi.NoteOnEvent) and event.data[1] == 0)):
                        endset = self.ticksToTime(event.tick, bpm, resolution)
                        currNote = NotesList[index]
                        duration = endset - currNote.onset
                        currNote.duration = self.secondsToDuration(duration)
                        index += 1
                    else:
                        onset = self.ticksToTime(event.tick, bpm, resolution)
                        # print onset
                        newNote = Note(onset = onset)
                        NotesList.append(newNote)
        return NotesList

    # Takes a list of Notes, returns a list of Notes that are rests
    def calculateRests(self, list_of_notes):
        n_notes = len(list_of_notes)
        allNotes = []
 
        ####  is duration negative?
        for i in range(0, n_notes-1):
            allNotes.append(list_of_notes[i])
            onset = list_of_notes[i].onset + list_of_notes[i].duration
            s_duration = list_of_notes[i+1].onset - onset
            duration = self.secondsToDuration(s_duration)
            rest = Note.Rest(duration=duration, onset = onset)
            allNotes.append(rest)
            if i == n_notes-2:
                allNotes.append(list_of_notes[n_notes-1])
        return allNotes

    # TO DO
    #def TunetoString(self):
    #    str = "Tune: Title - %s Contributors - %s \n\tTime Sig - %s, Key Sig - %s, Clef - " %(self.title, str(self.contributors), str(self.timeSignature), self.keySignature.KeytoString())

tune = Tune.TuneWrapper("c-major-scale-treble.mid") 
for note in tune.notes:
    print note.NotetoString()

# list_of_notes = tune.computeOnset("c-major-scale-treble.mid")
# print list_of_notes[0].NotetoString()
# list_of_rests = tune.calculateRests(list_of_notes)
# print "rests", list_of_rests
# print len(list_of_rests)
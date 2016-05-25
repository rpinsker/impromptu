from TuneSubclasses import *

# refer to vartec's answer at http://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
class Tune(object):

    def __init__(self, **kwargs):
        self.timeSignature = (4,4) # default time Signature
        self.keySignature = kwargs.get('keySignature')
        self.clef = kwargs.get('clef', Clef.TREBLE)
        # default title is midi file name
        self.title = self.setTitle(kwargs.get('title', kwargs.get('midi')))
        self.contributors = self.setContributors(kwargs.get('contributors', ['Add Contributors']))
        self.midifile = None
        self.events = kwargs.get('events')
        if kwargs.get('wav') != None and kwargs.get('wav').endswith('wav'):
            self.readWav(kwargs.get('wav'))
        elif kwargs.get('mp3') != None and kwargs.get('mp3').endswith('mp3'):
            raise NotImplementedError
        elif kwargs.get('json') != None and kwargs.get('json').endswith('json'):
            #print kwargs.get('json')
            self.JSONtoTune(kwargs.get('json'))
        elif kwargs.get('midi') != None and kwargs.get('midi').endswith('.mid'):
            self.midifile = kwargs.get('midi')
            pattern = self.MIDItoPattern(self.midifile)
            if (pattern.format!=1): # will only look at first track, don't want type 0 MIDI file has all of the channel data on one track
                print "\n***\nWARNING: Conversion of format %d MIDI files with more than one track is currently not supported and is still in development\n***\n" %(pattern.format)
            for event in pattern[0]: # looking through midi header
                if isinstance(event, midi.TimeSignatureEvent):
                # [nn dd cc bb] refer to http://www.blitter.com/~russtopia/MIDI/~jglatt/tech/midifile/time.htm
                    self.timeSignature = (event.data[0], 2<<(event.data[1] - 1))
            # override time sig in MIDI file
            if 'timeSignature' in kwargs:
                self.timeSignature = self.setTimeSignature(kwargs.get('timeSignature'))
            # first compute onset of Notes to construct list of Notes
            self.events = self.computeOnset(self.midifile)
            # then compute pitches of Notes
            i = 0
            for track in pattern:
                for event in track: # looking through first track
                    if isinstance(event, midi.NoteOnEvent):
                        self.events[i].setPitch(Pitch.MIDInotetoPitch(event.get_pitch()))
                        i += 1
            # then, insert rests
            self.events = self.calculateRests(self.events)
            # lastly, compute chords
            self.sortEventListByOnset()
            self.eventListToChords()

    # wrapper constructor with only MIDI file as parameter
    @classmethod
    def TuneWrapper(cls, file):
        if file.endswith('.mid'):
            return cls(midi=file)
        elif file.endswith('.mp3'):
            return cls(mp3=file)
        elif file.endswith('.wav'):
            return cls(wav=file)
        elif file.endswith('.json'):
            return cls(json=file)

    def getKey(self):
        return self.keySignature

    def setKey(self, k):
        self.keySignature = k

    def setTitle(self, title):
        if title != None and len(title) < 64:
            self.title = title

    def getTitle(self):
        return self.title

    def setContributors(self, cont):
        self.contributors = []
        for i in range(len(cont)):
            if len(cont[i]) <= 64:
                self.contributors.append(cont[i])

    def getContributors(self):
        return self.contributors

    def getTimeSignature(self):
        return self.timeSignature

    def setTimeSignature(self, ts):
        self.timeSignature = ts
        for i in range(2):
            if ts[i] <= 0 or isinstance(ts[i], int) == False:
                self.timeSignature = (4,4)

    def setEventsList(self, lst):
        self.events = lst

    def getEventsList(self):
        return self.events

    def sortEventListByOnset(self):
        self.events = sorted(self.events, key=lambda event: event.onset)

    def eventListToChords(self):
        newEventList = []
        prevOnset = -1
        for item in self.events:
            if item.onset != prevOnset: 
                newEventList.append(item)
                prevOnset = item.onset
            else:
                # add pitch to last event and turn to chord
                newEventList[-1] = newEventList[-1].combineEvent(item)
        self.events = newEventList

#         i = 0
#         while(i<len(self.events)-1):
#             if Helper.floatComp(self.events[i].onset,self.events[i+1].onset,0.001):
#                 # Chord, Event
#                 if isinstance(self.events[i],Chord):
#                     self.events[i].combineEvent(self.events[i+1]) #checks chords and notes
#                     self.events.pop(i+1)
#                 # Event, Chord
#                 elif isinstance(self.events[i+1],Chord):
#                     self.events[i+1].combineEvent(self.events[i]) #checks chords and notes
#                     self.events.pop(i)
#                 # Note, Note
#                 elif isinstance(self.events[i],Note) and isinstance(self.events[i+1],Note):
#                     self.events[i] = Chord(pitches = self.events[i].getPitch() + self.events[i+1].getPitch() ,duration= self.events[i].duration,onset=self.events[i].onset)
#                     self.events.pop(i+1)
#                 # Rest, Note
#                 elif isinstance(self.events[i],Rest) and isinstance(self.events[i+1],Note):
#                     self.events[i] = self.events[i+1]
#                     self.events.pop(i+1)
#                 # Note, Rest
#                 elif isinstance(self.events[i],Note) and isinstance(self.events[i+1],Rest):
#                     self.events[i+1] = self.events[i]
#                     self.events.pop(i)
#                 # Rest, Rest
#                 elif isinstance(self.events[i],Rest) and isinstance(self.events[i+1],Rest):
#                     self.events.pop(i+1)
#             else:
#                 i=i+1


    def addEvent(self, idx, event):
        self.events.insert(idx, event)

    def deleteEvent(self, idx):
        del self.events[idx]

    def editEvent(self, idx, event):
        # event contains new information (can be subset), so update original event 
        # with new info
        self.events[idx] = self.events[idx].editEvent(event)

    def eventsListEquals(self, list2):
        if len(self.getEventsList()) != len(list2):
            return False
        for i in range(0, len(list2)):
            if list2[i].eventEqual(self.getEventsList()[i]) == False:
                return False
        return True

    def durationTunetoJSON(self, tup):
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

    def writePitchtoFile(self, pitch, myfile):
        letter = ''
        octave = ''
        accidental = ''
        if pitch.letter != None:
            letter = pitch.letter
        if pitch.octave != None:
            octave = str(pitch.octave)
        if pitch.accidental != None:
            accidental = str(pitch.accidental)
        myfile.write('\t\t\t\t"pitch":{\n\t\t\t\t\t"letter":"%s",\n\t\t\t\t\t"octave":"%s",\n\t\t\t\t\t"accidental":"%s"\n\t\t\t\t}\n' %(str(letter), octave, accidental))

    def TunetoJSON(self):
        if self.title != None:
            filename = 'tune-' + self.title + '.json'
        else:
            filename = 'tune-generic.json'
        f = open(filename, 'w')
        
        f.write('{\n')
        f.write('\t"tune":{\n')
        
        f.write('\t\t"timeSignature":["%d","%d"],\n' %(self.timeSignature[0], self.timeSignature[1]))
        
        f.write('\t\t"clef":"%d",\n' %(self.clef))
        
        if self.title != None:
            f.write('\t\t"title":"%s",\n' %(self.title))
        else:
            f.write('\t\t"title":"",\n')

        f.write('\t\t"contributors":[')
        if self.contributors != None:
            n_contributors = len(self.contributors)
            if n_contributors > 0:
                for num in (0, n_contributors - 1):
                    f.write('"%s"' %(self.contributors[num]))
                    if num != n_contributors - 1:
                        f.write(',')

        f.write('],\n')

        f.write('\t\t"events":[\n')
        events = self.getEventsList()
        e_len = len(events)
        for x in range(0, e_len):
            event = events[x]
            f.write('\t\t\t{\n')
            if isinstance(event, Chord):
                f.write('\t\t\t\t"class":"chord",\n')
                if event.duration != None:
                    dur_str = self.durationTunetoJSON(event.duration)
                    f.write('\t\t\t\t"duration":"%s",\n' %(dur_str))
                else:
                    f.write('\t\t\t\t"duration":"",\n')

                if event.s_duration != None:
                    f.write('\t\t\t\t"s_duration":"%lf",\n' %(event.s_duration))
                else:
                    f.write('\t\t\t\t"s_duration":"",\n')

                f.write('\t\t\t\t"onset":"%lf",\n' %(event.onset))
                
                f.write('\t\t\t\t"pitches":[\n')
                pitches = event.getPitch()
                n_pitches = len(pitches)
                for n in range(0, n_pitches):
                    f.write('\t\t\t\t\t{\n')
                    f.write('\t\t\t\t\t"letter":"%c",\n' %(pitches[n]['letter']))
                    f.write('\t\t\t\t\t"octave":"%d",\n' %(int(pitches[n]['octave'])))
                    f.write('\t\t\t\t\t"accidental":"%d"\n' %(int(pitches[n]['accidental'])))
                    f.write('\t\t\t\t\t}')
                    if n != n_pitches-1:
                        f.write(',\n')
                    else:
                        f.write('\n')
                f.write('\t\t\t\t]\n')
                #f.write('\t\t\t}')
            elif isinstance(event, Note):
                f.write('\t\t\t\t"class":"note",\n')

                if event.duration != None:
                    dur_str = self.durationTunetoJSON(event.duration)
                    f.write('\t\t\t\t"duration":"%s",\n' %(dur_str))
                else:
                    f.write('\t\t\t\t"duration":"",\n')

                if event.s_duration != None:
                    f.write('\t\t\t\t"s_duration":"%lf",\n' %(event.s_duration))
                else:
                    f.write('\t\t\t\t"s_duration":"",\n')

                if event.frequency != None:
                    f.write('\t\t\t\t"frequency":"%lf",\n' %(event.frequency))
                else:
                    f.write('\t\t\t\t"frequency":"",\n')

                f.write('\t\t\t\t"onset":"%lf",\n' %(event.onset))

                self.writePitchtoFile(event.pitch, f)
            elif isinstance(event, Rest):
                f.write('\t\t\t\t"class":"rest",\n')

                if event.duration != None:
                    dur_str = self.durationTunetoJSON(event.duration)
                    f.write('\t\t\t\t"duration":"%s",\n' %(dur_str))
                else:
                    f.write('\t\t\t\t"duration":"",\n')

                if event.s_duration != None:
                    f.write('\t\t\t\t"s_duration":"%lf",\n' %(event.s_duration))
                else:
                    f.write('\t\t\t\t"s_duration":"",\n')

                f.write('\t\t\t\t"onset":"%lf",\n' %(event.onset))

                f.write('\t\t\t\t"pitch":{\n')  
                f.write('\t\t\t\t\t"letter":"r",\n') 
                f.write('\t\t\t\t\t"octave":"",\n') 
                f.write('\t\t\t\t\t"accidental":""\n')  
                f.write('\t\t\t\t}\n')      

            f.write('\t\t\t}')
            if x != e_len-1:
                f.write(',\n')
            else:
                f.write('\n')           

        f.write('\t\t],\n')

        keysig = self.keySignature
        if keysig == None:
            f.write('\t\t"keySignature": {}\n')
        else:
            f.write('\t\t"keySignature": {\n')
            if keysig.isMajor != None:
                f.write('\t\t\t"isMajor":"%s",\n' %(keysig.isMajor))
            else:
                f.write('\t\t\t"isMajor":"",\n')
            #f.write('\t\t\t')
            self.writePitchtoFile(keysig.pitch, f)
            f.write('\t\t}\n')

        f.write('\t}\n')
        f.write('}\n')
        f.close

        return filename

    def pitchJSONtoTune(self, pitch):
        if pitch['accidental'] != '':
            ksig_pitch_accidental = int(pitch['accidental'])
        else:
            ksig_pitch_accidental = ''
        ksig_pitch_letter = str(pitch['letter'])
        if pitch['octave'] != '':
            ksig_pitch_octave = int(pitch['octave'])
        else:
            ksig_pitch_octave = ''
        pitch = Pitch(accidental=ksig_pitch_accidental, letter=ksig_pitch_letter, octave=ksig_pitch_octave)
        return pitch

    def durationJSONtoTune(self, dur_str):
        dur = None
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

    def eventJSONtoTune(self, event):
        onset = float(event['onset'])
        duration = self.durationJSONtoTune(str(event['duration']))   
        #new_event = Event(duration=duration, onset=onset)

        if event['class'] == 'note':
            new_event = Note(duration=duration, onset=onset)
            if event['frequency'] != "":
                n_frequency = float(event['frequency'])
            else:
                n_frequency = None
            n_pitch = self.pitchJSONtoTune(event['pitch'])
            new_event.frequency = n_frequency
            new_event.setPitch(n_pitch)
        elif event['class'] == 'rest':
            new_event = Rest(duration=duration, onset=onset)
        elif event['class'] == 'chord': 
            new_event = Chord(duration=duration, onset=onset)
            pitches = []
            for p in event['pitches']:
                pch = self.pitchJSONtoTune(p)
                pitches.append(p)
            new_event.setPitch(pitches)
        return new_event
            

    def JSONtoTune(self, json_file):
        f = open(json_file)
        json_data = json.load(f)
        json_tune = json_data['tune']

        tune_title = json_tune['title']
        
        tune_contributors = []
        for contri in json_tune['contributors']:
            tune_contributors.append(str(contri))

        tune_clef = int(json_tune['clef'])

        tune_tsig1 = int(json_tune['timeSignature'][0])
        tune_tsig2 = int(json_tune['timeSignature'][1])
        tune_tsig = (tune_tsig1, tune_tsig2)

        tune_ksig_pitch = self.pitchJSONtoTune(json_tune['keySignature']['pitch'])
        iMflag = str(json_tune['keySignature']['isMajor'])
        iMflag.lower()
        ksigisMajor = True
        if iMflag == 'true':
            ksig_isMajor = True
        if iMflag == 'false':
            ksigisMajor = False
        tune_ksig = Key(pitch=tune_ksig_pitch, isMajor=ksigisMajor)

        tune_events = []
        for event in json_tune['events']:
            new = self.eventJSONtoTune(event)
            tune_events.append(new)

        self.setTitle(tune_title)
        self.setContributors(tune_contributors)
        self.clef = tune_clef
        self.setTimeSignature(tune_tsig)
        self.setKey(tune_ksig)
        self.setEventsList(tune_events)

    @staticmethod
    def convertFreqToPitch(freqlist):
        # return list of pitches
        pitchlist = []
        for freq in freqlist:
            # refer to http://stackoverflow.com/questions/20730133/extracting-pitch-features-from-audio-file
            pitchlist.append(Note.convertFreqToPitch(freq))
        return pitchlist

    ## SHOULD WE MOVE ticketsToTime and computeOnset methods to Event class?

    # turns ticks to time in seconds
    # The formula used is:
    # (# ticks * 60) / (BPM * resolution)
    @staticmethod
    def ticksToTime(ticks, bpm, resolution):
        return (ticks * 60) / (bpm * resolution)

    # takes in a duration in seconds, returns Duration enum value
    # 1 second = quarter note
    @staticmethod
    def secondsToDuration(dur):
        if (dur <= 0):
            return None
        approx_power = math.log(1/dur, 2)
        note_val = 4 - (round(approx_power) + 2)
        Dur_array = [Duration.SIXTEENTH, Duration.EIGHTH, Duration.QUARTER, Duration.HALF, Duration.WHOLE]
        if note_val < 0:
            return Duration.SIXTEENTH
        if note_val >= 4:
            # next iteration: add greater variety of note durations, e.g. combination of notes
            return Duration.WHOLE
        else: 
            return Dur_array[int (note_val)]

    # Reads a MIDI file in, returns a list of Notes
    # Notes are populated with onset and duration
    # assumes a one track MIDI file with notes in chronological order

    def computeOnset(self, myfile):
        pattern = self.MIDItoPattern(myfile)
        NotesList = []
        index = 0
        bpm = 0
        resolution = pattern.resolution
        s_duration = 0
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
                        s_duration = endset - currNote.onset
                        currNote.s_duration = s_duration
                        currNote.duration = self.secondsToDuration(s_duration)
                        # print "currNote", currNote.duration
                        index += 1
                    else:
                        onset = self.ticksToTime(event.tick, bpm, resolution)
                        # print onset
                        newNote = Note(onset = onset)
                        # print "newNote", newNote.duration
                        if newNote.duration != None:
                            NotesList.append(newNote)
        return NotesList

    # Takes a list of pitched Notes, returns a list of Notes with the included rests
    def calculateRests(self, list_of_notes):
        n_notes = len(list_of_notes)
        allNotes = []
        for i in range(0, n_notes-1):
            allNotes.append(list_of_notes[i])
            noteonset = list_of_notes[i].onset if list_of_notes[i].onset!=None else 0
            noteduration = list_of_notes[i].s_duration if list_of_notes[i].s_duration!= None else 0
            onset = noteonset + noteduration
            s_duration = list_of_notes[i+1].onset - onset
            duration = self.secondsToDuration(s_duration)
            if (duration != None): # duration is too small to consider as a rest
                #r_pitch = Pitch(letter="r")
                rest = Rest(duration=duration, s_duration=s_duration, onset=onset)
                allNotes.append(rest)
            if i == n_notes-2:
                allNotes.append(list_of_notes[n_notes-1])
        return allNotes

    # convert MIDI file to Pattern
    @staticmethod
    def MIDItoPattern(file):
        return midi.read_midifile(file)

    def toString(self):
        clefstring = {Clef.BASS: 'Bass', Clef.TREBLE: 'Treble'}.get(self.clef)
        if (self.getKey() == None):
            keystring = 'None'
        else:
            keystring = self.getKey().toString()
        buf = "Tune: \nTitle - %s, Contributors - %s \n\tTime Sig - %s, KeySig - %s, Clef - %s\nList of Notes:\n" %(self.title, str(self.contributors), str(self.timeSignature), keystring, clefstring)
        if self.getEventsList() != None:
            for event in self.getEventsList():
                buf = buf + "%s\n" %(event.toString())
        else:
                buf = buf + "No events list\n"
        return buf

    # def eventsListEquals(self, list1, list2):
    #     if len(list1) != len(list2):
    #         return False
    #     for i in range(len(list1)):
    #         if list1[i].eventEqual(list2[i]) == False:
    #             return False
    #     return True
    
    #aubio output array to event list using aubionotes
    def readWav(self, filename):
            ofArray=[]
            f= subprocess.check_output(["aubionotes", "-i", filename])
            raw = f.splitlines()
            for line in raw:
                ofArray = ofArray+[line.split()]
            events = []
            oldtuple = raw.pop(0)
            for tuple in ofArray:
                if len(tuple) ==1:
                    if len(oldtuple) ==1:
                        sdur = float(tuple[0]) - float(oldtuple[0])
                        events = events + [Rest(onset=oldtuple[0], s_duration=sdur, duration = self.secondsToDuration(sdur))]
                    else:
                        sdur = float(tuple[0]) - float(oldtuple[2])
                        events = events + [Rest(onset=oldtuple[2], s_duration=sdur, duration = self.secondsToDuration(sdur))]
                else:
                    sdur = float(tuple[2]) - float(tuple[1])
                    p = Pitch()
                    p = p.MIDInotetoPitch(math.floor(float(tuple[0])))
                    events = events+[Note(pitch=p, onset=float(tuple[1]), s_duration=sdur, duration = self.secondsToDuration(sdur))]
                oldtuple=tuple
            self.setEventsList(events)

                                   
# main function used for testing of Tune.py separate from web integration
if __name__ == "__main__":
    # default parameters
    INPUT_FILE = '../tests/MIDITestFiles/c-major-scale-treble.mid'
    # Sets parameters and files
    for i in xrange(1,len(sys.argv)):
        if (sys.argv[i] == '-f'): # input flag: sets input file name
            INPUT_FILE = sys.argv[i+1]
    # dummyInstance = Tune()
    # print dummyInstance.MIDItoPattern(INPUT_FILE)
#    print INPUT_FILE
    tune = Tune.TuneWrapper(INPUT_FILE)
    print tune.toString()
    tune.TunetoJSON()

#    file1 = '../tests/MIDITestFiles/three-notes-no-break.mid'
#    file1 = '../tests/MIDITestFiles/Berkeley Lennox Theme.mid'
    file1 = '../tests/MIDITestFiles/tune-with-chord-rest-note.mid'
    tune = Tune.TuneWrapper(file1)
#    runConvert('../tests/WAVTestFiles/Test1/')
    # tuneWav = Tune(wav = 'test1.wav')
    # tuneWav = Tune(wav = '../tests/WAVTestFiles/myRecording00.wav')
    # print tuneWav.toString()
    print tune.toString()

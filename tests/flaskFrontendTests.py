import sys
sys.path.insert(0, '../src')

from app import app
from app import getTune, setTune, makeLilypondFile, tuneToNotes, makeStaffFromTune, saveLilypondForDisplay, tunetoMeasures
import unittest
import Tune
import subprocess
import glob
import time
import abjad

tune = None

class AppTestCase(unittest.TestCase):


    def setUp(self):
        global tune
        app.config['TESTING'] = True
        self.app = app.test_client()
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")
        tune.title = "test title"

    @classmethod
    def tearDownClass(cls):
        subprocess.Popen(["rm"] + glob.glob("test.ly"))

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    # make sure only one pdf is in currentTune at a time so that there
    # is not an overload when new files are being uploaded
    def test_delete_old_PDF(self):
        #delete all old pdfs to start
        subprocess.Popen(["rm"] + glob.glob("static/currentTune/*.pdf"))

        # make 10 files and assert each time that there is one pdf in currentTune
        for i in range(0,10):
            self.app.get('/')
            files = glob.glob("static/currentTune/*.pdf")
            time.sleep(1)
            self.assertEqual(len(files),1)

    def test_make_lilypond_file(self):
        # test both branches to make sure it works if tune object is empty

        # test that some lilypond file is created when no tune object is present
        ly_file = makeLilypondFile(None)
        self.assertIsNotNone(ly_file)

        # make file from tune object and check that title matches
        ly_file = makeLilypondFile(tune)

        self.assertEqual(str(ly_file.header_block.title),"\\markup { \""+tune.title+"\" }")
        self.assertIsNotNone(ly_file)

    def test_tune_to_notes(self):
        # test tune with no notes
        res = tuneToNotes(None)
        self.assertEqual(res,[])

        # test tune with every possible combination of settings on a note
        # send this info to abjad and make a lilypond file.
        # the test here is that this doesn't crash. not testing accuracy of display,
        # as that is done on the side of abjad/lilypond.
        # this is just testing that every possible combination of our internal not representation
        # can be sent to abjad/lilypond without an error
        testTune = Tune.Tune()
        notes = []
        durations = [Tune.Duration.SIXTEENTH,Tune.Duration.EIGHTH,Tune.Duration.QUARTER,
                                     Tune.Duration.HALF,Tune.Duration.WHOLE]
        for letter in ['a','b','c','d','e','f','g']:
            for accidental in [Tune.Accidental.FLAT, Tune.Accidental.SHARP]:
                for octave in range(1,11):
                    for duration in durations:
                        pitch = Tune.Pitch()
                        pitch.letter = letter
                        pitch.accidental = accidental
                        pitch.octave = octave
                        note = Tune.Note()
                        note.pitch = pitch
                        note.duration = duration
                        notes.append(note)
                        note2 = Tune.Note()
                        note2.pitch = pitch
                        notes.append(note2)
        # test rests -- both with and without a duration
        for duration in durations:
            rest = Tune.Note()
            rest.letter = 'r'
            rest.duration = duration
            notes.append(rest)
            rest2 = Tune.Note()
            rest2.letter = 'r'
            notes.append(rest2)
        # test empty note
        notes.append(Tune.Note())
        testTune.setEventsList(notes)
        # test calling tuneToNotes
        notesA = tuneToNotes(testTune)
        staff = abjad.Staff()
        for measure in notesA:
            m = abjad.Measure(abjad.TimeSignature(tune.getTimeSignature()), measure)
            d = m._preprolated_duration
            if d == abjad.TimeSignature(tune.getTimeSignature()).duration:
                staff.append(m)
        abjad.lilypondfiletools.make_basic_lilypond_file(staff)


        # test a bad note fails
        badNote = Tune.Note()
        pitch = Tune.Pitch()
        pitch.letter = 'k'
        pitch.accidental = Tune.Accidental.FLAT
        pitch.octave = 1
        badNote.pitch = pitch
        badNotes = [badNote]
        badTune = Tune.Tune()
        badTune.setEventsList(badNotes) # changed tuneiter2
        self.assertRaises(TypeError,tuneToNotes,badTune)

    def test_title_and_name_input(self):
        global tune
        setTune(tune)

        # test valid title
        self.app.post('/', data=dict(
            titleInput="test my title!",
        ), follow_redirects=True)

        tune = getTune()
        self.assertEqual(tune.title,"test my title!".upper())

        # test invalid title (newline character)
        self.app.post('/', data=dict(
            titleInput="my\\ntitle!",
        ), follow_redirects=True)

        tune = getTune()
        self.assertEqual(tune.title, "test my title!".upper())

        # test invalid title (too long)
        self.app.post('/', data=dict(
            titleInput="test my titlelskdjflajdf;lakjsdf;lkajsdf;lkjas;dsdlkfjlskdjfldkfjlksjdflkfjlskdfjlsdfjoiwehgoaihgoishegoishegoishegoishegoiahseogahlskjdflk",
        ), follow_redirects=True)

        tune = getTune()
        self.assertEqual(tune.title, "test my title!".upper())

        # test invalid title (only spaces)
        self.app.post('/', data=dict(
            titleInput="            "
        ), follow_redirects=True)

        tune = getTune()
        self.assertEqual(tune.title, "test my title!".upper())

        # test invalid title (empty string)
        self.app.post('/', data=dict(
            titleInput=""
        ), follow_redirects=True)

        tune = getTune()
        self.assertEqual(tune.title, "test my title!".upper())

        # test valid contributors
        self.app.post('/', data=dict(
            contributorsInput="good name, good name, good name"
        ), follow_redirects=True)

        tune = getTune()
        self.assertEqual(tune.contributors, "good name, good name, good name")
        # title and contributors have same constraints so no need to test bad contributors

    def test_midi_upload(self):

        global tune
        setTune(tune)

        # Testing a valid .mid file
        f = open("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid", 'rb')
        self.app.post(
            '/',
            data={
                'fileInput': f,
            },
            content_type = 'multipart/form-data',
        )

        # The tune object should have found the midi file, in the uploads directory
        tune = getTune()
        self.assertEqual(tune.midifile, "static/uploads/e-flat-major-scale-on-bass-clef.mid")

        # Testing a non midi file
        f = open("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.pdf", 'rb')
        self.app.post(
            '/',
            data={
                'fileInput': f,
            },
            content_type='multipart/form-data',
        )

        # The tune object should not have chosen the pdf, should remain unchanged
        tune = getTune()
        self.assertEqual(tune.midifile, "static/uploads/e-flat-major-scale-on-bass-clef.mid")

    def test_change_title_and_name(self):

        global tune
        setTune(tune)

        # test title change displays in PDF
        self.app.post('/', data=dict(
            titleInput="test my title!",
        ), follow_redirects=True)

        tune = getTune()
        ly_file = makeLilypondFile(tune)
        test_title = "test my title!".upper()
        self.assertEqual(str(ly_file.header_block.title), "\\markup { \"" + test_title + "\" }")

        # test contributors change displays in PDF
        self.app.post('/', data=dict(
            contributorsInput="good name, bad name, ok name",
        ), follow_redirects=True)

        tune2 = getTune()
        ly_file = makeLilypondFile(tune2)
        self.assertEqual(str(ly_file.header_block.composer), "\\markup { \"good name, bad name, ok name\" }")

    # ALL BELOW HERE IS FOR ITERATION 2 (MILESTONE 4A)

    # rachel
    def test_clef(self):
        # set the tune object
        global tune
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")

        for c in [Tune.Clef.BASS, Tune.Clef.TREBLE]:
            # make a staff from our tune object
            tune.clef = c
            staff = makeStaffFromTune(tune)
            # make and save lilypond file from the staff
            lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
            saveLilypondForDisplay(lilypond_file)
            abjad.systemtools.IOManager.save_last_ly_as("test.ly")
            file = open("test.ly")
            # make sure clef is in lilypond file
            isPresent = ('        \\clef "' + {Tune.Clef.BASS: 'bass', Tune.Clef.TREBLE: 'treble'}.get(c) + '"\n' in file.readlines())
            self.assertEqual(isPresent, True)

    # rachel
    def test_key(self):
        # set the tune object
        global tune
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")

        # iterature through all combinations of key signature pitches
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            for isMajor in [True,False]:
                # make a key signature
                pitch = Tune.Pitch()
                pitch.letter = letter
                k = Tune.Key()
                k.pitch = pitch
                k.isMajor = isMajor

                # make a staff from our tune object
                tune.keySignature = k
                staff = makeStaffFromTune(tune)
                # make and save lilypond file
                lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
                saveLilypondForDisplay(lilypond_file)
                abjad.systemtools.IOManager.save_last_ly_as("test.ly")
                file = open("test.ly")
                # make sure correct key is in lilypond file
                if isMajor:
                    isPresent = ('        \\key ' + letter + ' \\major\n' in file.readlines())
                else:
                    isPresent = ('        \\key ' + letter + ' \\minor\n' in file.readlines())
                self.assertEqual(isPresent,True)

    # rachel
    def test_time_signature(self):
        # set the tune object
        global tune
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")

        # iterate through some time signatures
        for t in [(3, 4), (4, 4), (3, 8), (2, 4), (-1, -1)]:
            # make a staff from our tune object
            tune.setTimeSignature(t)
            staff = makeStaffFromTune(tune)
            # make and save lilypond file
            lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
            saveLilypondForDisplay(lilypond_file)
            abjad.systemtools.IOManager.save_last_ly_as("test.ly")
            file = open("test.ly")
            # check if time signature t is in lilypond file
            isPresent = ('            \\time ' + str(t[0]) + '/' + str(t[1]) + '\n' in file.readlines())
            # make sure invalid key not present
            if t == (-1, -1):
                self.assertEqual(isPresent, False)
            # make sure valid key present
            else:
                self.assertEqual(isPresent, True)

    # zakir
    # def test_delete_notes(self):
    #     # Below is a comprehensive test tune input (all possible notes)
    #     testTune1 = Tune.Tune()
    #     notesInternal1 = []
    #
    #     durations = [Tune.Duration.SIXTEENTH, Tune.Duration.EIGHTH, Tune.Duration.QUARTER,
    #                  Tune.Duration.HALF, Tune.Duration.WHOLE]
    #     for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
    #         for accidental in [Tune.Accidental.FLAT, Tune.Accidental.SHARP]:
    #             for octave in range(1, 11):
    #                 for duration in durations:
    #                     pitch = Tune.Pitch()
    #                     pitch.letter = letter
    #                     pitch.accidental = accidental
    #                     pitch.octave = octave
    #                     note = Tune.Note()
    #                     note.pitch = pitch
    #                     note.duration = duration
    #                     notesInternal1.append(note)
    #     # test rests -- both with and without a duration
    #     for duration in durations:
    #         rest = Tune.Note()
    #         rest.letter = 'r'
    #         rest.duration = duration
    #         notesInternal1.append(rest)
    #         rest2 = Tune.Note()
    #         rest2.letter = 'r'
    #         notesInternal1.append(rest2)
    #     # test empty note
    #     notesInternal1.append(Tune.Note())
    #     testTune1.setEventsList(notesInternal1)
    #     # test calling tuneToNotes
    #     notes1 = tuneToNotes(testTune1)
    #     staff1 = abjad.Staff(notes1)
    #     abjad.lilypondfiletools.make_basic_lilypond_file(staff1)
    #
    #
    #     # Now try deleting notes at all different positions
    #     for i in range(len(notesInternal1)):
    #         self.app.post('/', data=dict(
    #             notes_submit="submit",
    #             measure_number=i/4,
    #             note_number=i%4,
    #             submit_type="delete"
    #         ), follow_redirects=True)
    #         tune = getTune()
    #         ithPositionDeleted = notesInternal1[:i] + notesInternal1[i + 1:]
    #         self.assertEqual(tune.getEventsList(), ithPositionDeleted)

    # zakir
    # def test_add_notes(self):
    #     # Below is a comprehensive test tune input (all possible notes)
    #     testTune1 = Tune.Tune()
    #     notesInternal1 = []
    #
    #     durations = [Tune.Duration.SIXTEENTH, Tune.Duration.EIGHTH, Tune.Duration.QUARTER,
    #                  Tune.Duration.HALF, Tune.Duration.WHOLE]
    #     for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
    #         for accidental in [Tune.Accidental.FLAT, Tune.Accidental.SHARP]:
    #             for octave in range(1, 11):
    #                 for duration in durations:
    #                     pitch = Tune.Pitch()
    #                     pitch.letter = letter
    #                     pitch.accidental = accidental
    #                     pitch.octave = octave
    #                     note = Tune.Note()
    #                     note.pitch = pitch
    #                     note.duration = duration
    #                     notesInternal1.append(note)
    #                     note2 = Tune.Note()
    #                     note2.pitch = pitch
    #                     notesInternal1.append(note2)
    #     # test rests -- both with and without a duration
    #     for duration in durations:
    #         rest = Tune.Note()
    #         rest.letter = 'r'
    #         rest.duration = duration
    #         notesInternal1.append(rest)
    #         rest2 = Tune.Note()
    #         rest2.letter = 'r'
    #         notesInternal1.append(rest2)
    #     # test empty note
    #     notesInternal1.append(Tune.Note())
    #     testTune1.setEventsList(notesInternal1)
    #     # test calling tuneToNotes
    #     notes1 = tuneToNotes(testTune1)
    #     staff1 = abjad.Staff(notes1)
    #     abjad.lilypondfiletools.make_basic_lilypond_file(staff1)
    #
    #     # Now try adding a every duration note at all different positions
    #     for currentDuration in durations:
    #         for i in range(len(notesInternal1)):
    #             tune = getTune()
    #             add
    #             self.app.post('/', data=dict(
    #                 addNoteInput="{'position': " + str(i) + ", letter: 'a', octave: 4}",
    #             ), follow_redirects=True)
    #             note = Tune.Note()
    #             pitch = Tune.Pitch()
    #             pitch.letter = 'a'
    #             pitch.octave = 4
    #             note.pitch = pitch
    #             note.duration = currentDuration
    #             ithPositionAdded = notesInternal1[:i] + [note] + notesInternal1[i + 1:]
    #             self.assertEqual(tune.getEventsList(), ithPositionAdded)

    # rachel
    def test_making_chord(self):
        durations = [Tune.Duration.SIXTEENTH, Tune.Duration.EIGHTH, Tune.Duration.QUARTER,
                     Tune.Duration.HALF, Tune.Duration.WHOLE]

        testTune = Tune.Tune()
        chords = []
        # make a chord for all possible durations
        for duration in durations:
            pitch1 = Tune.Pitch()
            pitch1.letter = 'a'
            pitch1.accidental = Tune.Accidental.FLAT
            pitch1.octave = 5

            pitch2 = Tune.Pitch()
            pitch2.letter = 'd'
            pitch2.accidental = Tune.Accidental.SHARP
            pitch2.octave = 6

            pitch3 = Tune.Pitch()
            pitch3.letter = 'g'
            pitch3.octave = 3

            pitches = [pitch1,pitch2,pitch3]

            # make a chord in impromptu backend
            chord = Tune.Chord()
            chord.setPitch(pitches)
            chord.duration = duration

            chords.append(chord)

        testTune.setEventsList(chords)

        # test calling tuneToNotes and make sure a lilypond file can be created with no error
        notesA = tuneToNotes(testTune)
        staff = abjad.Staff()
        for measure in notesA:
            m = abjad.Measure(abjad.TimeSignature(tune.getTimeSignature()), measure)
            d = m._preprolated_duration
            if d == abjad.TimeSignature(tune.getTimeSignature()).duration:
                staff.append(m)
        abjad.lilypondfiletools.make_basic_lilypond_file(staff)

############################ EDITING SHEET MUSIC ###################################################
# User chooses a measure number from a dropdown. Pop up occurs to display the notes in that measure,
# each with its duration and pitch. Option to delete a note and add a note or edit the duration
# and pitch of the given notes (both given from dropdowns). Then update the Tune object
# accordingly and recreate the lilypond file to have abjad display it as a pdf.
####################################################################################################

# entering a measure number returns the right indices of notes in our tune object's note array
# (test a few measure numbers) -- sofia
    def test_get_notes_by_measure(self):

        global tune
        setTune(tune)
        # making test tune

        notes = []

        for n in range(4):
            note1 = Tune.Event()
            note1.pitch = Tune.Pitch()
            note1.letter = "c"
            note1.duration = (1,1)
            notes.append(note1)

        tune.setEventsList(notes)

        # test split measures to split notes into groups by measure
        self.assertEqual(4, len(tunetoMeasures(tune)))

        # test for empty measures edge case
        emptyTune = Tune.Tune()
        self.assertEqual(0, len(tunetoMeasures(emptyTune)))

        # test output of tunetoMeasures to return a note by measure

        outputMeasures = tunetoMeasures(tune)
        note1 = Tune.Note()
        note1.pitch = Tune.Pitch()
        note1.pitch.letter = "c"
        note1.pitch.octave = 4
        note1.duration = (1, 1)
        testNote = note1
        self.assertEqual(testNote.getPitch()[0].letter, outputMeasures[0][0].getPitch()[0].letter)
        self.assertEqual(testNote.duration, outputMeasures[0][0].duration)
        self.assertEqual(testNote.getPitch()[0].accidental, outputMeasures[0][0].getPitch()[0].accidental)
        self.assertEqual(testNote.getPitch()[0].octave, outputMeasures[0][0].getPitch()[0].octave)
        self.assertEqual(1, len(outputMeasures[1]))


    # changing duration (will be from a dropdown so can't be invalid) -- rachel
    def test_change_duration(self):
        # make notes and add to the list notes
        durations = [Tune.Duration.QUARTER, Tune.Duration.QUARTER, Tune.Duration.QUARTER,
                     Tune.Duration.QUARTER]
        notes = []

        curr_onset = 0.0
        for duration in durations:
            pitch = Tune.Pitch()
            pitch.letter = "a"
            pitch.octave = 5
            note = Tune.Note()
            note.pitch = pitch
            note.duration = duration
            note.onset = curr_onset
            curr_onset += 0.25
            notes.append(note)

        # make test tune object with the notes
        testTune = Tune.Tune()
        testTune.setTimeSignature((4,4))
        testTune.setEventsList(notes)
        # set the app's tune to be this test tune
        setTune(testTune)

        # for each note, send a request to edit the duration
        for i in range(0,len(durations)):
            newDuration = durations[len(durations)-i-1]
            self.app.post('/', data=dict(
                note_submit="submit",
                measure_number='1',
                note_number='1',
                noteIndex='0',
                duration0='1',
                duration1=str(newDuration),
                submit_type="edit"
            ), follow_redirects=True)

            # after making post request to change the duration, make sure new tune object's note list has been updated
            updatedTune = getTune()
            noteI = updatedTune.events[i]
            durationI = noteI.duration

            self.assertEqual(durationI,newDuration)




    # changing pitch (letter or accidental) (will be from a dropdown so can't be invalid) -- rachel
    def test_change_pitch(self):
        # make notes of all possible pitches and add to notes list
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        accidentals = [Tune.Accidental.FLAT, Tune.Accidental.SHARP]
        octaves = range(1, 11)
        notes = []

        for letter in letters:
            for accidental in accidentals:
                for octave in octaves:
                    pitch = Tune.Pitch()
                    pitch.letter = letter
                    pitch.accidental = accidental
                    pitch.octave = octave
                    note = Tune.Note()
                    note.pitch = pitch
                    note.duration = Tune.Duration.HALF
                    note.onset = 0.0
                    notes.append(note)

        # make test tune object with the notes
        testTune = Tune.Tune()
        testTune.setEventsList(notes)
        # set the app's tune to be this test tune
        setTune(testTune)

        # send a request to edit the pitch for the note 1 in measure 0
        for i in range(0, len(notes),15):
            newPitch = Tune.Pitch()
            newPitch.letter = letters[i % len(letters)] # just choose some letter in the letters list
            newPitch.accidental = accidentals[i %len(accidentals)] # just choose some accident in the accidentals list
            newPitch.octave = octaves[i % len(octaves)] # just choose some octave in the octaves list

            self.app.post('/', data=dict(
                note_submit="submit",
                measure_number='1',
                note_number='1',
                duration1='4',
                pitch=str(newPitch.letter),
                accidental=str(newPitch.accidental),
                octave=str(newPitch.octave),
                submit_type="edit"
            ), follow_redirects=True)

            # after making post request to change the duration, make sure new tune object's note list has been updated
            updatedTune = getTune()
            noteI = updatedTune.events[1]
            pitchI = noteI.pitch

            self.assertEqual(newPitch.letter, pitchI.letter)

    # upload a json file (and that a non-json file doesn't upload) -- sofia
    def test_json_upload(self):
        print "test_json_upload"
        global tune
        setTune(tune)

        # Testing a valid .json file
        f = open("../tests/JSONTestFiles/tune-generic.json", 'rb')

        self.app.post(
            '/',
            data={
                'jsonInput': f,
            },
            content_type='multipart/form-data',
        )
        f.close()
        f = open("../tests/JSONTestFiles/tune-generic.json", 'r')
        r = f.read()
        f.close()
        lines_input = r.splitlines()

        tune = getTune()
        tune.TunetoJSON(filename='test-output.json')

        f1 = open("test-output.json", 'r')

        r1 = f1.read()
        f1.close()
        lines_output = r1.splitlines()

        output_len = len(lines_output)
        input_len = len(lines_input)
        self.assertEqual(output_len, input_len)
        for i in range(output_len):
            print i
            self.assertEqual(lines_output[i], lines_input[i])

        print "test_json_upload passed"


    # upload wav -- sofia
    def test_wav_upload(self):
        global tune
        setTune(tune)

        # Testing a valid .wav file
        #f = open("../tests/WAVTestFiles/test1.wav", 'rb')
        #self.app.post(
        #    '/',
        #    data={
        #        'fileInput': f,
        #    },
        #    content_type='multipart/form-data',
        #)

        #f.close()
        # Testing a non wav file
        f = open("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.pdf", 'rb')
        self.app.post(
            '/',
            data={
                'fileInput': f,
            },
            content_type='multipart/form-data',
        )


if __name__ == '__main__':
    unittest.main()
import sys
sys.path.insert(0, '../src')

from app import app
from app import getTune, setTune, makeLilypondFile, tuneToNotes, makeStaffFromTune, saveLilypondForDisplay
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
        print "RUNNING: test_home_status_code ..."
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print "PASSED"

    # make sure only one pdf is in currentTune at a time so that there
    # is not an overload when new files are being uploaded
    # def test_delete_old_PDF(self):
    #     print "RUNNING: test_delete_old_PDF ..."
    #     #delete all old pdfs to start
    #     subprocess.Popen(["rm"] + glob.glob("static/currentTune/*.pdf"))
    #
    #     # make 10 files and assert each time that there is one pdf in currentTune
    #     for i in range(0,10):
    #         self.app.get('/')
    #         files = glob.glob("static/currentTune/*.pdf")
    #         time.sleep(1)
    #         self.assertEqual(len(files),1)
    #     print "PASSED"

    def test_make_lilypond_file(self):
        print "RUNNING: test_make_lilypond_file ..."
        # test both branches to make sure it works if tune object is empty

        # test that some lilypond file is created when no tune object is present
        ly_file = makeLilypondFile(None)
        self.assertIsNotNone(ly_file)

        # make file from tune object and check that title matches
        ly_file = makeLilypondFile(tune)

        self.assertEqual(str(ly_file.header_block.title),"\\markup { \""+tune.title+"\" }")
        self.assertIsNotNone(ly_file)
        print "PASSED"

    def test_tune_to_notes(self):
        print "RUNNING: test_tune_to_notes ..."
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
        testTune.setNotesList(notes)
        # test calling tuneToNotes
        notesA = tuneToNotes(testTune)
        staff = abjad.Staff(notesA)
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
        badTune.setNotesList(badNotes)
        self.assertRaises(TypeError,tuneToNotes,badTune)

        print "PASSED"

    def test_title_and_name_input(self):
        print "RUNNING: test_title_and_name_input ..."
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

        print "PASSED"

    def test_midi_upload(self):
        print "RUNNING: test_midi_upload ..."

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

        print "PASSED"


    def test_change_title_and_name(self):
        print "RUNNING: test_change_title_and_name ..."

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

        print "PASSED"


    # ALL BELOW HERE IS FOR ITERATION 2
        #TODO: Iteration 2
        #upload mp3 -- zakir


    #clef, key,time signature -- rachel
    def test_clef(self):
        print "RUNNING test_clef ... "
        global tune
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")

        for c in [Tune.Clef.BASS, Tune.Clef.TREBLE]:
            # make a staff from our tune object
            tune.clef = c
            staff = makeStaffFromTune(tune)
            # make and save lilypond file
            lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
            saveLilypondForDisplay(lilypond_file)
            abjad.systemtools.IOManager.save_last_ly_as("test.ly")
            file = open("test.ly")
            #print file.readlines()
            # make sure clef is in lilypond file
            isPresent = ('        \\clef "' + {Tune.Clef.BASS: 'bass', Tune.Clef.TREBLE: 'treble'}.get(c) + '"\n' in file.readlines())
            self.assertEqual(isPresent, True)
        print "PASSED"

    def test_key(self):
        print "RUNNING: test_key ..."

        global tune
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")

        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            for isMajor in [True,False]:
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
                # make sure key is in lilypond file
                if isMajor:
                    isPresent = ('        \\key ' + letter + ' \\major\n' in file.readlines())
                else:
                    isPresent = ('        \\key ' + letter + ' \\minor\n' in file.readlines())
                self.assertEqual(isPresent,True)
        print "PASSED"


    def test_time_signature(self):
        print "RUNNING test_time_signature ... "

        global tune
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")

        for t in [(3, 4), (4, 4), (3, 8), (2, 4), (-1, -1)]:
            # make a staff from our tune object
            tune.setTimeSignature(t)
            staff = makeStaffFromTune(tune)
            # make and save lilypond file
            lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(staff)
            saveLilypondForDisplay(lilypond_file)
            abjad.systemtools.IOManager.save_last_ly_as("test.ly")
            file = open("test.ly")
            # make sure time signature is in lilypond file
            isPresent = ('        \\time ' + str(t[0]) + '/' + str(t[1]) + '\n' in file.readlines())
            # make sure invalid key not present
            if t == (-1, -1):
                self.assertEqual(isPresent, False)
            # make sure valid key present
            else:
                self.assertEqual(isPresent, True)
        print "PASSED"

        #chords -- rachel

        #record to mp3 -- sofia

        # User chooses a measure number from a dropdown. Pop up occurs to display the notes in that measure,
        # each with its duration and pitch. Option to delete a note and add a note or edit the duration
        # and pitch of the given notes. We then update the Tune object accordingly and recreate the lilypond
        # file to have abjad display as a pdf.

        # entering a measure number returns the right indices of notes in our tune object's note array
        # (test a few measure numbers) -- sofia


        # entering valid duration and an invalid duration -- rachel

        # entering valid pitch and an invalid pitch (letter or accidental) -- rachel

        # deleting notes -- zakir

        # adding notes -- zakir

        # download and upload a json file (and that a non-json file doesn't upload) -- sofia

if __name__ == '__main__':
    unittest.main()
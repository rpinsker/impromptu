import sys
sys.path.insert(0, '../src')

from app import app
from app import getTune, setTune, makeLilypondFile, tuneToNotes
import unittest
import Tune
import subprocess
import glob
import time
import abjad
from StringIO import StringIO
from flask import Request

tune = None

class AppTestCase(unittest.TestCase):


    def setUp(self):
        global tune
        app.config['TESTING'] = True
        self.app = app.test_client()
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/e-flat-major-scale-on-bass-clef.mid")

    # def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])


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
        self.assertEqual(str(ly_file.header_block.title),"\\markup { "+tune.title+" }")
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







    # TODO: changing titles and names (both in pdf and on backend),


if __name__ == '__main__':
    unittest.main()
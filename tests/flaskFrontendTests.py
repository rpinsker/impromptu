import sys
sys.path.insert(0, '../src')

from app import app
from app import getTune, setTune
import unittest
import Tune
import subprocess
import glob
import time

tune = None

class AppTestCase(unittest.TestCase):


    def setUp(self):
        global tune
        app.config['TESTING'] = True
        self.app = app.test_client()
        tune = Tune.Tune.TuneWrapper("../tests/MIDITestFiles/c-major-scale-treble.mid")

    # def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])


    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_delete_old_PDF(self):
        #TODO RACHEL
        #delete all old pdfs to start
        subprocess.Popen(["rm"] + glob.glob("static/currentTune/*.pdf"))

        # make 10 files and assert each time that there is one pdf in currentTune
        for i in range(0,10):
            self.app.get('/')
            files = glob.glob("static/currentTune/*.pdf")
            time.sleep(1)
            self.assertEqual(len(files),1)

    # def test_make_lilypond_file(self):
    #     #TODO RACHEL
    #     # test both branches
    #     self.assertEqual(False,True)
    #
    # def test_tune_to_notes(self):
    #     #TODO RACHEL
    #     self.assertEqual(False,True)

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
            titleInput="my\ntitle!",
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


    # TODO test uploading file (real MIDI and bad) and changing titles and names (both in pdf and on backend),

if __name__ == '__main__':
    unittest.main()
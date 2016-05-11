import os
import sys
sys.path.insert(0, '../src')

from app import app
import unittest
import tempfile

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        # flaskr.app.config['TESTING'] = True
        # self.app = flaskr.app.test_client()
        # flaskr.init_db()

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
        self.assertEqual(False,True)

    def test_make_lilypond_file(self):
        #TODO RACHEL
        # test both branches
        self.assertEqual(False,True)

    def test_tune_to_notes(self):
        #TODO RACHEL
        self.assertEqual(False,True)

    def test_title_and_name_input(self):
        #TODO RACHEL
        self.assertEqual(False,True)

    # TODO test uploading file (real MIDI and bad) and changing titles and names (both in pdf and on backend),

if __name__ == '__main__':
    unittest.main()
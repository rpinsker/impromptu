import unittest
import abjad

def displayNoteTest(self):
    #Testing the display of a normal tune object
    note = Note(493.88, 2.0)
    notes = [note]
    test_staff = Staff(notes)
    control_staff = "good_staff.pdf"
    self.assertTrue(StaffEquals(test_staff,control_staff))

    #Testing the lack of display of an abnormal tune object
    note1 = (Note -1.00, 0.0)
    note2 = (Note 493.88, -1.0)
    test_staff1 = Staff([note1])
    test_staff2 = Staff([note2])
    self.assertFalse(test_staff1)
    self.assertFalse(test_staff2)

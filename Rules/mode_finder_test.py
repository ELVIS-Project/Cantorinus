import unittest
from mode_finder import *
import music21
from vis.analyzers.indexers import noterest

class ModeFinderTest(unittest.TestCase):
    '''
    Classes also contain docstrings, even if they are out of the box unit tests.
    '''
    def setUp(self):
        """
        setUp() creates global variables for the unittests.
        """

        piece = 'music/christlag.mei'
        global the_score
        the_score = music21.converter.parse(piece)
        the_notes = noterest.NoteRestIndexer(the_score).run()
        global part_notes
        part_notes = the_notes['noterest.NoteRestIndexer']['0'].tolist()
        global notes
        notes = []
        for note in ['D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5']:
            notes.append(music21.note.Note(note))

    def test_finalis(self):
        '''
        The test_finalis() tests the finalis() function by equality.
        '''

        d4 = music21.note.Note('D4')
        global fin
        fin = d4
        self.assertEqual(finalis(part_notes), d4)

    def test_pitch_range(self):
        '''
        The test_pitch_range() function tests the pitch_range() function by equality.
        '''

        part = the_score.parts[0]
        d4 = music21.note.Note('D4')
        e5 = music21.note.Note('E5')
        global p_range
        p_range = d4, e5
        self.assertEqual(pitch_range(part), (d4, e5))

    def test_range_type(self):
        """
        test_range_type() checks if range_type() returns 'complete'
        """

        self.assertEqual(range_type(p_range), 'complete')

    def test_species(self):
        """
        test_species() checks if species() returns ['T', 'S', 'T', 'T'],
        ['T', 'S', 'T']
        """

        sp = ['T', 'S', 'T', 'T'], ['T', 'S', 'T']
        d4 = music21.note.Note('D4')
        r_type = 'complete'
        self.assertEqual(species(notes, d4, r_type), sp)

    def test_spec_prep(self):
        """
        test_spec_prep() checks if spec_prep() returns the sorted range,
        ['D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5']
        """

        self.assertEqual(spec_prep(part_notes), notes)

    def test_characteristic(self):
        """
        test_characteristic() checks if characteristic() returns A
        """

        self.assertEqual(characteristic(the_score), 'A')

    def test_smaller(self):
        """
        test_smaller() checks if smaller() returns E4
        """

        a4 = music21.note.Note('A4')
        e4 = music21.note.Note('E4')

        self.assertEqual(smaller(part_notes, a4, e4), e4)

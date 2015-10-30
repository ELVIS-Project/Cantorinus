import unittest
from mode_finder import *
import music21
from vis.analyzers.indexers import noterest

class ModeFinderTest(unittest.TestCase):
    '''
    Classes also contain docstrings, even if they are out of the box unit tests.
    '''
    def setUp(self):
        '''
        The setUp() does ...
        '''
        piece = 'music/christlag.mei'
        global the_score
        the_score = music21.converter.parse(piece)
        the_notes = noterest.NoteRestIndexer(the_score).run()
        global part_notes
        part_notes = the_notes['noterest.NoteRestIndexer']['0'].tolist()

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
        '''
        The test_range_type() function tests the range_type function by equality.
        '''
        self.assertEqual(range_type(part_notes, p_range, fin), 'authentic')

    def test_species(self):
        '''
        The test_species() function tests the species() function by equality.
        '''
        sp = ['T', 'S', 'T', 'T'], ['T', 'S', 'T']
        d4 = music21.note.Note('D4')
        r_type = 'authentic'
        self.assertEqual(species(part_notes, d4, r_type), sp)

    def test_characteristic(self):
        '''
        The test_characteristic() function tests the characteristic function 
        by testing for equality.
        '''
        self.assertEqual(characteristic(the_score), 'A')

    def test_smaller(self):
        '''
        The test_smaller() function tests the smaller() function by equality.
        '''
        a4 = music21.note.Note('A4')
        e4 = music21.note.Note('E4')

        self.assertEqual(smaller(part_notes, a4, e4), e4)

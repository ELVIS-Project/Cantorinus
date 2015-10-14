import unittest
import mode_finder
import music21
from vis.analyzers.indexers import noterest


class ModeFinderTest(unittest.TestCase):

    part_notes = 0
    the_score = 0

    def setUp(self):

        piece = 'music/christlag.mei'
        global the_score
        the_score = music21.converter.parse(piece)
        the_notes = noterest.NoteRestIndexer(the_score).run()
        global part_notes
        part_notes = the_notes['noterest.NoteRestIndexer']['0'].tolist()

    def test_finalis(self):

        d4 = music21.note.Note('D4')
        self.assertEqual(mode_finder.finalis(part_notes), d4)

    def test_pitch_range(self):

        part = the_score.parts[0]
        d4 = music21.note.Note('D4')
        e5 = music21.note.Note('E5')
        self.assertEqual(mode_finder.pitch_range(part), (d4, e5))

    def test_species(self):

        sp = ['T', 'S', 'T', 'T'], ['T', 'S', 'T']
        d4 = music21.note.Note('D4')
        r_type = 'authentic'
        self.assertEqual(mode_finder.species(part_notes, d4, r_type), sp)

    def test_characteristic(self):

        self.assertEqual(mode_finder.characteristic(part_notes), 'A')

    def test_smaller(self):

        a4 = music21.note.Note('A4')
        e4 = music21.note.Note('E4')

        self.assertEqual(mode_finder.smaller(part_notes, a4, e4), e4)

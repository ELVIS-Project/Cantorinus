import music21 as m
from vis.models.indexed_piece import IndexedPiece
from vis.analyzers.indexers import noterest, offset, interval


def final(part):

    last = len(part) - 1

    fin = m.note.Note(part[last])
    # print fin.nameWithOctave
    return fin


def pitch_range(part, fin):

    p = m.analysis.discrete.Ambitus()
    # print p.getSolution(part)
    # print p.getPitchSpan(part)


def species(part, fin):

    notes = []

    if "Rest" in part:
        while "Rest" in part:
            part.remove("Rest")

    for note in part:
        notes.append(m.note.Note(note).name)

    notes = sorted(list(set(notes)))

    ind = notes.index(fin.name)
    octave = []
    new = []

    for x in range(ind, len(notes), 1):
        new.append(notes[x])
    for x in range(0, ind, 1):
        new.append(notes[x])

    octv = 4

    for pitch in new:

        if pitch == 'C':
            octv += 1

        n = m.note.Note(pitch)
        n.octave = octv
        octave.append(n)

    n = m.note.Note(octave[0].name)
    n.octave = octv
    octave.append(n)

    intervals = []
    for x in range(len(octave)-1):

        intv = m.interval.Interval(octave[x], octave[x+1])
        intervals.append(intv)

    print intervals



# def characteristic():


def main():

    piece = 'Cantorinus/Rules/music/lhomme_arme.mei'

    the_score = m.converter.parse(piece)
    the_notes = noterest.NoteRestIndexer(the_score).run()

    for x in range(len(the_score.parts)):

        part_notes = the_notes['noterest.NoteRestIndexer'][str(x)].tolist()
        fin = final(part_notes)
        pitch_range(the_score.parts[x], fin)
        species(part_notes, fin)


if __name__ == '__main__':
    main()
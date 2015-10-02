import music21
from vis.analyzers.indexers import noterest


def final(part):
    '''
    Write documentation comments here. That way they are available
    via the final.__doc__ string function or the help(final) function. 
    We added this to the [code guidelines](https://ddmal.music.mcgill.ca/lab-coding-guidelines).

    So here:
    The final function finds and returns note object of the last 
    note in a part.
    '''
    if "Rest" in part:
        while "Rest" in part:
            part.remove("Rest")

    last = len(part) - 1

    fin = music21.note.Note(part[last])
    return fin


# returns note names of the upper and lower most notes in the part
# can also return range (i.e. M11)?
def pitch_range(part):

    if "Rest" in part:
        while "Rest" in part:
            part.remove("Rest")

    p = music21.analysis.discrete.Ambitus()
    p_range = p.getPitchSpan(part)
    return p_range[0].nameWithOctave, p_range[1].nameWithOctave


def _merge_sort(notes):

    if len(notes) <= 1:
        return notes

    left = []
    right = []

    mid = len(notes)/2

    for x in range(0, mid, 1):
        left.append(notes[x])

    for x in range(mid, len(notes), 1):
        right.append(notes[x])

    left = _merge_sort(left)
    right = _merge_sort(right)

    return _merge(left, right)


def _merge(left, right):

    result = []

    l = 0
    r = 0
    short = 0

    if len(left) < len(right):
        short += len(left)

    else:
        short += len(right)

    while l < short and r < short:

        if music21.interval.getAbsoluteLowerNote(left[l], right[r]) == left[l]:
            result.append(left[l])
            l += 1

        else:
            result.append(right[r])
            r += 1

    if l < len(left):
        while l < len(left):
            result.append(left[l])
            l += 1

    if r < len(right):
        while r < len(right):
            result.append(right[r])
            r += 1

    return result


# finds the species of fourths and fifths used in the mode of the piece/part
def species(part, fin):

    if "Rest" in part:
        while "Rest" in part:
            part.remove("Rest")

    notes = []

    for note in part:

        note = music21.note.Note(note)

        new = True
        for x in range(len(notes)):
            if notes[x].nameWithOctave == note.nameWithOctave:
                new = False

        if new:
            notes.append(note)

    notes = _merge_sort(notes)

    split = notes.index(fin)

    fifth = []
    fourth = []

    for x in range(split, split+4, 1):
        intv = music21.interval.Interval(notes[x], notes[x+1])
        if intv.name == 'M2':
            intv = 'T'

        elif intv.name == 'm2':
            intv = 'S'

        fifth.append(intv)
        notes[x] = 0

    # right now fourth only works if the range is exactly the range of the mode
    # extra notes aren't being taken into account yet
    for x in range(len(notes)-1):
        if notes[x] is not 0 and notes[x+1] is not 0:
            intv = music21.interval.Interval(notes[x], notes[x+1])
            if intv.name == 'M2':
                fourth.append('T')

            elif intv.name == 'm2':
                fourth.append('S')

    my_species = (fifth, fourth)
    return my_species


# characteristic currently only finds the most frequently occurring note in the piece
def characteristic(part):

    note_freq = {}

    for note in part:

        if note is 'Rest':
            pass
        else:
            note = music21.note.Note(note)

        if note.name in note_freq:
            note_freq[note.name] += 1
        else:
            note_freq[note.name] = 1

    return max(note_freq, key=note_freq.get)

# a work in progress: picks the mode out of the list.
# adds "hypo" if in opposite order?
def mode(my_species):

    modes = {
        'dorian': (['T', 'S', 'T', 'T'], ['T', 'S', 'T']),
        'phrygian': (['S', 'T', 'T', 'T'], ['S', 'T', 'T']),
        'lydian': (['T', 'T', 'T', 'S'], ['T', 'T', 'S']),
        'mixolydian': (['T', 'T', 'S', 'T'], ['T', 'S', 'T']),
        'aeolian': (['T', 'S', 'T', 'T'], ['S', 'T', 'T']),
        'ionian': (['T', 'T', 'S', 'T'], ['T', 'T', 'S'])
    }

    for each in modes:
        if my_species == modes[each]:
            print each


def main():

    piece = 'Cantorinus/Rules/music/lhomme_arme.mei'
    piece1 = 'Cantorinus/Rules/music/kyrie_cumjubilo.mei'
    piece2 = 'Cantorinus/Rules/music/kyrie_deangelis.mei'
    piece3 = 'Cantorinus/Rules/music/christlag.mei'

    pieces = [piece, piece1, piece2, piece3]

    for piece in pieces:

        print piece

        the_score = music21.converter.parse(piece)
        the_notes = noterest.NoteRestIndexer(the_score).run()

        for x in range(len(the_score.parts)):

            part_notes = the_notes['noterest.NoteRestIndexer'][str(x)].tolist()

            fin = final(part_notes)
            p_range = pitch_range(the_score.parts[x])
            my_species = species(part_notes, fin)
            char = characteristic(part_notes)

            print 'final: ', fin.nameWithOctave
            print 'range: ', p_range
            print 'species: ', my_species
            print 'characteristic note: ', char

            mode(my_species)


if __name__ == '__main__':
    main()

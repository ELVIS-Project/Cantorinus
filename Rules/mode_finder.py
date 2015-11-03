import music21
from vis.analyzers.indexers import noterest
import csv

def finalis(part):
    """
    The finalis() function is modeled after Peter Schubert's first rule. 
    If a line ends on:
    - D => first or second mode. 
    - E => third or fourth mode.
    - F => fifth or sixth mode.
    - G => seventh or eighth mode.
    - A => ninth or tenth mode.
    - C => eleventh or twelfth mode.
    The 'part' argument is a part that has already been parsed by (1)
    music21, and (2) the noterest indexer of the VIS-Framework. For
    example if the indexed parts were called the_notes, then the 
    following statement would be passed in for (here) the (soprano) part
    as part:
    the_notes['noterest.NoteRestIndexer']['0'].tolist()
    """
    
    if "Rest" in part:
        while "Rest" in part:
            part.remove("Rest")

    # Finding the last event in a part.
    last = len(part) - 1

    return music21.note.Note(part[last])

def pitch_range(part):
    """
    The pitch_range() function is modeled after Peter Schubert's second 
    rule:
    Ambitus    => Range of PCs within a line; spans an octave.
    Authentic  => The range includes PCs an octave above the finalis 
                  (located at the bottom of the ambitus).
    Plagal     => The range includes PCs an octave above the fourth below
                  below the finalis. The finalis is within the middle of
                  the ambitus.
    Excessive  => If range of PCs in a line spans > octave.
    Mixed      => If range of PCs in a line spans both authentic and 
                  plagal ranges.
    Incomplete => If range of PCs in a line spans < octave.
    """
    
    if "Rest" in part:
        while "Rest" in part:
            part.remove("Rest")

    p = music21.analysis.discrete.Ambitus()
    p_range = p.getPitchSpan(part)
    return p_range[0], p_range[1]

def range_type(part, p_range, fin):
    ''' 
    Even helper functions need documentation strings.
    '''
    intv = music21.interval.Interval(p_range[0], p_range[1])

    if fin in p_range:
        return 'authentic'

def _merge_sort(notes):
    '''
    Even helper functions need documentation strings.
    '''
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

    lst = len(left)-1

    if music21.interval.getAbsoluteLowerNote(left[lst], right[0]) == left[lst]:
        left.extend(right)
        return left

    return _merge(left, right)


def _merge(left, right):
    '''
    Oh, hello another function without a documentation string :(.
    '''
    result = []

    while len(left) > 0 and len(right) > 0:
        if music21.interval.getAbsoluteLowerNote(left[0], right[0]) == left[0]:
            result.append(left[0])
            left.remove(left[0])

        else:
            result.append(right[0])
            right.remove(right[0])

    if len(left) > 0:
        result.extend(left)

    if len(right) > 0:
        result.extend(right)

    return result


# The species of fourths and fifths. The types ('species') of fourth and fifth
# are numbered according to the positions of the semitones and tones enclosed
# within them (T = whole tone, S = semitone). For instance, the TTST fifth is
# called a 'fourth species fifth' and it occurs in two locations in the natural
# diatonic system (some species of interval only occur in one location). When a
# species of interval is characteristic of more than one mode, the whole octave
# must be examined to determine the mode. The species of fourth and fifth give
# a mode its 'sound,' so you should learn to sing the different species and to
# identify them aurally. The end points of the various species of interval can
# be stressed by skipping to and from them or by using them as turning points
# in a melody.

def species(part, fin, r_type):
    '''
    Another missing docstring.
    '''
    notes = spec_prep(part)

    fifth = []
    start = notes.index(fin)
    stop = start + 4

    for note in notes:

        if music21.interval.Interval(note, fin) == 'P5':
            stop = notes.index(note)

    for x in range(start, stop+1, 1):

        fifth.append(notes[x])

    fourth = []

    if r_type == 'authentic':

        f_start = stop
        f_stop = len(notes)

        for note in notes:
            if music21.interval.Interval(fin, note).name == 'P8':
                f_stop = notes.index(note) + 1

    else:

        f_start = start - 4
        f_stop = start

    for x in range(f_start, f_stop, 1):
        fourth.append(notes[x])

    fif_intv = []
    fou_intv = []

    for x in range(len(fifth)-1):
        f_intv = music21.interval.Interval(fifth[x], fifth[x+1])
        if f_intv.name == 'm2':
            fif_intv.append('S')
        elif f_intv.name == 'M2':
            fif_intv.append('T')

    for x in range(len(fourth)-1):
        f_intv = music21.interval.Interval(fourth[x], fourth[x+1])
        if f_intv.name == 'm2':
            fou_intv.append('S')
        elif f_intv.name == 'M2':
            fou_intv.append('T')

    return fif_intv, fou_intv


def spec_prep(part):
    '''
    Hello, my name is spec_prep() function, and I'm missing a docstring.
    '''
    notes = []

    for note in part:

        if note == "Rest":
            pass
        else:
            note = music21.note.Note(note)

            if note in notes:
                pass
            else:
                notes.append(note)

    notes = _merge_sort(notes)

    rep = []

    for x in range(len(notes)-1):

        if notes[x].name[0] == notes[x+1].name[0]:
            rep.append(smaller(part, notes[x], notes[x+1]))

    for note in rep:
        notes.remove(note)

    return notes


def smaller(part, note1, note2):
    '''
    The smaller() function also needs a document string.
    '''

    note1_tally = 0
    note2_tally = 0

    for note in part:
        if note == note1.name:
            note1_tally += 1

        elif note == note2.name:
            note2_tally += 1

    if note1_tally < note2_tally:
        return note1

    else:
        return note2


# Characteristic notes. The end points of the characteristic species of fourth
# and fifth are the characteristic notes of the mode. They are always the final
# and the fifth above (or the fourth below) the final. Thus if we hear or see a
# melody that is continually emphasizing the notes E and B, we can be sure that
# melody is either in the Phrygian mode or the Hypophrigian.


def characteristic(part):
    """
    characteristic() finds and returns the 'characteristic' note, a note that
    occurs often and has the longest total duration of being played
    """

    notes = part.flat.getElementsByClass(music21.note.Note)

    note_dict = {}
    note_freq = {}

    for note in notes:
        if note.name in note_dict:
            note_dict[note.name] += note.duration.quarterLength
            note_freq[note.name] += 1

        else:
            note_dict[note.name] = note.duration.quarterLength
            note_freq[note.name] = 1

    total = note_freq

    for note in total:
        total[note] += note_dict[note]

    return max(total, key=total.get)


def main():
    '''
    Even the main function should have a documentation string.
    '''
    
    place = 'Cantorinus/Rules/music/'

    pieces = [
        'lhomme_arme',
        'kyrie_cumjubilo',
        'kyrie_deangelis',
        'christlag',
        'kyrie_dedominica',
        'la_spagna',
        'vater_unser',
        'da_jesus'
    ]

    for piece in pieces:

        the_score = music21.converter.parse(place + piece + '.mei')
        the_notes = noterest.NoteRestIndexer(the_score).run()

        # currently assuming that the piece only has one part
        part_notes = the_notes['noterest.NoteRestIndexer']['0'].tolist()

        fin = finalis(part_notes)
        p_range = pitch_range(the_score.parts[0])
        p_range = p_range[0], p_range[1]
        r_type = range_type(part_notes, p_range, fin)

        output = 'Cantorinus/Rules/output/'

        with open(output + piece + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'finalis',
                'pitch range',
                'range type',
                'species',
                'characteristic note'
            ])
            writer.writerow([
                fin.name,
                p_range,
                r_type,
                species(part_notes, fin, r_type),
                characteristic(the_score)
            ])


if __name__ == '__main__':
    main()

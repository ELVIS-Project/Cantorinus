import music21
from vis.analyzers.indexers import noterest


# Rule 1: The final note in a melodic line. If the line ends on D, the mode is
# first or second; E, third or fourth; F, fifth or sixth; G, seventh or eighth;
# A, ninth or tenth; C, eleventh or twelfth. Each mode also has a Greek name.


def finalis(part):

    """
    The finalis() function finds and returns a note object of the last note in
    a part.
    """
    if "Rest" in part:
        while "Rest" in part:
            part.remove("Rest")

    last = len(part) - 1

    fin = music21.note.Note(part[last])
    return fin


# Rule 2: The range of the line. It is normally an octave, built either above
# the final or above the fourth below the final. The former is the range of the
# authentic, add-numbered modes; the latter the plagal, or even-numbered modes.
# In the Greek nomenclature, the names of the plagal modes begin with the prefix
# 'hypo-' ('below'). The last note (final) in a plagal melody lies in the
# middle of the range; in an authentic melody, at the bottom. In practice,
# the modal octave may be exceeded by a step at either end. If the melody goes
# farther than that, the mode is called 'excessive'; if the melody covers both
# the plagal and authentic ranges, its mode is said to be 'mixed'; if the melody
# covers less than an octave, it is called 'incomplete.'


def pitch_range(part):
    """
    The pitch_range() function returns note names of the upper and lower most
    notes in the part.
    """
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

def smaller(part, note1, note2):

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


def species(part, fin):
    """
    finds the species of fourths and fifths used in the mode of the piece/part
    """

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

    print(notes)

    # smallish = []
    # for x in range(len(notes)):
    #     for y in range(x, len(notes), 1):
    #         if notes[x].name[0] == notes[y].name[0]:
    #             small = smaller(part, notes[x], notes[y])
    #             print small
    #             smallish.append(small)
    #
    # print smallish
    # for small in smallish:
    #     notes.remove(small)

    # find the species of fifth based on where the final is
    my_fin = notes.index(fin)

    species_fifth = []
    species_fourth = []

    for note in notes:
        if music21.interval.Interval(note, fin).name == 'P5':
            print(fin), (note)
            end = notes.index(note)

    smalls = []
    for x in range(len(notes)-1):
        if notes[x].name[0] == notes[x+1].name[0]:
            small = smaller(part, notes[x], notes[x+1])
            smalls.append(small)

    for small in smalls:
        notes.remove(small)

    notes = _merge_sort(notes)

    for x in range(my_fin, end, 1):
        intv = music21.interval.Interval(notes[x], notes[x+1])
        print notes[x], notes[x+1]
        print intv.name
        if intv.name == 'M2':
            intv = 'T'
            species_fifth.append(intv)

        elif intv.name == 'm2':
            intv = 'S'
            species_fifth.append(intv)

        notes[x] = 0

    fifth = 0
    last = 0

    if my_fin < 3:

        fifth = my_fin + 4
        last = fifth + 3

    elif my_fin >= 3:

        fifth = my_fin - 3
        last = my_fin

    my_species = (species_fifth, species_fourth)
    return my_species


# Characteristic notes. The end points of the characteristic species of fourth
# and fifth are the characteristic notes of the mode. They are always the final
# and the fifth above (or the fourth below) the final. Thus if we hear or see a
# melody that is continually emphasizing the notes E and B, we can be sure that
# melody is either in the Phrygian mode or the Hypophrigian.


def characteristic(part):
    """
    characteristic() finds and returns the most frequently occurring note
    """

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


def mode(fin, p_range, my_species, char):

    mode_species = {
        'dorian': (['T', 'S', 'T', 'T'], ['T', 'S', 'T']),
        'phrygian': (['S', 'T', 'T', 'T'], ['S', 'T', 'T']),
        'lydian': (['T', 'T', 'T', 'S'], ['T', 'T', 'S']),
        'mixolydian': (['T', 'T', 'S', 'T'], ['T', 'S', 'T']),
        'aeolian': (['T', 'S', 'T', 'T'], ['S', 'T', 'T']),
        'ionian': (['T', 'T', 'S', 'T'], ['T', 'T', 'S'])
    }

    for each in mode_species:
        if my_species == mode_species[each]:
            print('species thinks: '), (each)

    mode_finalis = {
        'D': 'dorian',
        'E': 'phrygian',
        'F': 'lydian',
        'G': 'mixolydian',
        'A': 'aeolian',
        'C': 'ionian'
    }

    mode_charac = {
        'D': ('dorian', 'mixolydian'),
        'E': ('phrygian', 'aeolian'),
        'F': 'lydian',
        'G': ('mixolydian', 'ionian'),
        'A': ('aeolian', 'dorian'),
        'C': ('ionian', 'lydian')
    }

    if fin.name in mode_finalis:
        print('finalis thinks: '), (mode_finalis[fin.name])

    if char in mode_charac:
        print('characteristic note thinks: '), (mode_charac[char])
        

def main():

    pieces = {
        'Cantorinus/Rules/music/lhomme_arme.mei': 'mixolydian',
        'Cantorinus/Rules/music/kyrie_cumjubilo.mei': 'dorian & hypodorian',
        'Cantorinus/Rules/music/kyrie_deangelis.mei': 'lydian',
        'Cantorinus/Rules/music/christlag.mei': 'dorian',
        'Cantorinus/Rules/music/kyrie_dedominica.mei': 'aeolian',
        'Cantorinus/Rules/music/la_spagna.mei': 'dorian',
        'Cantorinus/Rules/music/vater_unser.mei': 'dorian',
        'Cantorinus/Rules/music/da_jesus.mei': 'phrygian'
    }

    for piece in pieces:

        print(piece)

        the_score = music21.converter.parse(piece)
        the_notes = noterest.NoteRestIndexer(the_score).run()

        for x in range(len(the_score.parts)):

            part_notes = the_notes['noterest.NoteRestIndexer'][str(x)].tolist()

            fin = finalis(part_notes)
            p_range = pitch_range(the_score.parts[x])
            my_species = species(part_notes, fin)
            char = characteristic(part_notes)

            # print('actual: '), (pieces[piece])
            # print('final: '), (fin.nameWithOctave)
            # print('range: '), (p_range)
            # print('species: '), (my_species)
            # print('characteristic note: '), (char)
            #
            # mode(fin, p_range, my_species, char)


if __name__ == '__main__':
    main()
## midi_query
Query MIDI datasets for matching key, time signature &amp; chord progression

### Install Dependencies

`python setup.py install`

### Tests

`python -m unittest discover -s tests`

### Add Dataset

Add your dataset of .mid or .midi files to the `midi_query/datasets` directory. Nested directories are supported.

### Run Application

`python midi_query/query.py --chords 'Cmaj7,Emin7,Dmin7,Cmaj7' --key 'c'`

Find your results in the midi_query/output directory.

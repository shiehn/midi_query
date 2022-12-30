## midi_query
Query MIDI datasets for matching key, time signature &amp; chord progression

### Install Dependencies

`cd midi_query` (go into the root of the repo) than run:

`python setup.py install`

### Tests

`cd midi_query` (go into the root of the repo) than run:

`python -m unittest discover -s tests -t midi_query`

### Add Dataset

Add your dataset of .mid or .midi files to the `midi_query/datasets` directory. Nested directories are supported.

### Run Application

`cd midi_query` (go into the root of the repo) than run:

`python midi_query/query.py --chords 'Cmaj7,Emin7,Dmin7,Cmaj7' --key 'c'`

Find your results in the midi_query/output directory.

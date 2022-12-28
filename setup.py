from setuptools import setup

setup(
    name='midi_query',
    version='0.0.1',
    description='Query MIDI Dataset',
    url='https://github.com/shiehn/midi_query',
    author='Stephen Hiehn',
    author_email='stevehiehn@gmail.com',
    license='GPL v3',
    packages=['midi_query'],
    install_requires=['MIDIUtil>=1.2.1',
                      'python-rtmidi>=1.4.9',
                      'mido>=1.2.10'
                      ],

    classifiers=[
        'Programming Language :: Python :: 3'
    ],
)

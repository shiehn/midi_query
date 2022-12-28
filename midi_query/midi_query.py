import time
import rtmidi
import mido


def print_midi_file_info():
    midiout = rtmidi.MidiOut()
    midiout.open_virtual_port('foo')
    # note_on = [0x90, 60, 112]
    # midiout.send_message(note_on)

    port = mido.open_output(name='foo', virtual=True)

    mid = mido.MidiFile('datasets/ballade1.mid', clip=True)
    for msg in mid.play():
        port.send(msg)


def main():
    # midiout = rtmidi.MidiOut()
    # available_ports = midiout.get_ports()
    #
    # if available_ports:
    #     midiout.open_port(0)
    # else:
    #     midiout.open_virtual_port("My virtual output")

    print_midi_file_info()

    # degrees = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    # track = 0
    # channel = 0
    # time = 0  # In beats
    # duration = 1  # In beats
    # tempo = 60  # In BPM
    # volume = 100  # 0-127, as per the MIDI standard
    #
    # MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # # automatically)
    # MyMIDI.addTempo(track, time, tempo)
    #
    # for i, pitch in enumerate(degrees):
    #     MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
    #
    # with open("major-scale.mid", "wb") as output_file:
    #     MyMIDI.writeFile(output_file)


if __name__ == "__main__":
    main()

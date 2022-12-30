from mido import MidiFile, MidiTrack

from midi_query.midi_info import MidiInfo


class Extractor(object):
    def __init__(self, minfo: MidiInfo):
        if minfo is None:
            print('ERROR: midi_info is None')
            raise ValueError('midi_info cannot be None')
        self.midi_info = minfo

    def extract(self, start_index: int, num_of_bars: int = 4) -> MidiInfo:

        ticks_at_start = start_index * self.midi_info.get_ticks_per_beat() * 4
        ticks_at_end = ticks_at_start + (num_of_bars * self.midi_info.get_ticks_per_beat() * 4)

        midi_clip = MidiFile(type=1, ticks_per_beat=self.midi_info.get_ticks_per_beat())
        track = MidiTrack()
        midi_clip.tracks.append(track)

        current_time = 0.0
        for msg in self.midi_info.get_merged_track():
            if 'time' in msg.dict():
                current_time = current_time + msg.time

                if msg.type == 'note_on' or msg.type == 'note_off':
                    if current_time >= ticks_at_start and current_time < ticks_at_end:
                        track.append(msg)

        return MidiInfo(midi_file=midi_clip)

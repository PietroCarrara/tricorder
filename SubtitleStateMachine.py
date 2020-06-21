import srt

class SubtitleStateMachine:

    def __init__(self):
        self.subs = []
        self.string = ''
        self.start = None
        self._index = 0

    def say(self, string, time):
        string = srt.make_legal_content(string.strip())

        if string == '':
            self.flush(time)
            return

        if string == self.string:
            return

        self.flush(time)
        self.string = string
        self.start = time

    def flush(self, time):
        if self.string == '' or self.start is None:
            return

        self._index += 1
        self.subs.append(srt.Subtitle(self._index, self.start, time, self.string))

        print('{} --> {}'.format(self.start, time))
        print('"{}"'.format(self.string))
        print()

        self.string = ''
        self.start = None

    def get_subs(self):
        return srt.compose(self.subs)
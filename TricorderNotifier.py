class TricorderNotifier:
    def notify_frame(self, frame, completion):
        pass

    def notify_subtitle(self, sub):
        pass

    def notify_done(self):
        pass


class CLINotifier(TricorderNotifier):
    def notify_frame(self, frame, completion):
        pass

    def notify_subtitle(self, sub):
        pass

    def notify_done(self):
        pass


class GUINotifier(TricorderNotifier):
    def __init__(self, app):
        self.app = app

        self.subs = []

    def notify_frame(self, frame, completion):
        self.app.notify_frame.emit(frame, completion)

    def notify_subtitle(self, sub):
        self.subs.append(sub)
        self.app.notify_subtitles.emit(self.subs)

    def notify_done(self):
        pass

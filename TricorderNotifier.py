class TricorderNotifier:
    def notify_frame(self, frame, contents):
        pass

    def notify_progress(self, currFrame, totalFrames):
        pass

    def notify_time(self, time):
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

    def notify_frame(self, frame, contents):
        self.app.notify_frame.emit(frame)
        self.app.notify_display.emit(contents)

    def notify_time(self, time):
        pass

    def notify_progress(self, currFrame, totalFrames):
        self.app.notify_completion.emit(currFrame/totalFrames)

    def notify_subtitle(self, sub):
        self.app.notify_subtitles.emit(sub)

    def notify_done(self):
        pass

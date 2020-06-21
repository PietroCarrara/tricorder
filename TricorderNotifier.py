class TricorderNotifier:
    def notify_frame(self, frame, index):
        pass

    def notify_subtitle(self, frame):
        pass

    def notify_done(self):
        pass

class CLINotifier(TricorderNotifier):
    def notify_frame(self, frame, index):
        pass

    def notify_subtitle(self, frame, index):
        pass

    def notify_done(self):
        pass

class GUINotifier(TricorderNotifier):
    def __init__(self, frame, label, app):
        self.frame = frame
        self.label = label
        self.app = app

    def notify_frame(self, frame, index):
        pass

    def notify_subtitle(self, frame, index):
        pass

    def notify_done(self):
        pass
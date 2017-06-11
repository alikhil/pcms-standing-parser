
from watchdog.events import FileSystemEventHandler

class FSEventHandler(FileSystemEventHandler):

    def __init__(self, on_event):
        self.on_event = on_event

    def on_any_event(self, event):
        print("some event happened: " + event.src_path + " " + event.event_type)
        if event.src_path.endswith(".xml"):
            self.on_event()

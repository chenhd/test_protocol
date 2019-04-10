from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import json


modify_data_dict = {}
with open("./modify_data.json") as f:
    modify_data_dict = json.load(f)

def get_modify_data():
    return modify_data_dict


class myFileSystemEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == "./modify_data.json":
            try:
                with open("./modify_data.json") as f:
                    data = json.load(f)
                    global modify_data_dict
                    modify_data_dict = data
                    
                print("reload ./modify_data.json")
                print(get_modify_data())
            except Exception as e:
                print("modify format error")
                pass

event_handler = myFileSystemEventHandler()
path = "."
observer = Observer()
observer.schedule(event_handler, path, recursive=False)
observer.start()
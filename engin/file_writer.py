import os
import json


class FileWriter:

    def __init__(self, data):
        self.data = data
        self.writing()

    def writing(self):
        file_name = os.path.join('log_data')
        data = {str(self.data[-1]): self.data[:-2]}
        with open(file_name, 'a') as f:
            json.dump(data, f, indent=2)


import os
import json


class FileWriter:

    def __init__(self, data):
        self.data = data
        self.writing()

    def writing(self):       
        file_name = os.path.join(f'log_data {self.data[-1]}.json')
        
        try:
           with open(file_name, "r") as f:
              data = json.load(f)

        except :
           data = {}

        key = str(self.data[-2])
        value = self.data[:-2]
        data[key] = value

        with open(file_name, "w") as f:
            json.dump(data, f, indent=2)

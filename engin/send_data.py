import requests
import os
from dotenv import load_dotenv
import uuid
from iwriter import IWriter
load_dotenv()

class SendData(IWriter):

    def __init__(self):
        self.url = os.getenv('API_URL')

    def writing(self, data):
        try:
            mac = ','.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)][::-1])
            data["mac"] = mac
            response = requests.post(f'{self.url}/send-data', json=data)
            return response.json()["commend"], response.json()['timer'] 
        except Exception as e:
            print('Error sending data: ', e)
    

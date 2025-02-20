import requests
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

class SendPing:

    def __init__(self):
        self.url = os.getenv('API_URL')
        self.mac = ','.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)][::-1])

    def send(self):
        response = requests.get(f'{self.url}/ping/{self.mac}')
        return response.json()['commend']
    

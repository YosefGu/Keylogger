import requests
import os
import uuid

class UpdateStatus:

    def __init__(self):
        self.url = os.getenv('API_URL')
        self.mac = ','.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)][::-1])


    def update_status_and_timer(self):
        try:
            data = {'status': False, 'timer': 0}
            requests.post(f'{self.url}/update-status/{self.mac}', json=data)
        except Exception as e:
            print('Error updating status: ', e)

from flask import Blueprint, request
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
backend_path = os.getenv('ROOT_PATH')

routes = Blueprint('Routes', __name__)

# sava data on serevr machine
@routes.route('/send-data', methods=['POST'])
def send_data():
    mac = request.json.get('mac')
    data = request.json.get('data')

    # folder for specific machine
    folder_path = f'{backend_path}/data/{mac}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # file for specific day
    date = datetime.now().strftime('%Y-%m-%d')
    file_name = os.path.join(f'{folder_path}/{date}.json')
    try:
        with open(file_name, "r") as f:
            old_data = json.load(f)
    except FileNotFoundError:
        old_data = {}

    # adding new data for specific minute 
    time = datetime.now().strftime('%H:%M:%S')
    old_data[time] = data
    with open(file_name, 'w') as f:
        json.dump(old_data, f, indent=2)
    
    # status machin - check for commend to stop
    with open(f'{backend_path}/machins.json') as f:
        machins = json.load(f)
    return {'commend': machins[mac]['status']}, 200


# get machines name
@routes.route('/machines', methods=['GET'])
def get_machines():
    with open(f'{backend_path}/machins.json') as f:
        data = json.load(f)
    return list(data.keys())

# get machine data
@routes.route('/machine/<id>', methods=['GET'])
def get_machine_data(id):
    files = os.listdir(f'{backend_path}/data/{id}')
    data = []
    for file in files:
        file_path = f'{backend_path}/data/{id}/{file}'
        with open(file_path, 'r') as f:
            file_data = json.load(f)
            for key in file_data:
                decrypted_list = xor_decryption(file_data[key])
                data.append(decrypted_list) 
    return {"data": data}, 200
  

# check for status machin
@routes.route('/ping/<mac>', methods=['GET'])
def get_status(mac):
    with open(f'{backend_path}/machins.json', 'r') as f:
        old_data = json.load(f)
    if mac in old_data:
        return {'commend' : old_data[mac]['status']}
    
    old_data[mac] = {'status': False}
    with open(f'{backend_path}/machins.json', 'w') as f:
        json.dump(old_data, f, indent=4)
    return {'commend' : False}

def xor_decryption(data):
    password = 42
    xored_string = ""
    for char in data:
        if char == " ":
            xored_string += " "
        else:    
            xored_character = ord(char) ^ password
            xored_string += chr(xored_character)
    return xored_string
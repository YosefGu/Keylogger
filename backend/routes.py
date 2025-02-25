from flask import Blueprint, request,jsonify
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
    return {"machines" : list(data.keys())}

# get machine data
@routes.route('/machine/<id>', methods=['POST'])
def get_machine_data(id):
    files = os.listdir(f'{backend_path}/data/{id}')
    data = []
    for file in files:
        file_path = f'{backend_path}/data/{id}/{file}'
        with open(file_path, 'r') as f:
            file_data = json.load(f)
            for key in file_data:
                data.append(''.join(file_data[key]))
    return {"data": data}, 200
  

# check for status machine
@routes.route('/ping/<mac>', methods=['POST'])
def get_status(mac):
    file_path = f'{backend_path}/machins.json'
    try:
        with open(file_path, 'r') as f:
            machines = json.load(f)
    except FileNotFoundError:
        machines = {}

    return {'commend': machines.get(mac, {}).get('status', False)}

# updating of status machine
@routes.route('/update-status', methods=['POST'])
def update_status():
    mac = request.json.get('mac')
    status = request.json.get('status')

    file_path = f'{backend_path}/machins.json'
    
    try:
        with open(file_path, 'r') as f:
            machines = json.load(f)
    except FileNotFoundError:
        machines = {}

    if mac in machines:
        machines[mac]['status'] = status
    else:
        machines[mac] = {'status': status}

    with open(file_path, 'w') as f:
        json.dump(machines, f, indent=2)
    
    return jsonify({'message': f'Status updated for {mac}'}), 200

import os
import json
from flask import Blueprint, request, jsonify
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
backend_path = os.getenv('ROOT_PATH')

routes = Blueprint('Routes', __name__)

# sava data on serevr machine
@routes.route('/send-data', methods=['POST'])
def save_data():
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
    return {'commend': machins[mac]['status'],'timer': machins[mac]['timer']}, 200


# get machines name
@routes.route('/machines', methods=['GET'])
def get_machines():
    with open(f'{backend_path}/machins.json') as f:
        data = json.load(f)
    return list(data.keys())

# get machine data
@routes.route('/machine/<mac>', methods=['GET'])
def get_machine_data(mac):
    files = os.listdir(f'{backend_path}/data/{mac}')
    data = []
    for file in files:
        file_path = f'{backend_path}/data/{mac}/{file}'
        with open(file_path, 'r') as f:
            file_data = json.load(f)
            for key in file_data:
                data.append(''.join(file_data[key]))
                
    return {"data": data}, 200
  

# check for status machin
@routes.route('/ping/<mac>', methods=['GET'])
def get_status(mac):
    with open(f'{backend_path}/machins.json', 'r') as f:
        old_data = json.load(f)
    if mac in old_data:
        return {'commend' : old_data[mac]['status'], 'timer' : old_data[mac]['timer']}
    
    old_data[mac] = {'status': False,'timer': 0}
    with open(f'{backend_path}/machins.json', 'w') as f:
        json.dump(old_data, f, indent=4)
    return {'commend' : False, 'timer': 0}

# get data by date and time
@routes.route('/machine-time/<mac>', methods=['GET'])
def get_data_by_date(mac):
    machine = mac
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    
    # converting string to datetime object
    start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    start_time = datetime.strptime(start_time, "%H:%M:%S").time()
    end_time = datetime.strptime(end_time, "%H:%M:%S").time()

    # filtering files by date
    all_files = os.listdir(f'{backend_path}/data/{machine}')
    files_in_range = []
    for file in all_files:
        try:
            file_date = datetime.strptime(file.replace(".json",""), "%Y-%m-%d").date()
            if start_date <= file_date <= end_date:
                files_in_range.append(file)
        except ValueError:
            continue

    
    # adding data maching to time start and end
    data = []
    for file in files_in_range:
        file_date = datetime.strptime(file.replace(".json",""), "%Y-%m-%d").date()

        file_path = f'{backend_path}/data/{machine}/{file}'
        with open(file_path, 'r') as f:
            file_data = json.load(f)
            for key in file_data:
                key_time = datetime.strptime(key, "%H:%M:%S").time()
                if file_date == start_date:
                    if key_time >= start_time:
                        data.append(''.join(file_data[key]))
                elif file_data == end_date:
                    if key_time <= end_time:
                        data.append(''.join(file_data[key]))
                else:
                    data.append(''.join(file_data[key]))
    return {"data": data}
  

# updating of status and time machine
@routes.route('/update-status/<mac>', methods=['POST'])
def update_status(mac):
    mac = mac
    status = request.json.get('status')
    timer = request.json.get('timer')

    file_path = f'{backend_path}/machins.json'
    
    try:
        with open(file_path, 'r') as f:
            machines = json.load(f)
    except FileNotFoundError:
        machines = {}

    if mac in machines:
        machines[mac]['status'] = status
        machines[mac]['timer'] = timer
    else:
        machines[mac] = {'status': status, 'timer': 0}
    with open(file_path, 'w') as f:
        json.dump(machines, f, indent=2)
    
    return jsonify({'message': f'Status updated for {mac}'}), 200
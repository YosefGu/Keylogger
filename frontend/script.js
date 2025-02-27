const url = "http://127.0.0.1:5000";

// get machines
function fetchMachines() {
    fetch(`${url}/machines`)
        .then(response => response.json())
        .then(data => updateMachineSelects(data.machines))
        .catch(error => console.error('Error fetching machines:', error));
}

// update machine
function updateMachineSelects(machines) {
    const machineSelects = document.querySelectorAll('.select-machin');
    machineSelects.forEach(select => {
        select.innerHTML = "";
        machines.forEach((machine, index) => {
            const option = document.createElement('option');
            option.value = machine;
            option.textContent = `Machine ${index + 1}`;
            select.appendChild(option);
        });
    });
}

// update status
function updateMachineStatus(machine, status, timer = 0) {
    fetch(`${url}/update-status/${machine}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, timer })
    })
    .catch(error => console.error('Error updating machine status', error));
}


document.addEventListener('DOMContentLoaded', function () {
    fetchMachines();

    // off time-work when is NON-STOP
    document.getElementById('non-stop-checkbox').addEventListener('change', function () {
        document.getElementById('time-work').disabled = this.checked;
    });
});

// click on start
document.querySelector('.start-button').addEventListener('click', function () {
    const selectedMachine = document.querySelector('.select-machin').value;
    const timeWorkInput = document.getElementById('time-work');
    const errorMessage = document.getElementById('error-message');
    const nonStopChecked = document.getElementById('non-stop-checkbox').checked;

    let timerValue = nonStopChecked ? 0 : parseInt(timeWorkInput.value, 10);

    if (!nonStopChecked && (isNaN(timerValue) || timerValue < 1 || timerValue > 9999)) {
        errorMessage.style.display = 'block';
        return;
    }

    errorMessage.style.display = 'none';
    updateMachineStatus(selectedMachine, true, timerValue);
});

// click on stop
document.querySelector('.stop-button').addEventListener('click', function () {
    const selectedMachine = document.querySelector('.select-machin').value;
    updateMachineStatus(selectedMachine, false);
});

// off select time whene is Show All Time
document.addEventListener('DOMContentLoaded', function () {
    const allTimeCheckbox = document.getElementById('all-time');
    const startTimeInput = document.getElementById('start-time');
    const endTimeInput = document.getElementById('end-time');

    allTimeCheckbox.addEventListener('change', function () {
        startTimeInput.disabled = this.checked;
        endTimeInput.disabled = this.checked;
    });
});

// show
document.getElementById('show-button').addEventListener('click', function () {
    const allTimeChecked = document.getElementById('all-time').checked;
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;
    const machine = document.getElementById('select-machin').value;
    const errorMessage = document.getElementById('show-error-message')

    if (!allTimeChecked && (startTime === "" || endTime === "")) {
        errorMessage.style.display = 'block';
        return;
    }

    let requestData = {};
    let requestUrl = allTimeChecked ? `${url}/machine/${machine}` : `${url}/machine-time/${machine}`;

    if (!allTimeChecked) {
        const startParts = startTime.split("T");
        const endParts = endTime.split("T");

        requestData = {
            start_date: startParts[0],
            end_date: endParts[0],
            start_time: startParts[1] + ":00",
            end_time: endParts[1] + ":00"
        };
    }

    fetch(requestUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        const machineDataDiv = document.getElementById('machine-data')
        if (data.data && data.data.length > 0) {
            machineDataDiv.innerHTML = `<p>${data.data.join(' ')}</p>`;
            machineDataDiv.style.display = 'block';

        } else {
            machineDataDiv.innerHTML = `<p>no data</p>`;
            machineDataDiv.style.display = 'block'
        }
    })
    .catch(error => console.error('Error fetching machine data:', error));
});
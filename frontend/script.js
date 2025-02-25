
const url =


function fetchMachines() {
    fetch('http://127.0.0.1:5000/machines')
    .then(response => response.json())
    .then(data => {console.log("Received machines",data);
     updateMachineSelects(data.machines);})
    .catch(error => console.error('Erorr fetching machines:',error));
    
}

function updateMachineSelects(machines) {
    const machineSelects = 
    document.querySelectorAll('.select-machin');
    machineSelects.forEach(select => {
        select.innerHTML = "" ;
        machines.forEach(machine => {
        const option = 
        document.createElement('option');
        option.value = machine ;
        option.textContent = machine ;
        select.appendChild(option);
        });
    });
}

function  updateMachineStatus(machine,status) {
    fetch('http://127.0.0.1:5000/update-status',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({mac:machine , status:status})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Machine' + machine + 'status update to' + status);
        })
        
        .catch(error => console.error('Error updating machine status',error))

}

document.querySelector('.start-button').addEventListener('click',function(){
    const selectdMachine = 
    document.querySelector('#select-machin').value;
    console.log('Starting machine:',selectdMachine);
    updateMachineStatus(selectdMachine,true);
});

document.querySelector('.stop-button').addEventListener('click',function(){
    const selectdMachine = 
    document.querySelector('#select-machin').value;
    console.log('Stopping machine:',selectdMachine);
    updateMachineStatus(selectdMachine,false);
})

document.addEventListener('DOMContentLoaded', function(){
    fetchMachines();
})
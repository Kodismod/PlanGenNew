
var point = 1
var loaded = false
document.querySelector(".switch_table").addEventListener('click', async () => {
    const schedule = await loadSchedule();
    create_table(schedule);
});


async function loadSchedule() {
    fetch('http://127.0.0.1:5000/getschedule')
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(text => {
        const data = JSON.parse(text);
        console.log(data);
        create_table(data);
    })
    .catch(error => console.error('Error:', error));
}

// Функция для добавления данных в таблицу
function create_table(data) {
    const tableBody = document.getElementById('schedule');

    if (!tableBody) {
        console.error('Элемент с id "schedule" не найден.');
        return;
    }
    tableBody.innerHTML = '';

    if(point == 1){
        for (const [time, places] of Object.entries(data)) {
            const row = document.createElement('tr');
    
            const timeCell = document.createElement('td');
            timeCell.textContent = time;
            row.appendChild(timeCell);
    
            const point1Cell = document.createElement('td');
            point1Cell.textContent = places['Точка 1'].join(', ') || 'Нет данных';
            row.appendChild(point1Cell);
    
            const point2Cell = document.createElement('td');
            point2Cell.textContent = "Бар";
            row.appendChild(point2Cell);
    
            tableBody.appendChild(row);
        }
        point = 2
    }
    else{
        for (const [time, places] of Object.entries(data)) {
            const row = document.createElement('tr');
    
            const timeCell = document.createElement('td');
            timeCell.textContent = time;
            row.appendChild(timeCell);
    
            const point1Cell = document.createElement('td');
            point1Cell.textContent = places['Точка 2'].join(', ') || 'Нет данных';
            row.appendChild(point1Cell);
    
            const point2Cell = document.createElement('td');
            point2Cell.textContent = "Зал";
            row.appendChild(point2Cell);
    
            tableBody.appendChild(row);
        }
        point = 1
    }
    
}







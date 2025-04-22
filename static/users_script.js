document.addEventListener("DOMContentLoaded", loadtable())


async function loadtable() {
    fetch('http://127.0.0.1:5000/loadusers')
    .then(response => {
        if (!response.ok) 
        {
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


function create_table(data){
    const tableBody = document.getElementById('user-table');

    if (!tableBody) {
        console.error('Элемент с id "user-table" не найден.');
        return;
    }

    tableBody.innerHTML = '';
    for (const[id, info] of Object.entries(data)) {
        const row = document.createElement('tr');
    
            const timeCell = document.createElement('td');
            timeCell.textContent = id;
            row.appendChild(timeCell);
    
            const point1Cell = document.createElement('td');
            point1Cell.textContent = info['Инициалы'];
            row.appendChild(point1Cell);
    
            const point2Cell = document.createElement('td');
            point2Cell.textContent = info['Code'];
            row.appendChild(point2Cell);
    
            tableBody.appendChild(row);

    }

    console.log("Успешно")
}
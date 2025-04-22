let scheduleData = {};

        // Функция для загрузки расписания с сервера
        async function loadSchedule() {
            try {
                const response = await fetch('http://127.0.0.1:5000/getschedule');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                scheduleData = data;
                updateJsonView();
            } catch (error) {
                console.error('Error loading schedule:', error);
                document.getElementById('jsonOutput').textContent = 'Ошибка загрузки данных: ' + error.message;
                document.getElementById('jsonOutput').className = '';
            }
        }

        // Функция для отправки изменений на сервер
        async function saveSchedule() {
            try {
                const response = await fetch('http://127.0.0.1:5000/updateschedule', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(scheduleData)
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                const result = await response.json();
                console.log('Schedule updated:', result);
                return true;
            } catch (error) {
                console.error('Error saving schedule:', error);
                return false;
            }
        }

        // Функция для обновления отображения JSON
        function updateJsonView() {
            const jsonOutput = document.getElementById('jsonOutput');
            jsonOutput.textContent = JSON.stringify(scheduleData, null, 2);
            jsonOutput.className = '';
        }

        // Функция для обработки формы
        async function handleSubmit(event) {
            event.preventDefault();
            
            const time = document.getElementById('timeSelect').value;
            const point = document.getElementById('pointSelect').value;
            const nameToRemove = document.getElementById('removeInput').value.trim();
            const nameToAdd = document.getElementById('addInput').value.trim();
            
            if (!nameToRemove && !nameToAdd) {
                alert('Введите хотя бы одно имя для удаления или добавления');
                return;
            }
            
            // Получаем данные для выбранного времени
            const timeData = scheduleData[time];
            if (!timeData) {
                alert('Данные для выбранного времени не найдены');
                return;
            }
            
            // Определяем точки, к которым нужно применить изменения
            const pointsToUpdate = point === 'all' ? Object.keys(timeData) : [point];
            
            // Удаляем имя из выбранных точек, если оно указано
            if (nameToRemove) {
                pointsToUpdate.forEach(point => {
                    if (timeData[point]) {
                        timeData[point] = timeData[point].filter(name => name !== nameToRemove);
                    }
                });
            }
            
            // Добавляем имя в выбранные точки, если оно указано
            if (nameToAdd) {
                pointsToUpdate.forEach(point => {
                    if (timeData[point]) {
                        if (!timeData[point].includes(nameToAdd)) {
                            timeData[point].push(nameToAdd);
                        }
                    }
                });
            }
            
            // Обновляем отображение JSON
            updateJsonView();
            
            // Сохраняем изменения на сервере
            const saveResult = await saveSchedule();
            if (!saveResult) {
                alert('Ошибка при сохранении изменений на сервере');
                return;
            }
            
            // Очищаем поля ввода
            document.getElementById('removeInput').value = '';
            document.getElementById('addInput').value = '';
            
            alert('Изменения применены и сохранены успешно!');
        }

        // Инициализация при загрузке страницы
        document.addEventListener('DOMContentLoaded', function() {
            // Загружаем данные с сервера
            loadSchedule();
            
            // Назначаем обработчик формы
            document.getElementById('submitButton').addEventListener('click', handleSubmit);
        });
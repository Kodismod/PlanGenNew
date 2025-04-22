document.getElementById('linkForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартную отправку формы
    
    const linkInput = document.getElementById('linkInput');
    const userInput = linkInput.value;
    const extractedId = get_id(userInput);
    
    alert("Успешно!");
    
    // Отправляем ID на сервер для сохранения в JSON
    fetch('/save_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: extractedId }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('ID успешно сохранён:', data);
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});



function get_id(url) {
    return url.split('/')[5];
}
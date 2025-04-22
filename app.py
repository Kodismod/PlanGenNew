from flask import Flask,render_template, request, jsonify
import json
import os
from table import process_table_to_json

app = Flask(__name__, static_folder="static", template_folder="templates")

filename = os.path.join(app.static_folder, 'data', 'schedule_local.json')

def save_schedule(schedule):
    """Сохраняет расписание в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    return render_template('Users.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/table')
def table():
    return render_template('Table.html')

@app.route('/schedule')
def schedule():
    return render_template('Schedule.html')

@app.route('/getschedule')
def getschedule():
    try:
        with open('static/data/schedule_local.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/loadusers')
def loadusers():
    try:
        with open('static/data/users_base.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/updateschedule', methods=['POST'])
def update_schedule():
    """Обновляет расписание на сервере"""
    try:
        # Получаем новые данные расписания из запроса
        new_schedule = request.get_json()
        
        if not new_schedule:
            return jsonify({"error": "No data provided"}), 400
        
        # Валидация данных (можно добавить более строгую проверку)
        if not isinstance(new_schedule, dict):
            return jsonify({"error": "Invalid schedule format"}), 400
        
        # Сохраняем новое расписание
        save_schedule(new_schedule)
        
        return jsonify({"status": "success", "message": "Schedule updated"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    
@app.route('/save_id', methods=['POST'])
def save_id():
    data = request.get_json()
    user_id = data.get('id')
    
    if not user_id:
        return jsonify({"error": "ID не предоставлен"}), 400
    
    # Путь к файлу /static/data/id.json
    file_path = os.path.join('static', 'data', 'id.json')
    
    # Создаем папки, если их нет
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Записываем ID в файл
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({"id": user_id}, f, ensure_ascii=False, indent=4)
    
    return jsonify({"success": True, "id": user_id})

@app.route('/save_new_base' , methods=['POST'])
def save_new_base():
    process_table_to_json()
    return jsonify({"status": "success", "message": "Base updated"})

if __name__ == '__main__':
    app.run(debug=True)
    

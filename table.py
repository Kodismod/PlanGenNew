import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from collections import defaultdict
from datetime import datetime, timedelta
from algor import generate_schedule
import os

path = "C:\\Users\\A L E K S\\Desktop\\PlanGen\\static\\data\\plangen.json"
# Настройка аутентификации
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
client = gspread.authorize(credentials)



def normalize_date(date_str):
    """Приводит дату к формату DD.MM"""
    try:
        # Удаляем все пробелы и лишние символы
        date_str = date_str.strip().replace(' ', '')
        
        # Пробуем разные форматы дат
        for fmt in ("%d.%m", "%d.%m.%Y", "%-d.%-m", "%d.%m", "%d/%m", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%d.%m")
            except ValueError:
                continue
        return date_str[:5]  # Берем первые 5 символов (DD.MM)
    except Exception as e:
        print(f"Ошибка нормализации даты '{date_str}': {str(e)}")
        return date_str

def get_tomorrow_date_string():
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%d.%m")

def get_names_for_tomorrow():
    try:
        file_path = os.path.join('static', 'data', 'id.json')
        with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        # Открытие таблицы
        spreadsheet = client.open_by_key(data.get(id)) 
        worksheet = spreadsheet.sheet1  # Первый лист
        all_data = worksheet.get_all_values()
        
        if not all_data:
            print("Таблица пуста")
            return []
        
        headers = all_data[0]
        tomorrow_date = get_tomorrow_date_string()
        print(f"Ищем дату: {tomorrow_date}")
        
        # Выводим все заголовки для отладки
        print("Заголовки в таблице:", headers)
        
        date_column = None
        for i, header in enumerate(headers):
            normalized_header = normalize_date(header)
            print(f"Проверяем заголовок: '{header}' -> нормализовано: '{normalized_header}'")
            if normalized_header == tomorrow_date:
                date_column = i + 1
                print(f"Нашли дату в столбце {date_column}")
                break
        
        if date_column is None:
            available_dates = [normalize_date(h) for h in headers[1:]]
            print(f"Дата {tomorrow_date} не найдена. Доступные даты: {available_dates}")
            return []
        
        names = []
        PRESENCE_VALUES = ['✅', '1', '+', 'да', 'yes', 'y', 'д']
        
        for row_num, row in enumerate(all_data[1:], start=2):
            if len(row) < date_column:
                print(f"Строка {row_num}: недостаточно столбцов")
                continue
                
            try:
                if ' - ' in row[0]:
                    _, name = row[0].split(' - ', 1)
                else:
                    name = row[0]
                
                cell_value = row[date_column - 1].strip().lower()
                if any(presence in cell_value for presence in PRESENCE_VALUES):
                    print(f"Строка {row_num}: {name.strip()} - присутствует ({cell_value})")
                    names.append(name.strip())
                else:
                    print(f"Строка {row_num}: {name.strip()} - отсутствует ({cell_value})")
            except Exception as e:
                print(f"Ошибка обработки строки {row_num}: {str(e)}")
        
        print(f"Найдены сотрудники на завтра: {names}")
        return names
    
    except Exception as e:
        print(f"Ошибка в get_names_for_tomorrow: {str(e)}")
        return []

def process_table_to_json(output_file='C:\\Users\\A L E K S\\Desktop\\PlanGen\\static\\data\\users_base.json'):
    file_path = os.path.join('static', 'data', 'id.json')
    with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

    # Открытие таблицы
    spreadsheet = client.open_by_key(data["id"]) 
    worksheet = spreadsheet.sheet1  # Первый лист
    all_data = worksheet.get_all_values()
    
    if not all_data:
        print("Таблица пуста")
        return
    
    # Получаем заголовки (даты) из первой строки
    headers = all_data[0]
    date_headers = headers[1:]  # Пропускаем первый заголовок (ID и имя)
    
    result = {}
    
    # Обрабатываем строки с пользователями (начиная со второй строки)
    for row in all_data[1:]:
        if not row or not row[0]:  # Пропускаем пустые строки
            continue
            
        # Разделяем ID и имя
        if ' - ' in row[0]:
            user_id, user_name = row[0].split(' - ', 1)
        else:
            user_id, user_name = row[0], ''
            
        # Обрабатываем данные по датам
        dates_data = {}
        for i, date_value in enumerate(row[1:]):  # Пропускаем первый элемент (ID и имя)
            if i >= len(date_headers):  # Если дат больше чем заголовков
                break
                
            date_header = date_headers[i]
            # Преобразуем значение в "+" или "-"
            status = "+" if date_value.strip().lower() == "\"+\"" else "-"
            dates_data[date_header] = status
        
        # Формируем запись для JSON
        result[user_id.strip()] = {
            "Инициалы": user_name.strip(),
            "Code": "None",
            "Даты": dates_data
        }
    
    # Сохраняем в JSON файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"Данные успешно сохранены в {output_file}")
   

#if __name__ == "__main__":
    #print("=== Начало работы скрипта ===")
    
    #names = get_names_for_tomorrow()
    
    #if names:
        #print("\n=== Начало генерации расписания ===")
       # schedule = generate_schedule(names)
       # print("\n=== Итоговое расписание ===")
      #  print(schedule)
   # else:
       # print("Нет сотрудников для создания расписания на завтра")
    
   # print("=== Работа скрипта завершена ===")

###
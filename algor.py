import random
from collections import defaultdict
import json
import os

def generate_schedule(names):
    hours = [f"{h:02d}:00" for h in range(9, 22)]
    peak_hours = ['12:00', '13:00', '11:00']
    schedule = defaultdict(lambda: {'Точка 1': [], 'Точка 2': []})
    rest_count = {name: 0 for name in names}

    with open(os.path.join('static', 'data', 'schedule_local.json'), 'w', encoding='utf-8') as f:
        f.write('{\n')  
        for i, hour in enumerate(hours):
            available_names = names.copy()
            
            
            point2_employee = random.choice(available_names)
            available_names.remove(point2_employee)

           
            if hour in peak_hours:
                point1_employees = available_names
            else:
                rest_candidates = [name for name in available_names if rest_count[name] < 2]
                if rest_candidates and len(available_names) > 1:
                    resting_employee = random.choice(rest_candidates)
                    rest_count[resting_employee] += 1
                    available_names.remove(resting_employee)
                
                point1_employees = random.sample(available_names, min(2, len(available_names)))

            
            hour_schedule = {
                "Точка 1": point1_employees,
                "Точка 2": [point2_employee]
            }
            json_line = json.dumps(hour_schedule, ensure_ascii=False)
            f.write(f'  "{hour}": {json_line}')
            if i < len(hours) - 1:
                f.write(',\n')
            else:
                f.write('\n')

        f.write('}') 

    with open('schedule_local.json', 'r', encoding='utf-8') as f:
        return f.read()


names = ['Алексей', 'Мария', 'Иван', 'Елена']
schedule = generate_schedule(names)
print(schedule)

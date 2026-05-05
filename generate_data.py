"""
Генерирует:
  - 30 машин в data/cars.json
  - 30+ поездок для 10 водителей в data/drivers.json
Каждый файл содержит JSON Lines (по одному документу на строку).
"""

import json
import random
from faker import Faker

fake = Faker('ru_RU')

# 1. МАШИНЫ (30 штук)

def generate_license_plate():
    """Генерирует реалистичный российский госномер."""
    letters = 'АВЕКМНОРСТУХ'
    return f"{random.choice(letters)}{random.randint(100,999)}{random.choice(letters)}{random.choice(letters)} {random.randint(10,199)}"

car_types = ["Легковой", "Грузовой фургон", "Микроавтобус", "Тягач", "Самосвал", "Рефрижератор"]

cars = []
for i in range(1, 31):
    car = {
        "id": i,
        "index": "cars",
        "doc_type": "_doc",
        "body": {
            "id_машины": i,
            "регистрационный_номер": generate_license_plate(),
            "тип_машины": random.choice(car_types),
            "дата_профилактики": fake.date_between(start_date="-2y", end_date="today").isoformat(),
            "расход_горючего_на_100_км": round(random.uniform(6.5, 28.0), 1),
            "пробег": random.randint(5000, 350000),
            "акт_осмотра_машины": (
                f"Тормозная система в норме. "
                f"{random.choice(['Двигатель работает ровно', 'Обнаружена незначительная вибрация двигателя', 'Требуется замена масла'])}. "
                f"{random.choice(['Кузов без повреждений', 'Имеются мелкие царапины на левом борту', 'Требуется покраска заднего бампера'])}. "
                f"Пройден плановый техосмотр {random.randint(1,12)}.{random.randint(1,28)}.{random.randint(2024,2026)}."
            )
        }
    }
    cars.append(car)

# 2. ВОДИТЕЛИ И ПОЕЗДКИ (10 водителей, у каждого 2–6 поездок)

driver_pool = []
for i in range(1, 11):
    driver_pool.append({
        "id_водителя": i,
        "имя": f"{fake.last_name()} {fake.first_name()} {fake.middle_name()}"
    })

drivers = []
doc_id = 1

for driver in driver_pool:
    num_trips = random.randint(2, 6)

    for _ in range(num_trips):
        driver_doc = {
            "id": doc_id,
            "index": "drivers",
            "doc_type": "_doc",
            "body": {
                "id_водителя": driver["id_водителя"],
                "персональные_данные_водителя": driver["имя"],
                "дата_поездки": fake.date_between(start_date="-6m", end_date="today").isoformat(),
                "id_машины": random.randint(1, 30),
                "путевой_лист": (
                    f"Маршрут: {fake.city_name()}, {fake.street_name()} д.{random.randint(1,100)} → "
                    f"{fake.city_name()}, {fake.street_name()} д.{random.randint(1,100)}. "
                    f"Груз: {random.choice(['продукты питания', 'строительные материалы', 'бытовая техника', 'мебель', 'медикаменты'])}. "
                    f"Вес: {random.randint(200,5000)} кг. Особые отметки: {random.choice(['без происшествий', 'пробка на МКАД', 'погрузка задержана'])}."
                ),
                "адрес_поездки": f"{fake.city_name()}, {fake.street_name()}, д.{random.randint(1,100)}",
                "длительность_поездки": round(random.uniform(0.3, 14.0), 1)
            }
        }
        drivers.append(driver_doc)
        doc_id += 1

# 3. СОХРАНЕНИЕ В ФАЙЛЫ

with open('data/cars.json', 'w', encoding='utf-8') as f:
    for car in cars:
        f.write(json.dumps(car, ensure_ascii=False) + '\n')

with open('data/drivers.json', 'w', encoding='utf-8') as f:
    for driver in drivers:
        f.write(json.dumps(driver, ensure_ascii=False) + '\n')

print("=" * 50)
print("ГЕНЕРАЦИЯ ДАННЫХ ЗАВЕРШЕНА")
print("=" * 50)
print(f"Машин:     {len(cars)} → data/cars.json")
print(f"Поездок:   {len(drivers)} → data/drivers.json")
print(f"Водителей: {len(driver_pool)}")
print("\nРаспределение поездок по водителям:")
for driver in driver_pool:
    count = sum(1 for d in drivers if d['body']['id_водителя'] == driver['id_водителя'])
    print(f"  ID {driver['id_водителя']:2d} ({driver['имя']}): {count} поездок")
print()

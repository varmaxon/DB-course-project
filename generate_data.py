import json
import random
import datetime
from faker import Faker

# Инициализация Faker с русской локалью
fake = Faker('ru_RU')

# Функция для генерации госномера
def generate_license_plate():
    letters = 'АВЕКМНОРСТУХ'
    return f"{random.choice(letters)}{random.randint(100,999)}{random.choice(letters)}{random.choice(letters)} {random.randint(10,199)}"

# Типы машин
car_types = ["Легковой", "Грузовой фургон", "Микроавтобус", "Тягач", "Самосвал", "Рефрижератор"]

# Генерация машин
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

# Сохранение машин в файл (один JSON-объект на строку для удобства чтения)
with open('cars.json', 'w', encoding='utf-8') as f:
    for car in cars:
        f.write(json.dumps(car, ensure_ascii=False) + '\n')

print("Сгенерировано 30 машин, сохранено в cars.json")

# Генерация водителей и поездок
drivers = []
for i in range(1, 31):
    full_name = f"{fake.last_name()} {fake.first_name()} {fake.middle_name()}"
    driver = {
        "id": i,
        "index": "drivers",
        "doc_type": "_doc",
        "body": {
            "id_водителя": i,
            "персональные_данные_водителя": full_name,
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
    drivers.append(driver)

with open('drivers.json', 'w', encoding='utf-8') as f:
    for driver in drivers:
        f.write(json.dumps(driver, ensure_ascii=False) + '\n')

print("Сгенерировано 30 водителей/поездок, сохранено в drivers.json")

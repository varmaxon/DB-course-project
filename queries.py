import json
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

print("=" * 60)
print("ЗАПРОС 1: Суммарный расход горючего по типам машин, сгруппированных по годам профилактики")
print("=" * 60)

query1 = {
    "size": 0,
    "aggs": {
        "профилактика_по_годам": {
            "date_histogram": {
                "field": "дата_профилактики",
                "calendar_interval": "year",
                "format": "yyyy",
                "min_doc_count": 1
            },
            "aggs": {
                "типы_машин": {
                    "terms": {
                        "field": "тип_машины",
                        "size": 10
                    },
                    "aggs": {
                        "суммарный_расход": {
                            "sum": {
                                "field": "расход_горючего_на_100_км"
                            }
                        }
                    }
                }
            }
        }
    }
}

result1 = es.search(index="cars", body=query1)

# Выводим результаты
print("\nРезультаты:")
for year_bucket in result1['aggregations']['профилактика_по_годам']['buckets']:
    year = year_bucket['key_as_string']
    print(f"\nГОД ПРОФИЛАКТИКИ: {year}")
    for type_bucket in year_bucket['типы_машин']['buckets']:
        car_type = type_bucket['key']
        total_fuel = type_bucket['суммарный_расход']['value']
        count = type_bucket['doc_count']
        print(f"   - {car_type}: {count} машин(ы), суммарный расход = {total_fuel:.1f} л/100км")

# Сохраняем результат в файл для отчёта (используем .body для получения словаря)
with open('query1_result.json', 'w', encoding='utf-8') as f:
    json.dump(result1.body, f, ensure_ascii=False, indent=2)
print("\nПолный JSON-ответ сохранён в 'query1_result.json'")


print("\n\n" + "=" * 60)
print("ЗАПРОС 2: Общее число поездок по каждому водителю")
print("=" * 60)

query2 = {
    "size": 0,
    "aggs": {
        "поездки_по_водителям": {
            "terms": {
                "field": "id_водителя",
                "size": 30,
                "order": { "_key": "asc" }
            }
        }
    }
}

result2 = es.search(index="drivers", body=query2)

print("\nРезультаты:")
for bucket in result2['aggregations']['поездки_по_водителям']['buckets']:
    driver_id = bucket['key']
    trips_count = bucket['doc_count']
    print(f"- Водитель ID {driver_id}: {trips_count} поездок/поездка")

total_trips = sum(bucket['doc_count'] for bucket in result2['aggregations']['поездки_по_водителям']['buckets'])
unique_drivers = len(result2['aggregations']['поездки_по_водителям']['buckets'])
print(f"\nВСЕГО ПОЕЗДОК: {total_trips}")
print(f"УНИКАЛЬНЫХ ВОДИТЕЛЕЙ: {unique_drivers}")

# Сохраняем результат в файл для отчёта
with open('query2_result.json', 'w', encoding='utf-8') as f:
    json.dump(result2.body, f, ensure_ascii=False, indent=2)
print("\nПолный JSON-ответ сохранён в 'query2_result.json'")

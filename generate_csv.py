import csv
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# Машины
cars_res = es.search(index="cars", body={"query": {"match_all": {}}}, size=100)  # match_all аналог select * 
cars = [hit['_source'] for hit in cars_res['hits']['hits']]

with open('cars.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_машины', 'регистрационный_номер', 'тип_машины'])
    for car in cars:
        writer.writerow([car['id_машины'], car['регистрационный_номер'], car['тип_машины']])

# Водители (уникальные)
drivers_res = es.search(index="drivers", body={"query": {"match_all": {}}}, size=100)
trips = [hit['_source'] for hit in drivers_res['hits']['hits']]

drivers_dict = {}
for trip in trips:
    did = trip['id_водителя']
    if did not in drivers_dict:
        drivers_dict[did] = trip['персональные_данные_водителя']

with open('drivers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_водителя', 'персональные_данные_водителя'])
    for did, fio in drivers_dict.items():
        writer.writerow([did, fio])

# Поездки
with open('trips.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_водителя', 'id_машины', 'дата_поездки', 'адрес_поездки', 'длительность_поездки'])
    for trip in trips:
        writer.writerow([trip['id_водителя'], trip['id_машины'],
                         trip['дата_поездки'], trip['адрес_поездки'],
                         trip['длительность_поездки']])

print("CSV-файлы созданы.")

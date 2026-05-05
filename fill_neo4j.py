from elasticsearch import Elasticsearch
from py2neo import Graph

# Подключение к Elasticsearch (правильный способ)
es = Elasticsearch("http://localhost:9200")

# Подключение к Neo4j
graph = Graph("bolt://localhost:7687", auth=('neo4j', 'iu6-magisters'))

# Если нужно пересоздать граф заново (раскомментируй следующую строку):
# graph.delete_all()

# Получаем все машины из ES
cars_res = es.search(index="cars", body={"query": {"match_all": {}}}, size=100)
cars = [hit['_source'] for hit in cars_res['hits']['hits']]

# Создаём узлы машин
for car in cars:
    graph.run(
        "MERGE (m:Машина {id_машины: $id}) "
        "ON CREATE SET m.регистрационный_номер = $reg, m.тип_машины = $type",
        id=car['id_машины'], reg=car['регистрационный_номер'], type=car['тип_машины']
    )

# Получаем все поездки
drivers_res = es.search(index="drivers", body={"query": {"match_all": {}}}, size=100)
trips = [hit['_source'] for hit in drivers_res['hits']['hits']]

# Для каждой поездки создаём узлы водителей и отношения
for trip in trips:
    graph.run(
        "MERGE (d:Водитель {id_водителя: $id}) "
        "ON CREATE SET d.персональные_данные_водителя = $fio",
        id=trip['id_водителя'], fio=trip['персональные_данные_водителя']
    )
    graph.run(
        "MATCH (d:Водитель {id_водителя: $d_id}) "
        "MATCH (m:Машина {id_машины: $m_id}) "
        "CREATE (d)-[:ВЫПОЛНИЛ_ПОЕЗДКУ_НА {"
        "  дата_поездки: $дата,"
        "  адрес_поездки: $адрес,"
        "  длительность_поездки: $длит"
        "}]->(m)",
        d_id=trip['id_водителя'], m_id=trip['id_машины'],
        дата=trip['дата_поездки'], адрес=trip['адрес_поездки'],
        длит=trip['длительность_поездки']
    )

print("Граф успешно заполнен!")

"""
Преобразование документов "Водитель" в векторы и сохранение в pgvector.
Используется модель all-MiniLM-L6-v2 (384 измерения).
"""

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector
import psycopg2

# 1. Подключение к Elasticsearch и получение данных
es = Elasticsearch("http://localhost:9200")

# Извлекаем все документы из индекса drivers (каждый документ – одна поездка)
res = es.search(index="drivers", body={"query": {"match_all": {}}}, size=100)
docs = [hit['_source'] for hit in res['hits']['hits']]
print(f"Получено документов из Elasticsearch: {len(docs)}")

# 2. Загрузка модели SentenceTransformer
# Эта модель понимает русский язык и даёт качественные эмбеддинги.
# Она работает на CPU и не требует мощного железа.
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Модель загружена. Размерность вектора:", model.get_sentence_embedding_dimension())

# 3. Подключение к PostgreSQL
# psycopg2 = Python-драйвер для работы с PostgreSQL. Позволяет подключаться к бд из кода Python и выполнять SQL-запросы
conn = psycopg2.connect(
    database="iu6",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Регистрируем тип vector для psycopg2
register_vector(conn)
cur = conn.cursor()

# 4. Обработка каждого документа и вставка в БД
for i, doc in enumerate(docs):
    # Формируем текст, который будет превращён в вектор.
    # Чем информативнее текст, тем лучше векторы отражают смысл.
    # Берём ФИО + путевой лист + адрес.
    fio = doc['персональные_данные_водителя']
    route = doc['путевой_лист']
    address = doc['адрес_поездки']
    text_for_embedding = f"Водитель: {fio}. Маршрут: {route}. Адрес: {address}."

    # Преобразуем текст в вектор
    embedding = model.encode(text_for_embedding).tolist()

    # Вставляем запись в таблицу driver_vectors
    cur.execute(
        """
        INSERT INTO driver_vectors (doc_id, driver_id, fio, route_text, embedding)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (doc.get('id', i),           # id документа
         doc['id_водителя'],         # id водителя
         fio,
         text_for_embedding,
         embedding)
    )   

    if (i + 1) % 5 == 0:
        print(f"Обработано {i+1} документов...")

# Фиксируем изменения
conn.commit()
cur.close()
conn.close()
print("Все векторы успешно сохранены в таблицу driver_vectors!")

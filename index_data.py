import json
from elasticsearch import Elasticsearch, helpers

# Подключаемся к Elasticsearch
es = Elasticsearch("http://localhost:9200")

def load_and_index(file_path, index_name):
    """
    Читает JSON-файл (по одному объекту на строку) и загружает в Elasticsearch.
    
    Параметры:
        file_path  - путь к JSON-файлу
        index_name - имя индекса ('cars' или 'drivers')
    """
    actions = []  # список действий для bulk-запроса
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # пропускаем пустые строки
                continue
                
            # Парсим JSON-строку в словарь
            doc = json.loads(line)
            
            # Извлекаем тело документа (поля, которые пойдут в _source)
            body = doc['body']
            
            # Используем наш id как _id документа в Elasticsearch
            doc_id = doc['id']
            
            # Формируем действие для bulk API (правильный формат)
            action = {
                "_index": index_name,
                "_id": str(doc_id),  # id должен быть строкой
                "_source": body
            }
            actions.append(action)
    
    # Отправляем все документы одним bulk-запросом
    print(f"Загружаем {len(actions)} документов в индекс '{index_name}'...")
    
    # Используем streaming_bulk для лучшего контроля ошибок
    success = 0
    failed = 0
    errors = []
    
    for ok, result in helpers.streaming_bulk(
        es,
        actions,
        chunk_size=10,
        raise_on_error=False
    ):
        if ok:
            success += 1
        else:
            failed += 1
            errors.append(result)
    
    print(f"✅ Индекс '{index_name}': загружено {success} документов")
    if failed:
        print(f"⚠️  Ошибок при загрузке: {failed}")
        # Покажем первую ошибку для диагностики
        if errors:
            print(f"   Пример ошибки: {errors[0]}")
    
    # Принудительно сбрасываем буфер индексации (refresh)
    es.indices.refresh(index=index_name)
    print(f"   Индекс '{index_name}' обновлён (refresh)\n")

# ============================================
# ЗАГРУЗКА ДАННЫХ
# ============================================

print("=" * 50)
print("ИНДЕКСАЦИЯ ДОКУМЕНТОВ В ELASTICSEARCH")
print("=" * 50)

# Загружаем машины
load_and_index('data/cars.json', 'cars')

# Загружаем водителей
load_and_index('data/drivers.json', 'drivers')

# ============================================
# ПРОВЕРКА: сколько документов в каждом индексе
# ============================================

print("=" * 50)
print("ПРОВЕРКА ЗАГРУЗКИ")
print("=" * 50)

cars_count = es.count(index="cars")['count']
drivers_count = es.count(index="drivers")['count']

print(f"Документов в индексе 'cars':    {cars_count}")
print(f"Документов в индексе 'drivers': {drivers_count}")

# Покажем один документ из каждого индекса для проверки
if cars_count > 0:
    print("\n--- Пример документа из 'cars' ---")
    sample_car = es.get(index="cars", id="1")
    print(json.dumps(sample_car['_source'], ensure_ascii=False, indent=2))
else:
    print("\n⚠️  В индексе 'cars' нет документов")

if drivers_count > 0:
    print("\n--- Пример документа из 'drivers' ---")
    sample_driver = es.get(index="drivers", id="1")
    print(json.dumps(sample_driver['_source'], ensure_ascii=False, indent=2))
else:
    print("\n⚠️  В индексе 'drivers' нет документов")

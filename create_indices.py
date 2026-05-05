from elasticsearch import Elasticsearch

# Подключаемся к локальному Elasticsearch (по умолчанию порт 9200)
es = Elasticsearch("http://localhost:9200")

# 2.1. ОПРЕДЕЛЕНИЕ АНАЛИЗАТОРА
# Это блок "settings", который задаёт анализатор.
# По заданию:
#   - токенизатор standard (русский язык)
#   - фильтр lowercase (нижний регистр)
#   - фильтр stop (удаление русских стоп-слов)
#   - фильтр stemmer (стемминг по snowball, русский)

settings = {
    "analysis": {
        "analyzer": {
            "russian_analyzer": {           # имя анализатора
                "type": "custom",
                "tokenizer": "standard",    # стандартный токенизатор
                "filter": [
                    "lowercase",            # привести к нижнему регистру
                    "russian_stop",         # удалить стоп-слова (определён ниже)
                    "russian_stemmer"       # стемминг (определён ниже)
                ]
            }
        },
        "filter": {
            "russian_stop": {               # фильтр стоп-слов
                "type": "stop",
                "stopwords": "_russian_"    # встроенный список русских стоп-слов
            },
            "russian_stemmer": {            # фильтр стемминга
                "type": "stemmer",
                "language": "russian"       # русский язык (snowball)
            }
        }
    }
}

# 2.2. МАППИНГ ДЛЯ ИНДЕКСА "cars" (машины)
# Поля из задания:
#   регистрационный_номер, тип_машины, дата_профилактики, расход_горючего_на_100_км, пробег, акт_осмотра_машины (*)
# Поля, отмеченные *, должны использовать анализатор russian_analyzer

cars_mapping = {
    "properties": {
        "id_машины": {
            "type": "integer"               # числовой идентификатор
        },
        "регистрационный_номер": {
            "type": "keyword"               # точное значение, не анализируется
        },
        "тип_машины": {
            "type": "keyword"               # точное значение (Легковой, Грузовой...)
        },
        "дата_профилактики": {
            "type": "date"                  # дата в формате ISO
        },
        "расход_горючего_на_100_км": {
            "type": "float"                 # число с плавающей точкой
        },
        "пробег": {
            "type": "integer"               # целое число
        },
        "акт_осмотра_машины": {
            "type": "text",                 # полнотекстовое поле
            "analyzer": "russian_analyzer"  # с нашим анализатором
        }
    }
}

# 2.3. МАППИНГ ДЛЯ ИНДЕКСА "drivers" (водители)
# Поля из задания:
#   id_водителя, персональные_данные_водителя (*), дата_поездки, id_машины, путевой_лист (*), адрес_поездки, длительность_поездки

drivers_mapping = {
    "properties": {
        "id_водителя": {
            "type": "integer"
        },
        "персональные_данные_водителя": {
            "type": "text",                 # полнотекстовое поле (*)
            "analyzer": "russian_analyzer"  # с анализатором
        },
        "дата_поездки": {
            "type": "date"
        },
        "id_машины": {
            "type": "integer"
        },
        "путевой_лист": {
            "type": "text",                 # полнотекстовое поле (*)
            "analyzer": "russian_analyzer"  # с анализатором
        },
        "адрес_поездки": {
            "type": "text"                  # текстовое поле (можно и keyword, но оставим text)
        },
        "длительность_поездки": {
            "type": "float"
        }
    }
}

# СОЗДАНИЕ ИНДЕКСОВ

# Создаём индекс cars, если его ещё нет
if not es.indices.exists(index="cars"):
    es.indices.create(
        index="cars",
        body={
            "settings": settings,
            "mappings": cars_mapping
        }
    )
    print("✅ Индекс 'cars' создан с анализатором и маппингом")
else:
    print("⚠️  Индекс 'cars' уже существует. Удалите его, если нужно пересоздать:")
    print("   curl -X DELETE 'localhost:9200/cars'")

# Создаём индекс drivers, если его ещё нет
if not es.indices.exists(index="drivers"):
    es.indices.create(
        index="drivers",
        body={
            "settings": settings,
            "mappings": drivers_mapping
        }
    )
    print("✅ Индекс 'drivers' создан с анализатором и маппингом")
else:
    print("⚠️  Индекс 'drivers' уже существует. Удалите его, если нужно пересоздать:")
    print("   curl -X DELETE 'localhost:9200/drivers'")

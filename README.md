# БД | Курсовой проект
## Разработка макета аналитической системы на основе баз данных NoSQL

### Используем 4 NoSQL-технологии:
1. Elasticsearch - полнотекстовый поиск и агрегации по документам.

2. Neo4j - графовая база данных для анализа связей.

3. Hadoop + Spark - распределённая обработка табличных данных.

4. Pgvector - векторное представление документов и поиск похожих по смыслу.

### Команды для работы:
1. Elasticsearch:

elasticsearch-7.17.0/bin/elasticsearch

2. Kibana:

kibana-7.17.0-linux-x86_64/bin/kibana

3. Neo4j:

Запуск: sudo systemctl start neo4j
Проверить запуск: service --status-all | grep neo4j
Автозапуск: sudo systemctl enable neo4j

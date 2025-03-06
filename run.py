from tasks import fetch_tenders, fetch_publish_date

pages = [1, 2]
all_tenders = []

# Получаем ID тендеров
for page in pages:
    tenders = fetch_tenders.delay(page).get()  # Celery-таска
    all_tenders.extend(tenders)

# Парсим XML для каждого тендера
results = [fetch_publish_date.delay(tid).get() for tid in all_tenders]

# Выводим результат
for res in results:
    print(res)

from tasks import fetch_tenders, fetch_publish_date

pages = [1, 2]
all_tenders = []

# Получаем ID тендеров (асинхронно)
for page in pages:
    all_tenders.extend(fetch_tenders.delay(page).get())

# Парсим XML-данные для каждого тендера (асинхронно)
results = [fetch_publish_date.delay(tid).get() for tid in all_tenders]

# Выводим результат
for res in results:
    print(res)

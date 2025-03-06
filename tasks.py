from celery_config import app
import requests
from bs4 import BeautifulSoup
import xmltodict

BASE_URL = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
PRINT_URL = "https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber={}"
XML_URL = "https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber={}"


@app.task
def fetch_tenders(page):
    """Получает список ID тендеров с указанной страницы"""
    url = f"{BASE_URL}?fz44=on&pageNumber={page}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    tenders = []
    for link in soup.select("a[href*='printForm/view.html?regNumber=']"):
        tender_id = link['href'].split("regNumber=")[-1]
        tenders.append(tender_id)

    return tenders


@app.task
def fetch_publish_date(tender_id):
    """Получает дату публикации тендера из XML"""
    xml_url = XML_URL.format(tender_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(xml_url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка запроса: {xml_url} - Код {response.status_code}")
        return f"{xml_url} - ERROR {response.status_code}"

    print(f"Raw XML for {tender_id}:\n", response.text[:500])  # Выведет первые 500 символов XML

    try:
        xml_data = xmltodict.parse(response.text)
        print(f"Parsed XML Data for {tender_id}:\n", xml_data)  # Проверяем структуру

        # Поиск даты
        publish_date = (
            xml_data.get('export', {})
                    .get('fcsNotification', {})
                    .get('publishDTInEIS', None)
        )

        return f"{xml_url} - {publish_date}"
    except Exception as e:
        print(f"Ошибка парсинга XML для {tender_id}: {e}")
        return f"{xml_url} - XML Parsing Error: {str(e)}"

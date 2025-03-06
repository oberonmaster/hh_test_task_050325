from celery import shared_task
import requests
from bs4 import BeautifulSoup
import xmltodict

BASE_URL = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
PRINT_URL = "https://zakupki.gov.ru/epz/order/notice/printForm/view.html?regNumber={}"
XML_URL = "https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber={}"


@shared_task
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


@shared_task
def fetch_publish_date(tender_id):
    """Получает дату публикации тендера из XML"""
    xml_url = XML_URL.format(tender_id)
    response = requests.get(xml_url)

    if response.status_code != 200:
        return f"{xml_url} - None"

    xml_data = xmltodict.parse(response.text)
    publish_date = xml_data.get('export', {}).get('contract', {}).get('publishDTInEIS', None)

    return f"{xml_url} - {publish_date}"

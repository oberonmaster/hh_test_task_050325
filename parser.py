import requests
from bs4 import BeautifulSoup
import xmltodict

BASE_URL = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
XML_URL = "https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber={}"

def fetch_tenders_sync(page):
    """Синхронно получает список тендеров"""
    url = f"{BASE_URL}?fz44=on&pageNumber={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tenders = []
    for link in soup.select("a[href*='printForm/view.html?regNumber=']"):
        tender_id = link['href'].split("regNumber=")[-1]
        tenders.append(tender_id)

    return tenders

def fetch_publish_date_sync(tender_id):
    """Синхронно получает дату публикации"""
    xml_url = XML_URL.format(tender_id)
    response = requests.get(xml_url)

    if response.status_code != 200:
        return f"{xml_url} - None"

    xml_data = xmltodict.parse(response.text)
    publish_date = xml_data.get('export', {}).get('contract', {}).get('publishDTInEIS', None)

    return f"{xml_url} - {publish_date}"

if __name__ == "__main__":
    tenders = fetch_tenders_sync(1)
    for tid in tenders:
        print(fetch_publish_date_sync(tid))

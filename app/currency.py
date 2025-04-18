import requests
from bs4 import BeautifulSoup


def get_usd_rate():
    try:
        response = requests.get("https://minfin.com.ua/ua/currency/usd/")
        soup = BeautifulSoup(response.text, "html.parser")
        rate_tag = soup.select_one(".sc-1x32wa2-9")
        rate = float(rate_tag.text.replace(',', '.')[:6])
        return rate
    except Exception:
        return 40.0

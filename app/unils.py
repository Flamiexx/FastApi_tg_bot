import requests
from bs4 import BeautifulSoup


def convert_to_usd(amount_uah: float) -> float:
    try:
        response = requests.get("https://minfin.com.ua/ua/currency/usd/")
        soup = BeautifulSoup(response.text, "html.parser")
        rate_tag = soup.select_one(".sc-1x32wa2-9.fxtpMX")
        rate = float(rate_tag.text.replace(",", "."))
        return round(amount_uah / rate, 2)
    except Exception as e:
        print("Error fetching exchange rate:", e)
        return 0.0

from bs4 import BeautifulSoup
import requests

from config import URL, HEADERS, CONTENT_CHECK_STR
from utils import *


def scrap_slowhop(page=0) -> list:

    """Scraps data from Slowhop.com last minute site. Returns list sorted by check-in date"""

    scrap = []
    while True:
        page += 1
        url = URL.format(page=page)
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        no_response = soup.find_all(text=CONTENT_CHECK_STR)
        offers = soup.select('.media')
        print('page', page)
        if not no_response:
            for i in offers:
                try:
                    scrap = serialize_data(get_data(i))
                except Exception as e:
                    print(e)
        else:
            break
    return sorted(scrap, key=lambda d: d['zameldowanie'])

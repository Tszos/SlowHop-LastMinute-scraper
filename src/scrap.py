from bs4 import BeautifulSoup
import requests

from config import URL, HEADERS, CONTENT_CHECK_STR
from utils import *


def scrap_slowhop(page=0) -> list:

    """Scraps data from Slowhop.com last minute site. Returns list sorted by check-in date"""

    scrap = []
    base_url = MAIN_PAGE_URL
    response = requests.get(base_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    pages_quantity = get_pages_quantity(soup=soup, element='.results-pagination__link', element_number=0)
    for p in range(1, pages_quantity + 1):
        url = URL.format(page=p)
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')
        offers = soup.select('.media')
        print('page', page)
        for i in offers:
            try:
                scrap = serialize_data(get_data(i))
            except Exception as e:
                print(e)
        else:
            break
    return sorted(scrap, key=lambda d: d['zameldowanie'])

from datetime import datetime
import re

from config import MAIN_PAGE_URL


def get_offer_url(source) -> dict:
    site = MAIN_PAGE_URL + source.select('.search-product')[0]['href']
    return {'strona': site}


def get_location(source) -> dict:
    location = source.select('.search-product--sub-text')[0].get_text(strip=True)
    return {'miejsce': location}


def get_name(source) -> dict:
    name = source.find('h5').string
    return {'nazwa': name}


def get_description(source) -> dict:
    description = source.select('.last-minute-items')[0].get_text(separator='§', strip=True).split(',')
    if len(description) == 1:
        description = description[0]
    else:
        description = description[0].strip() + ' - kilka opcji do wyboru'
    return {'opis': description}


def get_dates_and_size(source) -> dict:
    date_raw = str(source.select('.last-minute-info')[0].get_text(strip=True).replace('-', '.'))
    date_in = datetime.strptime((date_raw.split('·')[0]).strip().split(' ')[0],
                                '%d.%m').date().strftime('%d.%m')
    date_out = datetime.strptime((date_raw.split('·')[0]).strip().split(' ')[2],
                                 '%d.%m.%Y').date().strftime('%d.%m.%Y')
    size = (date_raw.split('·')[1]).strip()
    return {'zameldowanie': date_in, 'wymeldowanie': date_out, 'wielkość': size}


def get_price(source) -> dict:
    price_raw = source.select('.last-minute-price')[0].get_text(separator='§', strip=True)
    price = price_raw.split('§')
    if len(price) > 1:
        old_price = float(price_raw.split('§')[0])
        new_price = float(re.sub('\D', '', price_raw.split('§')[1]))
        savings = old_price - new_price
    else:
        new_price = float(re.sub('\D', '', price[0]))
        old_price = '-'
        savings = '-'
    return {'oszczędność': savings, 'nowa cena': new_price, 'stara cena': old_price}


def get_image(source) -> dict:
    img = source.select('.search-product--header')[0]['style'].split("'")[1]
    return {'zdjęcie': img}


def get_data(source) -> list[dict]:
    offer_url = get_offer_url(source)
    location = get_location(source)
    name = get_name(source)
    if source.select('.last-minute-items'):
        description = get_description(source)
    else:
        description = '-'
    date_and_size = get_dates_and_size(source)
    price = get_price(source)
    img = get_image(source)
    return [offer_url, location, name, description, date_and_size, price, img]


def serialize_data(scraped):
    data = {}
    for i in scraped:
        data.update(i)
    return data

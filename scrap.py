from datetime import datetime

from bs4 import BeautifulSoup
import requests
import re


def scrap_slowhop(page=0):
    scrap = []
    data = {}
    while True:
        page += 1
        url = f'https://slowhop.com/pl/last-minute?page={page}'
        slowhop = 'https://slowhop.com'
        # from https://httpbin.org/get
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75"}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        no_response = soup.find_all(text='Ups! Chwilowo tutaj pusto. Wszystkie last minute zeszły na pniu...')
        dupa = soup.select('.col-md-4')

        print('page', page)
        if not no_response:
            for i in dupa:
                try:
                    site = slowhop + i.select('.search-product')[0]['href']
                    # print(site)
                    data.update({'strona': site})
                    place = i.select('.search-product--sub-text')[0].get_text(strip=True)
                    name = i.find('h5').string
                    if i.select('.last-minute-items'):
                        description = i.select('.last-minute-items')[0].get_text(separator='§', strip=True).split(',')
                        if len(description) == 1:
                            description = description[0]
                        else:
                            description = description[0].strip() + ' - kilka opcji do wyboru'
                    else:
                        description = '-'
                    date_raw = str(i.select('.last-minute-info')[0].get_text(strip=True).replace('-', '.'))
                    date_in = datetime.strptime((date_raw.split('·')[0]).strip().split(' ')[0],
                                                '%d.%m').date().strftime('%d.%m')
                    date_out = datetime.strptime((date_raw.split('·')[0]).strip().split(' ')[2],
                                                 '%d.%m.%Y').date().strftime('%d.%m.%Y')
                    size = (date_raw.split('·')[1]).strip()
                    price_raw = i.select('.last-minute-price')[0].get_text(separator='§', strip=True)
                    price = price_raw.split('§')
                    img = i.select('.search-product--header')[0]['style'].split("'")[1]
                    # print(img)
                    data.update({'zdjęcie': img})
                    # print(place)
                    data.update({'miejsce': place})
                    # print(name)
                    data.update({'nazwa': name})
                    if description:
                        # print(description)
                        data.update({'opis': description})
                    # print(date_in)
                    data.update({'zameldowanie': date_in})
                    # print(date_out)
                    data.update({'wymeldowanie': date_out})
                    # print(size)
                    data.update({'wielkość': size})
                    if len(price) > 1:
                        old_price = float(price_raw.split('§')[0])
                        new_price = float(re.sub('\D', '', price_raw.split('§')[1]))
                        # print(old_price)
                        savings = old_price - new_price
                        data.update({'oszczędność': savings})
                        data.update({'stara cena': old_price})
                        # print(new_price)
                        data.update({'nowa cena': new_price})
                    else:
                        new_price = float(re.sub('\D', '', price[0]))
                        old_price = '-'
                        savings = '-'
                        # print(old_price)
                        # print(new_price)
                        data.update({'oszczędność': savings})
                        data.update({'nowa cena': new_price})
                        data.update({'stara cena': old_price})
                    data_copy = data.copy()
                    scrap.append(data_copy)
                    # print('--------------------')
                except Exception as e:
                    print(e)
        else:
            break
    return sorted(scrap, key=lambda d: d['nowa cena'])


if __name__ == '__main__':
    print(scrap_slowhop())

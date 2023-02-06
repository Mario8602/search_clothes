import json
from time import perf_counter
import os.path

import requests
from bs4 import BeautifulSoup as bs

from site_data.headers_params import cookies, headers, params


urls = {
    'catalog': '/catalog/',
    'monitory': {
        'url': 'https://www.dns-shop.ru/catalog/17a8c23316404e77/komplekty-klaviaturamysh/',
        'tag': 'a',
        'class_': 'catalog-product__name ui-link ui-link_black'
    }}


def page_count_search(url):
    response = requests.get(url, cookies=cookies, headers=headers)
    data = json.loads(response.text)
    root = bs(data['html'], 'lxml')
    number = []
    numbers_page = root.find('a', class_='pagination-widget__page-link_last', href=True)
    if numbers_page is None:
        return 1
    else:
        number.append(numbers_page.get('href'))
        number_pages = number[0].split('/')[-1][3:]
        return number_pages


def get_uniq_id(url):
    if not os.path.exists('json_data'):
        os.makedirs('json_data')
    number_of_pages = page_count_search(url)
    unique_id = []
    for page in range(1, int(number_of_pages)+1):
        response = requests.get(url, params={'p': page}, headers=headers, cookies=cookies)
        data = json.loads(response.text)
        data_bs = bs(data['html'], 'lxml')
        print(f'Поиск уникальных id товара на странице: {page}')

        info_prod = data_bs.find_all('div', class_='catalog-product ui-button-widget')
        for i in info_prod:
            unique_id.append(i.get('data-product'))

    with open('json_data/my.txt', 'w') as file:
        file.write(str(unique_id))


def get_data_prod():
    lst_id = open('json_data/my.txt', 'r')
    lst_id_my = lst_id.read()
    data_items = {}
    item_number = 0
    for item_id in eval(lst_id_my):
        print('Товар номер:', item_number)
        item_number += 1
        data = 'data={"type":"product-buy","containers":[{"id":"as-MqCfbo",' \
               '"data":{"id":'f'"{item_id}"'',"params":{"showOneClick":true,"isCard":true}}}]}'

        response = requests.post(
            'https://www.dns-shop.ru/ajax-state/product-buy/',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        ).json()

        item_name = response.get('data').get('states')[0].get('data').get('name')
        item_price = response.get('data').get('states')[0].get('data').get('price')
        item_price_old = max(item_price.values())
        item_price_sale = min(item_price.values())

        if len(item_price) > 1:
            data_items[item_id] = {
                'item_name': item_name,
                'item_price_old': item_price_old,
                'item_price_sale': item_price_sale,
            }

    with open('json_data/5_dns_result.json', 'w') as file:
        json.dump(data_items, file, indent=4, ensure_ascii=False)


def main():
    get_uniq_id('https://www.dns-shop.ru/catalog/17a8c23316404e77/komplekty-klaviaturamysh/')
    get_data_prod()


if __name__ == '__main__':
    start = perf_counter()
    main()
    print(f'time: {(perf_counter() - start):.02f}')

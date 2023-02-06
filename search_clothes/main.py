from bs4 import BeautifulSoup
import requests
import json
from site_data.headers_params import headers


def get_data():
    response = requests.get(
        'https://api.retailrocket.ru/api/2.0/recommendation/popular/57b561fb65bf1932a870d842/?&features=%'
        '2FPropertyInterests&stockId=2204&categoryIds=188&categoryPaths=&session=62a0bae782847c00017185fa&'
        'pvid=215114593406956&isDebug=false&format=json',
        headers=headers,
    ).json()
    items_thing = {}

    for item in response:
        if item.get('OldPrice') != 0:
            item_price = item.get('Price')
            item_oldprice = item.get('OldPrice')
            item_ids = item.get('ItemId')
            item_name = item.get('Name')
            item_art = item.get('Params').get('Артикул')
            item_url = item.get('Url')
            item_pic_url = item.get('PictureUrl')

            items_thing[item_ids] = {
                'item_price': item_price,
                'item_oldprice': item_oldprice,
                'item_name': item_name,
                'item_art': item_art,
                'item_url': item_url,
                'item_pic_url': item_pic_url
            }
    with open('json_data/2_items_things.json', 'w') as file:
        json.dump(items_thing, file, indent=4, ensure_ascii=False)


    # with open('all_price_products.json', 'w') as file:
    #     json.dump(product_price, file, indent=4, ensure_ascii=False)
    # print(product_price)


def main():
    get_data()


if __name__ == "__main__":
    main()

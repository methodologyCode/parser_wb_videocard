import csv

import requests

from models import Products


class ParseVideoCard:
    def __init__(self, brand='MSI', limit=10, page=1):
        self.limit = limit
        self.page = page
        self.brand = brand
        self.brands = {'AMD': 28933, 'MSI': 27445, 'ASUS': 5786}
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                         'Win64; x64) '
                                         'AppleWebKit/537.36 (KHTML, like '
                                         'Gecko) '
                                         'Chrome/102.0.0.0 Safari/537.36'}

    def parse(self):
        count = 1
        self.set_csv_order_name()
        while count <= self.page:
            response = requests.get('https://catalog.wb.ru/brands/m/catalog'
                                    f'?appType=1&brand={self.brands[self.brand]}&'
                                    f'limit={self.limit}&curr=rub&dest'
                                    f'=-1257786&page={count}&sort=popular'
                                    '&xsubject=3274',
                                    headers=self.user_agent)
            data = Products.model_validate(response.json()['data'])
            if not data.products:
                break
            self.save_file_csv(data)
            count += 1

    def set_csv_order_name(self):
        with open('data.csv', mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'Название', 'Цена', 'Бренд', 'Рейтинг'])

    def save_file_csv(self, data):
        with open('data.csv', mode='a', encoding='utf-8') as file:
            writer = csv.writer(file)
            for product in data.products:
                writer.writerow([product.id, product.name, product.salePriceU,
                                 product.brand, product.rating])


if __name__ == '__main__':
    parser = ParseVideoCard()
    parser.parse()

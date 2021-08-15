import glob
import json
import requests, csv
from bs4 import BeautifulSoup
import pandas as pd

def get_urls():
    print('Getting url....')

    headers = {
        'user-agent': 'Mozilla/5.0  Chrome/92.0'
    }

    params = {
        'dealer_id': '',
        'list_price_max': '',
        'list_price_min': '',
        'makes[]': 'chevrolet',
        'maximum_distance': 30,
        'mileage_max': '',
        'page_size': 20,
        'sort': 'best_match_desc',
        'stock_type': 'all',
        'year_max': '',
        'year_min': '',
        'zip': ''

    }
    res = requests.get('https://www.cars.com/shopping/results/', headers=headers, params=params, )
    soup = BeautifulSoup(res.text, 'html.parser')

    page_item = soup.find_all('li', attrs={'class': 'sds-pagination__item'})
    total_pages = len(page_item) - 1

    return total_pages

def get_produk(page):
    print('Getting product....page{}'.format(page))
    params = {
        'page': page,
        'page_size': 20,
        'dealer_id': '',
        'list_price_max': '',
        'list_price_min': '',
        'makes[]': 'chevrolet',
        'maximum_distance': 30,
        'mileage_max': '',
        'sort': 'best_match_desc',
        'stock_type': 'all',
        'year_max': '',
        'year_min': '',
        'zip': ''
    }

    res = requests.get('https://www.cars.com/shopping/results/', params=params)
    soup = BeautifulSoup(res.text, 'html.parser')

    products = soup.find_all('div', {'class': 'vehicle-card-main'})
    urls = []

    for product in products:
        url = product.find('a')['href']
        urls.append(url)

    return urls

def get_detail(url):
    print('Getting detail.....')
    res = requests.get('https://www.cars.com/' +url)

    soup = BeautifulSoup(res.text, 'html.parser')

    product = soup.find('h1').text.strip()
    price = soup.find('span', attrs={'class': 'primary-price'}).text.strip()
    dealer = soup.find('h3', attrs={'class': 'sds-heading--5'}).text.strip()
    rating = soup.find('span', attrs={'class': 'sds-rating__count'}).text.strip()

    dict_data = {
        'product': product,
        'price': price,
        'dealer': dealer,
        'rating': rating
    }

    # Generate JSON file in detail product
    with open('./results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)

def create_csv():
    print('Creating csv files.....')
    datas = []
    files = sorted(glob.glob('./results/*.json'))
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)

def run():

    options = int(input('Input Options Number:\n 1. Collecting all urls\n 2. get detail all product\n 3. Create CSV'))

    total_pages = get_urls()
    if options == 1:

        # Put url pages in json
        total_urls = []
        for i in range(total_pages):
            page = i + 1
            urls = get_produk(page)
            total_urls += urls
        # Generate JSON file
        with open('all_urls.json', 'w') as outfile:
            json.dump(total_urls, outfile)

    if options == 2:
        # Open json files after generate
        with open('all_urls.json') as json_file:
            all_url = json.load(json_file)

        for url in all_url:
            get_detail(url)

    if options == 3:
            create_csv()


if __name__ == '__main__':
    run()
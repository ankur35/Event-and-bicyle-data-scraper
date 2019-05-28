# -*- coding: utf-8 -*-




import requests
import json
import os
from bs4 import BeautifulSoup
from pprint import pprint
from time import time


def scrape_year(main_url):

    data = []
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    content = soup.find(id='cms-content-left')
    articles = content.find_all('article')

    for article in articles:
        h2 = article.find('h2')
        link = h2.find('a')

        if link is None:
            continue
        
        address = article.find(**{'class': 'adr'})
        
        street = address.find(**{'class': 'street-address'}).text
        locality = address.find(**{'class': 'locality'}).text
        postcode = address.find(**{'class': 'postal-code'}).text

        ps = article.find_all('p')
        dates = None

        for p in ps:
            if 'Dates:' in p.text:
                dates = p.find('span').text
        
        if dates is None:
            continue

        data.append({
            'title': h2.text,
            'street': street,
            'locality': locality,
            'postcode': postcode,
            'dates': dates,
            'url': link['href']
        })

    return data


baseurl = 'http://www.londontown.com'
data_dir = 'eventsdata'

data = {}

for year in [2015]:
    print('\nProcessing year {}'.format(year))
    
    start = time()
    year_data = []

    for month in ['Januari', 'Februari', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November, Decemder']:
        main_url = baseurl + '/London/{}-in-London_{}'.format(month, year)

        if year == 2019:
            main_url = baseurl + '/London/{}-in-London'.format(month)
        
        year_data.extend(scrape_year(main_url))
    
    data[year] = year_data

    stop = time()

    print('  scraped {0} events in {1: .1f}s'.format(len(year_data), stop-start))
    
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    with open(data_dir + '/events-{}.json'.format(year), 'w') as f:
        json.dump(year_data, f)
        f.close()
    
    print('  data is saved in {}/events-{}.json\n'.format(data_dir, year))

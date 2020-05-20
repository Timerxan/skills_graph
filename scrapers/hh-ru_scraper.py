""" Scraping vacancies from hh.ru.

As argument use word or phrase in double quotes.
Saves results to ./data/raw-tags_{phrase_to_search}.json' file

"""


import datetime
import json
import sys
import time

import requests

HH_MAX_PAGES_COUNT = 20
FETCH_FOR_DAYS = 365*3


def scrape(phrase_to_search):
    ses = requests.Session()
    ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}

    date_to = datetime.datetime.now().replace(microsecond=0)
    date_from = date_to - datetime.timedelta(days=FETCH_FOR_DAYS)
    params = {
        'text': phrase_to_search,
        'per_page': 100,
        'date_from': date_from.isoformat(),
        'date_to': date_to.isoformat(),
    }
    url = f'https://api.hh.ru/vacancies'
    vacancies_ids = set()
    total_pages = 0
    done = False
    while not done:  # getting list of all vacancies ids
        for pag_num in range(HH_MAX_PAGES_COUNT):
            time.sleep(0.5)
            print(f'\rscraping page {total_pages + pag_num}', end='')
            params['page'] = pag_num
            res = ses.get(url, params=params).json()
            if not res['items']:
                done = True
                break
            last_vacancy = res['items'][-1]
            vacancies_ids.update([item['id'] for item in res['items']])
        if done:
            break
        total_pages += HH_MAX_PAGES_COUNT
        params['date_to'] = last_vacancy['published_at']
    print()

    # parsing vacancies ids, getting vacancy page and scraping tags from each vacancy
    tags_list = []
    for vac_id in vacancies_ids:
        vac_res = ses.get(f'https://api.hh.ru/vacancies/{vac_id}')
        skills = vac_res.json()['key_skills']
        if skills:  # at least one skill present
            print(vac_id)
            tags = [skill['name'] for skill in skills]
            print(' '.join(tags))
            tags_list.append(tags)
            print()
        time.sleep(0.1)  # not to overload the server

    res = {'phrase': phrase_to_search, 'items_number': len(tags_list), 'items': tags_list}
    with open(f'./data/raw/raw-tags_{phrase_to_search}.json', 'w') as fp:  # serializing
        json.dump(res, fp)

    return tags_list


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ./scrapers/hh-ru_scraper.py python')
    else:
        phrase_to_search = sys.argv[1]
        tags_list = scrape(phrase_to_search)

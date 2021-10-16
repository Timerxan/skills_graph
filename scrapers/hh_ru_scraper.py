""" Scraping vacancies from hh.ru.

As argument use word or phrase in double quotes.
Saves results to ./data/raw-tags_{phrase_to_search}.json' file

"""


import datetime
import json
import sys
import time
import requests
import sql_db_operation as db_op


def get_vacancies_id_list(specialization=1, phrase_to_search=False):
    date_to = datetime.datetime.now().replace(microsecond=0)
    date_from = date_to - datetime.timedelta(days=365)
    params = {
              'page': 0,
              'per_page': 100,
              'order_by': 'publication_time',
              'date_from': date_from.isoformat(),
              'date_to': date_to.isoformat(),
              'specialization': specialization,
             }
    if phrase_to_search: params['text'] = phrase_to_search

    res = {}

    URL = 'https://api.hh.ru/vacancies'

    try:
        ses = requests.Session()
        ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
        res = ses.get(URL, params=params).json()
        if 'errors' in res.keys():
            print(res['errors'])
            return False
    except Exception as ex:
        print('Error:', ex)
        print('res=', res)
        return False

    # getting list of all vacancies ids
    print('vacancies_found : vacancies_added')
    while res['items']:
        time.sleep(0.1)
        try:
            res = ses.get(URL, params=params).json()
            if 'errors' in res.keys():
                print(res['errors'])
                return False
            vacancies_found = res['found']
            vacancies = [(item['id'], item['published_at']) for item in res['items']]

        except Exception as ex:
            print('Error:', ex)
            print('res=', res)
            return False

        query = ''
        for vac_id, published_at in vacancies:
            published_at = f'"{published_at}"'
            query = f'{query}' \
                    f'{db_op.insert_into_table("vacancy_ids", ["vac_id", "publish_date"], [vac_id, published_at])}\n'

        db_op.execute_query(query)

        print(f'\r {vacancies_found:14d} :{len(res["items"]):16d}', end='')
        params['page'] += 1
        if params['page'] == res['pages']-1:
            last_vacancy_date = res["items"][-1]["published_at"]
            params['date_to'] = last_vacancy_date
            params['page'] = 0

    return True


def parse_vacancy_skills(vac_id, specialization='1', database_name=db_op.DATA_BASE):

    URL = 'https://api.hh.ru/vacancies'
    vac_res = {}
    try:
        ses = requests.Session()
        ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
        vac_res = ses.get(f'{URL}/{vac_id}').json()
        if 'errors' in vac_res.keys():
            print(vac_res['errors'])
            return False
        if specialization not in [s['profarea_id'] for s in vac_res['specializations']]:
            return False
        skills = vac_res['key_skills']
        published_at = vac_res['published_at']

    except Exception as ex:
        print('Error:', ex)
        print(vac_res)
        return False

    if skills:  # at least one skill present
        skills = [skill['name'] for skill in skills]
    else: return False

    return vac_id, published_at, skills


if __name__ == '__main__':
    print(get_vacancies_id_list())

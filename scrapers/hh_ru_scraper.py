""" Scraping vacancies from hh.ru.

As argument use word or phrase in double quotes.
Saves results to ./data/raw-tags_{phrase_to_search}.json' file

"""


import datetime
import json
import sys
import time
import requests


def get_vacancies_id_list(database_name='test.db', specialization = 1, phrase_to_search = False):
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
    if phrase_to_search: params['text']= phrase_to_search

    res = {}
    vacancies_ids = set()
    URL = 'https://api.hh.ru/vacancies'

    try:
        ses = requests.Session()
        ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
        res = ses.get(URL, params=params).json()
    except Exception as ex:
        print('Error:', ex)
        print('res=', res)
        return False

    # getting list of all vacancies ids
    print('vacancies_found : vacancies_added : vacancies_all_saved')
    while res['items']:
        time.sleep(0.5)
        try:
            res = ses.get(URL, params=params).json()
            vacancies_found = res['found']
            vacancies_ids.update([item['id'] for item in res['items']])
        except Exception as ex:
            print('Error:', ex)
            print('res=', res)
            return vacancies_ids

        print(f'\r {vacancies_found:14d} :{len(res["items"]):16d} :{len(vacancies_ids):15d}', end='')
        params['page'] += 1
        if params['page'] == res['pages']-1:
            last_vacancy_date = res["items"][-1]["published_at"]
            params['date_to'] = last_vacancy_date
            params['page'] = 0

    return vacancies_ids


# def parse_vacancy_skill_tags(database_name, ):
#     # parsing vacancy pages and scraping tags from each vacancy
#     URL = 'https://api.hh.ru/vacancies'
#
#     try:
#         ses = requests.Session()
#         ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
#     except Exception as ex:
#         print('Error:', ex)
#
#     tags_list = []
#
#     for vac_id in vacancies_ids:
#         vac_res = ses.get(f'{URL}/{vac_id}')
#         skills = vac_res.json()['key_skills']
#         if skills:  # at least one skill present
#             print(vac_id)
#             tags = [skill['name'] for skill in skills]
#             print(' '.join(tags))
#             tags_list.append(tags)
#             print()
#         time.sleep(0.1)  # not to overload the server
#
#     res = {'parse_date': str(datetime.datetime.now()),
#            'phrase': phrase_to_search,
#            'items_number': len(tags_list),
#            'items': tags_list}
#
#     with open(save_path, 'w', encoding='utf8') as fp:  # serializing
#         json.dump(res, fp, ensure_ascii=False)
#
#     return tags_list


if __name__ == '__main__':
    get_vacancies_id_list()

""" Scraping vacancies from hh.ru.

As argument use word or phrase in double quotes.

Example:
    "phrase ro search" """


import sys
import requests
import time
import pickle


def scrape(phrase_to_search):
    ses = requests.Session()
    ses.headers = {'HH-User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"}

    url = f'https://api.hh.ru/vacancies?text={phrase_to_search}&per_page=100'
    res = ses.get(url)

    # getting list of all vacancies ids
    res_all = []
    for p in range(res.json()['pages']):
        time.sleep(0.5)
        print(f'scraping page {p}')
        url_p = url + f'&page={p}'
        res = ses.get(url_p)
        res_all.append(res.json())

    # parcing vacancies ids, getting vacancy page and scraping tags from each vacancy
    tags_list = []
    for page_res_json in res_all:
        for item in page_res_json['items']:
            vac_id = item['id']
            vac_res = ses.get(f'https://api.hh.ru/vacancies/{vac_id}')
            if len(vac_res.json()["key_skills"]) > 0:  # at least one skill present
                print(vac_id)
                tags = [v for v_dict in vac_res.json()["key_skills"] for _, v in v_dict.items()]
                print(' '.join(tags))
                tags_list.append(tags)
                print()
            time.sleep(0.1)  # not to overload the server

    with open(f"raw-tags_{phrase_to_search}.pkl", "wb") as fp:  # Pickling
        pickle.dump(tags_list, fp)

    return tags_list


if __name__ == '__main__':
    phrase_to_search = sys.argv[1]
    tags_list = scrape(phrase_to_search)

"""
Scraping vacancies from hh.ru.
"""

from datetime import datetime, timedelta
import time
import requests
import sql_db_operation as db_op

URL = 'https://api.hh.ru/vacancies'


def create_session(url=URL):
    try:
        ses = requests.Session()
        ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
        res = ses.get(url)
        return ses
    except Exception as ex:
        print('Error:', ex)
        return False


def get_vacancies_id_list(session, specialization=1, phrase_to_search=False):

    date_to = datetime.now().replace(microsecond=0)
    date_from = date_to - timedelta(days=2)

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
    try:
        res = session.get(URL, params=params).json()
        if 'errors' in res.keys():
            print(res['errors'])
            return False
    except Exception as ex:
        print('Error:', ex)
        print('res=', res)
        return False

    print('vacancies_found : vacancies_added')
    while res['items']:
        time.sleep(0.1)
        try:
            res = session.get(URL, params=params).json()
            if 'errors' in res.keys():
                print(res['errors'])
                return False
            vacancies_found = res['found']
            vacancies = [(item['id'], item['published_at']) for item in res['items']]

        except Exception as ex:
            print('Error:', ex)
            print('res=', res)
            return False

        insert_vac_ids_to_db(vacancies)

        print(f' {vacancies_found:14d} :{len(res["items"]):16d}')
        params['page'] += 1
        if params['page'] == res['pages']-1:
            last_vacancy_date = res["items"][-1]["published_at"]
            params['date_to'] = last_vacancy_date
            params['page'] = 0

    return True


def insert_vac_ids_to_db(vacancies, db_name=db_op.DATA_BASE):
    script = ''
    for vac_id, published_at in vacancies:
        published_at = f'"{published_at[0:10]}"'
        script = f'{script}' \
                 f'{db_op.insert_into_table("vacancy_ids", ["vac_id", "publish_date"], [vac_id, published_at])}\n'

    return db_op.execute_script(script)


def update_skills_table_on_db(vac_ids, list_of_skills_id, db_name=db_op.DATA_BASE):
    script = ''
    for vac_id, skills_ids in zip(vac_ids, list_of_skills_id):
        if skills_ids:
            skills_ids = ['parsed'] + skills_ids
            script = f'{script}' \
                     f'{db_op.update_table("vacancy_ids", skills_ids,["1"]*(len(skills_ids)+1), f"vac_id = {vac_id}")}\n'
        else:
            script = f'{script}' \
                    f'{db_op.update_table("vacancy_ids", ["parsed"],["0"], f"vac_id = {vac_id}")}\n'
    # print(script)
    return db_op.execute_script(script)


def get_unparsed_vac_ids_from_db(db_name=db_op.DATA_BASE):
    query = db_op.select_data('vacancy_ids', ['vac_id'], 'parsed IS NULL')
    query = f'{query} LIMIT 10;'
    vacancies = db_op.execute_query(query)
    return [vac[0] for vac in vacancies]


def parse_vacancy_skills(session, vac_id, specialization='1', db_name=db_op.DATA_BASE):
    vac = {}
    try:
        vac = session.get(f'{URL}/{vac_id}').json()

        if 'errors' in vac.keys():
            print(vac['errors'])
            return False

        s = vac['specializations']
        if len(s) > 2*len([s['profarea_id'] for s in s if s['profarea_id'] == specialization]):
            return False

        skills = vac['key_skills']

    except Exception as ex:
        print('Error:', ex)
        print(vac)
        return False

    if skills:  # at least one skill present
        skills = [skill['name'] for skill in skills]
    else: return False

    return skills


def get_all_skills(db_name=db_op.DATA_BASE):
    query = db_op.select_data('all_skills', ['skill_id', 'skill'], 'TRUE')
    return db_op.execute_query(query)


def update_all_skills_on_db(new_skills, db_name=db_op.DATA_BASE):
    script = ''
    for skill in new_skills:
        skill = f'"{skill}"'
        script = f'{script}' \
                 f'{db_op.insert_into_table("all_skills", ["skill"], [skill])}\n'

    # print(script)
    return db_op.execute_script(script)


def alter_table_on_db(new_skills, db_name=db_op.DATA_BASE):
    script = ''
    for skill in new_skills:
        script = f'{script}' \
                 f'{db_op.add_column("vacancy_ids", skill)}INTEGER ;\n'
    # print(script)
    return db_op.execute_script(script)


def processing_vac_skills(session, db_name=db_op.DATA_BASE):
    vac_ids = get_unparsed_vac_ids_from_db()
    print('________________________')
    if not vac_ids:
        print('All vacancies in db have parsed')
        return 'DONE'
    list_of_skills = []
    for vac_id in vac_ids:
        vac_skills = parse_vacancy_skills(session, vac_id)
        if vac_skills:
            list_of_skills.append([skill.upper() for skill in vac_skills])
        else:
            list_of_skills.append(False)

    newly_parsed_skills = set()
    for skills in list_of_skills:
        if skills:
            newly_parsed_skills.update(set(skills))

    all_skills = get_all_skills()
    new_unique_skills = newly_parsed_skills.difference({skill[1] for skill in all_skills})

    if new_unique_skills:
        update_all_skills_on_db(new_unique_skills)

    all_skills = get_all_skills()
    all_skills_dic = {skill[1]: skill[0] for skill in all_skills}
    new_unique_skills_ids = [f'skill_id_{all_skills_dic[skill]}' for skill in new_unique_skills]
    alter_table_on_db(new_unique_skills_ids)
    list_of_skills_ids = [[f'skill_id_{all_skills_dic[skill]}' for skill in skills] if skills else False
                          for skills in list_of_skills]
    update_skills_table_on_db(vac_ids, list_of_skills_ids)
    return True


if __name__ == '__main__':
    ses = create_session()
    # get_vacancies_id_list(ses)
    p = processing_vac_skills(ses)
    while p != 'DONE':
        p = processing_vac_skills(ses)
    ses.close()

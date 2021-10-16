import sqlite3 as sq

DATA_BASE = "scrapers/sql_database/hh_vacancies.db"


def execute_script(script, db_name=DATA_BASE):
    try:
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.executescript(script)
            return True
    except Exception as ex:
        print(ex)
        return False


def execute_query(query, db_name=DATA_BASE):
    try:
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute(query)
            return cur.fetchall()
    except Exception as ex:
        print(ex)
        return


def query_generator(pattern: str, options: list):
    query = pattern
    for a in options:
        query = query.replace('|?|', a, 1)
    return query


def create_table(table_name: str, columns: list):
    pattern = """ CREATE TABLE IF NOT EXISTS |?| ( |?| ) """
    return query_generator(pattern, [table_name, ','.join(columns)])


def add_column(table_name: str, column: str):
    pattern = """ ALTER TABLE |?| ADD COLUMN |?| """
    return query_generator(pattern, [table_name, column])


def insert_into_table(table_name: str, columns: list, values: list):
    pattern = """ INSERT INTO |?| ( |?| ) VALUES ( |?| ) ;"""
    return query_generator(pattern, [table_name, ','.join(columns), ','.join(values)])


def update_table(table_name: str, columns: list, values: list, conditions: str):
    pattern = """ UPDATE |?| SET |?| WHERE |?| ;"""
    return query_generator(pattern,
                           [table_name, ','.join([f'{col}={val}' for col, val in zip(columns, values)]), conditions])


def select_data(table_name: str, columns: list, conditions: str):
    pattern = """ SELECT |?| FROM |?| WHERE |?| """
    return query_generator(pattern, [','.join(columns), table_name, conditions])


if __name__ == '__main__':
    query = select_data("vacancy_ids", ["vac_id"], 'vac_id<40000000')
    print(query)
    print(execute_query(query))

import sqlite3 as sq

DATA_BASE = "scrapers/sql_database/hh_vacancies.db"


def execute_query(query, db_name=DATA_BASE):
    try:
        with sq.connect(db_name) as con:
            cursor = con.cursor()
            cursor.executescript(query)
            row = cursor.fetchall()
        return row
    except Exception as ex:
        print(ex)
        return False


def query_generator(query: str, options: list):
    for a in options:
        query = query.replace('|?|', a, 1)
    return query


def create_table(table_name: str, columns: list):
    pattern = """ CREATE TABLE IF NOT EXISTS |?| ( |?| ) """
    return query_generator(pattern, [table_name, ','.join(columns)])


def add_column(table_name: str, column: str):
    pattern = """ ALTER TABLE |?| ADD COLUMN |?| ;"""
    return query_generator(pattern, [table_name, column])


def insert_into_table(table_name: str, columns: list, values: list):
    pattern = """ INSERT INTO |?| ( |?| ) VALUES ( |?| ) ;"""
    return query_generator(pattern, [table_name, ','.join(columns), ','.join(values)])


def update_table(table_name: str, columns: list, values: list, conditions: str):
    pattern = """ UPDATE |?| SET |?| WHERE |?| ;"""
    return query_generator(pattern,
                           [table_name, ','.join([f'{col}={val}' for col, val in zip(columns, values)]), conditions])




if __name__ == '__main__':
    query = insert_into_table("vacancy_ids", ["vac_id", "publish_date"], ['23423423', "'fdfsdf234-34f'"])
    print(query)
    execute_query(query)

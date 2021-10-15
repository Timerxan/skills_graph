import sqlite3 as sq

DATA_BASE = "scrapers/sql_database/hh_vacancies.db"


def execute_query(db_name, query):
    try:
        with sq.connect(db_name) as con:
            cursor = con.cursor()
            cursor.execute(query)
        return True
    except Exception as ex:
        print(ex)
        return False


def query_generator(query: str, options: list):
    for a in options:
        query = query.replace('|?|', a, 1)
    return query


def create_table(table_name: str, columns: list, db_name=DATA_BASE):
    pattern = """ CREATE TABLE IF NOT EXISTS |?| ( |?| ) """
    query = query_generator(pattern, [table_name, ','.join(columns)])
    return execute_query(db_name, query)


def add_column(table_name: str, column: str, db_name=DATA_BASE):
    pattern = """ ALTER TABLE |?| ADD COLUMN |?| """
    query = query_generator(pattern, [table_name, column])
    return execute_query(db_name, query)


def insert_into_table(table_name: str, columns: list, values: list, db_name=DATA_BASE):
    pattern = """ INSERT INTO |?| ( |?| ) VALUES ( |?| ) """
    query = query_generator(pattern, [table_name, ','.join(columns), ','.join(values)])
    return execute_query(db_name, query)


def update_table(table_name: str, columns: list, values: list, conditions: str, db_name=DATA_BASE):
    pattern = """ UPDATE |?| SET |?| WHERE |?| """
    query = query_generator(pattern,
                            [table_name, ','.join([f'{col}={val}' for col, val in zip(columns, values)]), conditions])
    return execute_query(db_name, query)

if __name__ == '__main__':
    update_table('skills_by_day', ['skill_1', 'skill_2'], ['5', '2'], 'day = 5')


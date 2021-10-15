import sqlite3 as sq


def execute_query(query):
    with sq.connect("scrapers/sql_database/hh_vacancies.db") as con:
        cursor = con.cursor()
        cursor.execute(query)


query_create_table = """
CREATE TABLE IF NOT EXISTS skills_by_day 
(
day INTEGER
)
"""
query_add_column = """
ALTER TABLE skills_by_day ADD COLUMN skill2
"""
query_insert_into_table = """
INSERT INTO skills_by_day (day,skill)
VALUES (15,3)
"""
query_update_table = """
UPDATE skills_by_day
SET skill = skill +1
"""


if __name__ == '__main__':
    execute_query(query_add_column)

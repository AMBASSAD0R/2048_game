# программа ответственная за SQL БД


import sqlite3

# создание связи с SQL базой
con = sqlite3.connect("2048.sqlite")

# создание курсора
cur = con.cursor()

# создание SQL БД
cur.execute("""
create table if not exists RECORDS (
    name text,
    score integer
)""")


def insert_result(name, score):
    """добавление данных в БД"""
    cur.execute("""
        INSERT into RECORDS values (?, ?)
    """, (name, score))
    con.commit()


def get_best():
    """получение лучшего результата из БД"""
    cur.execute("""
    SELECT name gamer, max(score) score FROM RECORDS
    GROUP BY name
    ORDER BY score DESC
    LIMIT 3
    """)
    return cur.fetchall()

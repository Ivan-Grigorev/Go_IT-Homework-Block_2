import datetime
import random
import faker

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error


try:
    connection = psycopg2.connect(user='**********',
                                  password='**********',
                                  host='127.0.0.1',
                                  port='5432',
                                  database='**********'
                                  )

    cursor = connection.cursor()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    sql_query = 'INSERT INTO grades VALUES (%s, %s, %s, %s, %s)'
    grade_id = 0

    for i in range(1, 31):
        titles = ['Programming', 'Psychics', 'History', 'English', 'Algebra']
        for j in titles * 4:
            grade_id += 1
            cursor.execute(sql_query, (grade_id, i, j, random.randrange(1, 6), faker.Faker().date_between(
                datetime.date(year=2021, month=1, day=1), end_date='now')))

except (Exception, Error) as error:
    print("Error", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgresSQL connection is closed")

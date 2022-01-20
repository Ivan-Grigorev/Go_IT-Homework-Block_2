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

    sql_query = 'INSERT INTO students VALUES (%s, %s, %s)'
    for i in range(1, 31):
        groups = ['A', 'B', 'C']
        fake_name = faker.Faker().name()
        cursor.execute(sql_query, (i, fake_name, random.choice(groups)))

except (Exception, Error) as error:
    print("Error", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

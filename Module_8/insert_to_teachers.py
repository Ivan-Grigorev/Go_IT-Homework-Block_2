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

    sql_query = 'INSERT INTO teachers VALUES (%s, %s)'
    for i in range(1, 4):
        fake_teacher = 'Prof.' + faker.Faker().last_name()
        cursor.execute(sql_query, (i, fake_teacher))

except (Exception, Error) as error:
    print("Error", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

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

    sql_query = """INSERT INTO lessons (id, title, teacher)
                    VALUES (1, 'Programming', 'Prof.Bennett'),
                            (2, 'Psychics', 'Prof.Washington'),
                            (3, 'History', 'Prof.Williams'),
                            (4, 'English', 'Prof.Washington'),
                            (5, 'Algebra', 'Prof.Bennett')"""
    cursor.execute(sql_query)

except (Exception, Error) as error:
    print("Error", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgresSQL connection is closed")

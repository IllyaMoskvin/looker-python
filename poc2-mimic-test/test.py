
import pymysql.cursors

connection = pymysql.connect(host='127.0.0.1')
cursor = connection.cursor()

query = """
    SELECT
        foo,
        bar,
    FROM
        `baz`
    WHERE
        foo = %s AND bar = %s
"""

cursor.execute(query, (2, 2))

result = cursor.fetchall()
print(result)

cursor.close()
connection.close()

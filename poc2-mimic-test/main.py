import os
import sys
import pymysql.cursors

host = os.environ.get("DB_HOST", "localhost")
password = os.environ.get("DB_PASS", "does_not_matter")

connection = pymysql.connect(
    host=host,
    user='looker',
    password=password,
    db='does_not_matter',
)
cursor = connection.cursor()

query = """
    SELECT
        foo,
        bar,
        date,
        revenue,
    FROM
        `does_not_matter`
    WHERE
        foo = %s AND bar = %s
"""

cursor.execute(
    query,
    (
        int(sys.argv[1]) if len(sys.argv) > 1 else 0,
        sys.argv[2] if len(sys.argv) > 2 else "Scenario B",
    )
)

result = cursor.fetchall()
print(result)

cursor.close()
connection.close()

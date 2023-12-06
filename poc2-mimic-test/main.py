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
        (DATE(CONVERT_TZ(poc2.date,'UTC','America/Los_Angeles'))) AS `poc2.date`,
        SUM(poc2.revenue)  AS `poc2.revenue`
    FROM poc2
        WHERE (poc2.foo) = %s AND (poc2.bar) = %s
    GROUP BY
        1
    ORDER BY
        1
    LIMIT 5000
"""

cursor.execute(
    query,
    (
        int(sys.argv[1]) if len(sys.argv) > 1 else 123,
        sys.argv[2] if len(sys.argv) > 2 else "ABC",
    )
)

result = cursor.fetchall()
print(result)

cursor.close()
connection.close()

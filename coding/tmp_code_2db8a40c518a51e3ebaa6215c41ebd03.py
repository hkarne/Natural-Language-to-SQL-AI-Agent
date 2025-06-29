import os
import subprocess
import json
import psycopg2

try:
    subprocess.check_call(['pip', 'install', 'psycopg2-binary'])
except subprocess.CalledProcessError as e:
    print(json.dumps({"columns": [], "results": []}))
    exit(1)


def query_database(query):
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=int(os.environ['DB_PORT']),
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        cur = conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        conn.close()
        return columns, results
    except (psycopg2.Error, KeyError) as e:
        print(json.dumps({"columns": [], "results": []}))
        exit(1)


query = """
SELECT first_name, last_name, MAX(salary)
FROM employees
GROUP BY first_name, last_name
ORDER BY MAX(salary) DESC
LIMIT 1;
"""

columns, results = query_database(query)

print(json.dumps({'columns': columns, 'results': [list(row) for row in results]}))

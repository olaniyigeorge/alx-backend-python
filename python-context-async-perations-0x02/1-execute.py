import sqlite3
from contextlib import contextmanager

@contextmanager
def execute_query(db_name, query, params=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or [])
        results = cursor.fetchall()
        yield results
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Query failed: {e}")
        raise
    finally:
        conn.close()


query = "SELECT * FROM User WHERE first_name=?"
params = ("Og",)

with execute_query("users.db", query, params) as result:
    print(result)

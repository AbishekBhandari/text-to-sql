import logging
from .database import get_conn
from .validator import validate
from .llm import call_llm

logging.basicConfig(filename="logs/agent.log", level=logging.INFO)


def execute(sql):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(sql)

    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    result = [dict(zip(cols, r)) for r in rows]

    cur.close()
    conn.close()

    return result


def repair_sql(sql, error):

    prompt = f"""
Fix this PostgreSQL query.

SQL:
{sql}

Error:
{error}

Return ONLY SQL.
"""

    return call_llm(prompt).replace("```sql", "").replace("```", "").strip()
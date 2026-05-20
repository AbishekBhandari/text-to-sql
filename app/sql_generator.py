from .llm import call_llm


def generate_sql(decomposition):

    prompt = f"""
You are a PostgreSQL expert.

Convert this structured plan into SQL.

Rules:
- SELECT only
- Use joins correctly
- Use aliases
- Optimize query

Input:
{decomposition}

Return ONLY SQL.
"""

    sql = call_llm(prompt)

    return sql.replace("```sql", "").replace("```", "").strip()
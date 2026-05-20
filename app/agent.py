import time
import logging

from .llm_decomposer import decompose
from .sql_generator import generate_sql
from .executor import execute, repair_sql
from .validator import validate
from .llm import call_llm

logging.basicConfig(filename="logs/agent.log", level=logging.INFO)


def summarize(question, result):

    prompt = f"""
Question: {question}
SQL Result: {result}

Explain this in simple natural language.
"""

    return call_llm(prompt)


def run_agent(question):

    # STEP 1: Decomposition
    decomposition = decompose(question)
    logging.info(f"DECOMPOSITION: {decomposition}")

    # STEP 2: SQL generation
    sql = generate_sql(decomposition)
    logging.info(f"SQL: {sql}")

    retries = 0
    max_retries = 3

    while retries < max_retries:

        try:
            validate(sql)

            start = time.time()
            result = execute(sql)
            end = time.time()

            logging.info(f"EXEC TIME: {end-start}")

            summary = summarize(question, result)

            return {
                "question": question,
                "decomposition": decomposition,
                "sql": sql,
                "result": result,
                "summary": summary,
                "status": "success"
            }

        except Exception as e:

            logging.error(str(e))

            sql = repair_sql(sql, str(e))
            retries += 1

    return {
        "question": question,
        "decomposition": decomposition,
        "sql": sql,
        "result": None,
        "summary": "Failed after retries",
        "status": "failed"
    }
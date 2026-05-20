import csv
import json
import re
import pandas as pd
from .llm import call_llm

# --- Your existing code ---
def extract_json(text):
    text = text.strip()
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group()
    raise Exception(f"No JSON found:\n{text}")

def decompose(question):
    prompt = f"""
You are an experienced SQL analyst.
Break the question into structured JSON.
Return ONLY JSON.
Format:
{{
    "intent":"",
    "tables":[],
    "columns":[],
    "filters":[],
    "joins":[]
}}
Question:
{question}
DO NOT explain.
DO NOT add markdown.
JSON ONLY.
"""
    result = call_llm(prompt)
    clean = extract_json(result)
    return json.loads(clean)


# --- New Function to Return a List of JSON Objects ---
def get_decomposed_list_from_csv(csv_path, question_column_name="question"):
    """
    Reads a CSV file, decomposes every question, and returns a 
    list of dictionaries (JSON objects).
    """
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    if question_column_name not in df.columns:
        raise ValueError(f"Column '{question_column_name}' not found in the CSV.")

    decomposed_questions_list = []

    print(f"Processing {len(df)} questions from CSV...")

    for index, row in df.iterrows():
        question = row[question_column_name]
        
        try:
            # Get the JSON components from the LLM
            components = decompose(question)
            
            # Append the structured dictionary to our list
            decomposed_questions_list.append({
                "original_question": question,
                "intent": components.get("intent", ""),
                "tables": components.get("tables", []),
                "columns": components.get("columns", []),
                "filters": components.get("filters", []),
                "joins": components.get("joins", [])
            })
            
        except Exception as e:
            print(f"❌ Failed to decompose row {index + 1} ('{question}'): {e}")
            # Optional: Append an empty/error structure so indices align with the CSV
            decomposed_questions_list.append({
                "original_question": question,
                "intent": "ERROR_PARSING_LLM_OUTPUT",
                "tables": [],
                "columns": [],
                "filters": [],
                "joins": []
            })

    return decomposed_questions_list


# --- Example Usage ---
if __name__ == "__main__":
    # 1. Run the processing function
    results = get_decomposed_list_from_csv(
        csv_path="sql_questions.csv", 
        question_column_name="question"
    )
    
    # 2. View the resulting Python list of JSON objects
    print("\n--- Final Structured List Output ---")
    print(json.dumps(results, indent=4))
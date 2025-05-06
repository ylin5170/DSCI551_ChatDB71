import openai
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_sql_output(response_text):
    # Extract SQL inside ```sql ... ``` if it exists
    match = re.search(r"```sql\s*(.+?)```", response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    lines = response_text.strip().splitlines()
    cleaned_lines = [line for line in lines if not re.match(r"^(sure|here|you can|to)", line.strip().lower())]
    return "\n".join(cleaned_lines).strip()

def natural_language_to_sql(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a MySQL query generator for a movie database. "
                    "Only use the following tables and their columns:\n"
                    "- title_basics(tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)\n"
                    "- title_ratings(tconst, averageRating, numVotes)\n"
                    "- title_principals(tconst, ordering, nconst, category, job, characters)\n"
                    "When inserting new rows, always use a unique tconst that starts with 'tt999' (e.g., 'tt999001', 'tt999002'). "
                    "Do NOT use 'tt1234567'.\n"     
                    "Only return clean MySQL queries. Do NOT include explanations, markdown, or any extra text."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_sql = response.choices[0].message.content
    return clean_sql_output(raw_sql)
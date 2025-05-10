
from openai import OpenAI
from pymongo import MongoClient
import json

# --- DB setup ---------------------------------------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["IMDB"]
akas = db["title_akas"]

# --- OpenAI client (API key comes from env var OPENAI_API_KEY) --------------
openai_client = OpenAI()

# --- Prompt -----------------------------------------------------------------
SYSTEM_PROMPT = r"""
You translate natural-language *mutation* requests into structured MongoDB
commands for the "title_akas" collection (IMDb alias data).

Return STRICT JSON only — no markdown, no commentary.

Schema keys:
  titleId (string)      – FK to title_basics.tconst
  region (string, 2-letter)
  language (string, 2-letter ISO-639-1)
  title  (string)       – the alias text
  isOriginalTitle (0/1) – optional, default 0

Required JSON format:
{
  "action": "insert" | "update" | "delete",
  "collection": "title_akas",
  "data": { ... }           // see below
}

insert → "data" is the full document to insert.
update → "data" contains:
          "filter": { ... },   // match condition
          "update": { ... }    // fields to set
delete → "data" is the match condition.

If the user requests multiple inserts, return one object with
action:"insertMany" and data:[ {...}, {...}, ... ]  (array of documents).

For update/delete actions, the "filter" MUST include titleId
PLUS at least one of {region, language, title} so that it matches exactly
one document.

Examples
--------
User: Add a US English alias "Demo Movie" for tt1234567
→
{
  "action": "insert",
  "collection": "title_akas",
  "data": {
    "titleId": "tt1234567",
    "region": "US",
    "language": "en",
    "title": "Demo Movie",
    "isOriginalTitle": 0
  }
}
"""

# ---------------------------------------------------------------------------

def nl_to_mutation(nl_input: str) -> str:
    """Parse NL mutation, execute, and return human message."""
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": nl_input}
        ]
    )

    raw_reply = response.choices[0].message.content
    print("GPT‑raw:", raw_reply)
    try:
        parsed = eval(raw_reply)
    except Exception as e:
        return f" JSON parse error: {e}\nRaw: {raw_reply}"
    if isinstance(parsed, list):
        docs = [p["data"] for p in parsed if p.get("action") == "insert"]
        try:
            result = akas.insert_many(docs)
            return f"Inserted {len(result.inserted_ids)} documents."
        except Exception as e:
            return f" insertMany failed: {e}"
    if not isinstance(parsed, dict):
        return "Unexpected GPT structure."

    # --- strict JSON parse ---------------------------------------------------
    

    action = parsed.get("action")
    data   = parsed.get("data", {})

    # --- INSERT --------------------------------------------------------------
    if action == "insert":
        try:
            result = akas.insert_one(data)
            return f"Inserted alias. _id = {result.inserted_id}"
        except Exception as e:
            return f" Insert failed: {e}"

    # --- UPDATE --------------------------------------------------------------
    elif action == "update":
        filt  = data.get("filter")
        patch = data.get("update")
        if not isinstance(filt, dict) or not isinstance(patch, dict):
            return " GPT returned invalid update structure."
        update_doc = patch if any(k.startswith("$") for k in patch) else {"$set": patch}
        try:
            result = akas.update_one(filt, update_doc)
            return f"Updated {result.modified_count} record(s)."
        except Exception as e:
            return f"Update failed: {e}"
    elif action == "insertMany":
        if not isinstance(data, list):
            return " insertMany expects an array in 'data'."
        try:
            result = akas.insert_many(data)
            return f" Inserted {len(result.inserted_ids)} documents."
        except Exception as e:
            return f" insertMany failed: {e}"
    # --- DELETE --------------------------------------------------------------
    elif action == "delete":
        try:
            result = akas.delete_one(data)
            return f" Deleted {result.deleted_count} record(s)."
        except Exception as e:
            return f" Delete failed: {e}"

    else:
        return" Unknown or unsupported action."
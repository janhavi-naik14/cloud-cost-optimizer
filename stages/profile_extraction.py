import json
import os
from utils.groq_client import get_groq_client
from utils.json_utils import extract_json_object

DATA_DIR = "data"
PROFILE_PATH = os.path.join(DATA_DIR, "project_profile.json")
DESC_PATH = os.path.join(DATA_DIR, "project_description.txt")


PROFILE_EXTRACTION_PROMPT = """
You are a strict JSON generator.

TASK:
Convert the given project description into a CLEAN and structured JSON object.

MANDATORY RULES:
- Output ONLY valid JSON
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include comments
- Follow the schema EXACTLY
- Normalize spelling mistakes and informal words
- Normalize technology names (e.g., "react js" → "React", "mongo" → "MongoDB")
- Infer a reasonable project name if not explicitly stated
- If a value cannot be reasonably inferred, use null
- If MULTIPLE alternatives are mentioned (e.g., "AWS or GCP"),
  preserve ALL options joined using " / " (slash), do NOT pick one

REQUIRED JSON SCHEMA:
{
  "name": string,
  "budget_inr_per_month": number | null,
  "description": string,
  "tech_stack": {
    "frontend": string | null,
    "backend": string | null,
    "database": string | null,
    "proxy": string | null,
    "hosting": string | null
  },
  "non_functional_requirements": array
}

PROJECT DESCRIPTION:
\"\"\"
{project_description}
\"\"\"
"""


def extract_project_profile():
    if not os.path.exists(DESC_PATH):
        raise FileNotFoundError("project_description.txt not found")

    with open(DESC_PATH, "r", encoding="utf-8") as f:
        project_description = f.read()

    prompt = PROFILE_EXTRACTION_PROMPT.replace(
    "{project_description}", project_description
)


    client = get_groq_client()

    for _ in range(3):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON"},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1200,
        )

        content = response.choices[0].message.content
        parsed = extract_json_object(content)

        if parsed:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(PROFILE_PATH, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2)
            return

    raise ValueError("Profile extraction failed")

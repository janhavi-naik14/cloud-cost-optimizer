import json
import os
from utils.groq_client import get_groq_client
from utils.json_utils import extract_json_array

DATA_DIR = "data"
PROFILE_PATH = os.path.join(DATA_DIR, "project_profile.json")
BILLING_PATH = os.path.join(DATA_DIR, "mock_billing.json")


BILLING_GENERATION_PROMPT = """
You are a strict JSON generator.

TASK:
Generate a JSON array of synthetic cloud billing records.

RULES:
- Output ONLY valid JSON
- Do NOT include explanations, markdown, or extra text
- Generate BETWEEN 12 AND 20 records
- Cloud-agnostic services
- Realistic values

IMPORTANT:
- The project profile may contain multiple alternatives
  (e.g., "AWS / GCP", "MySQL / PostgreSQL")
- For THIS billing run, select ONE reasonable option per category
- Do NOT generate billing for multiple alternatives at once
- Assume a single realistic deployment scenario

EACH RECORD MUST INCLUDE:
month, service, resource_id, region,
usage_type, usage_quantity, unit, cost_inr, desc

PROJECT PROFILE:
{project_profile}
"""


def generate_mock_billing():
    # Skip generation if billing already exists
    if os.path.exists(BILLING_PATH):
        return

    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        project_profile = json.load(f)

    prompt = BILLING_GENERATION_PROMPT.replace(
    "{project_profile}",
    json.dumps(project_profile, indent=2)
)



    client = get_groq_client()

    for _ in range(3):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return ONLY a valid JSON array. "
                        "Start with '[' and end with ']'."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=2000,
        )

        content = response.choices[0].message.content
        parsed = extract_json_array(content)

        if parsed and 12 <= len(parsed) <= 20:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(BILLING_PATH, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2)
            return

    raise ValueError("Billing generation failed")

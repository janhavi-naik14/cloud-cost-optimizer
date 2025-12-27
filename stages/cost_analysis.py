import json
import os
from utils.groq_client import get_groq_client
from utils.json_utils import extract_json_object

DATA_DIR = "data"
PROFILE_PATH = os.path.join(DATA_DIR, "project_profile.json")
BILLING_PATH = os.path.join(DATA_DIR, "mock_billing.json")
REPORT_PATH = os.path.join(DATA_DIR, "cost_optimization_report.json")


COST_ANALYSIS_PROMPT = """
You are a strict JSON generator and cloud cost optimization engine.

OUTPUT RULES (MANDATORY):
- Output ONLY valid JSON
- Do NOT include explanations, markdown, or extra text
- Follow the JSON structure EXACTLY
- Do NOT rename fields
- Do NOT omit any field
- Do NOT add extra fields
- Numbers must be numbers (not strings)

REQUIRED JSON FORMAT:
{
  "project_name": string,
  "analysis": {
    "total_monthly_cost": number,
    "budget": number | null,
    "budget_variance": number,
    "service_costs": {
      "<service_name>": number
    },
    "high_cost_services": {
      "<service_name>": number
    },
    "is_over_budget": boolean
  },
  "recommendations": [
    {
      "title": string,
      "service": string,
      "current_cost": number,
      "potential_savings": number,
      "recommendation_type": "open_source" | "free_tier" | "alternative_provider" | "optimization" | "right_sizing",
      "description": string,
      "implementation_effort": "low" | "medium" | "high",
      "risk_level": "low" | "medium" | "high",
      "steps": [string, string, string],
      "cloud_providers": [string, string]
    }
  ],
  "summary": {
    "total_potential_savings": number,
    "savings_percentage": number,
    "recommendations_count": number,
    "high_impact_recommendations": number
  }
}

IMPORTANT (FOLLOW STRICTLY):
- Generate BETWEEN 6 AND 10 recommendations
- EACH recommendation MUST contain:
  title, service, current_cost, potential_savings
- Treat mock_billing.json as the CURRENT deployment
- Treat project_profile.json as AVAILABLE ALTERNATIVES
- Use alternatives from the profile (e.g., "AWS / GCP", "MySQL / PostgreSQL")
- cloud_providers MUST NOT be empty
- recommendation_type MUST be one of:
  open_source, free_tier, alternative_provider, optimization, right_sizing

BUDGET LOGIC (MANDATORY):
- If budget exists:
  - analysis.budget = budget_inr_per_month from project_profile.json
  - budget_variance = total_monthly_cost - budget
  - is_over_budget MUST be:
      true  → ONLY if total_monthly_cost > budget
      false → if total_monthly_cost <= budget

HIGH COST SERVICES LOGIC (MANDATORY):
- high_cost_services MUST include ONLY the TOP 1–3 highest-cost services
- Do NOT include low-cost services or regional duplicates

RECOMMENDATION DISTRIBUTION (HARD CONSTRAINT — DO NOT VIOLATE):
- Do NOT repeat the same cloud provider in every recommendation.
- The FULL SET of recommendations MUST include ALL of the following providers:
  1) AWS
  2) Azure
  3) GCP
  4) At least ONE Open-Source or Free-Tier solution
- At least ONE recommendation MUST be for Azure.
- At least ONE recommendation MUST be for GCP.
- At least ONE recommendation MUST be for an Open-Source / Free-Tier tool.
- cloud_providers MUST contain ONLY the providers that apply to THAT recommendation.
- Do NOT write values like "AWS / GCP" or "Multiple". Use a SINGLE concrete provider per recommendation.
- If a recommendation is Open-Source or Free-Tier, cloud_providers MUST contain ONLY ["Open-Source"] or ["Free-Tier"].
- If you are unsure, choose a reasonable cloud provider instead of combining names.
- If the above constraints cannot be satisfied, REGENERATE the recommendations until they are satisfied BEFORE producing the JSON output.


INPUT DATA:

PROJECT PROFILE:
{project_profile}

MOCK BILLING:
{mock_billing}
"""


def generate_cost_report():
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        project_profile = json.load(f)

    with open(BILLING_PATH, "r", encoding="utf-8") as f:
        mock_billing = json.load(f)

    prompt = (
    COST_ANALYSIS_PROMPT
        .replace("{project_profile}", json.dumps(project_profile, indent=2))
        .replace("{mock_billing}", json.dumps(mock_billing, indent=2))
)


    client = get_groq_client()

    for _ in range(3):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON"},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=2000,
        )

        content = response.choices[0].message.content
        parsed = extract_json_object(content)

        if parsed:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(REPORT_PATH, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2)
            return

    raise ValueError("Cost analysis failed")

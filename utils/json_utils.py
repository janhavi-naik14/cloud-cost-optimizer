import json
import re


def _clean_text(text: str) -> str:
    if not text:
        return ""

    # Remove code fences
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)

    # Normalize fancy quotes
    text = (
        text.replace("“", '"').replace("”", '"')
            .replace("’", "'").strip()
    )
    return text


def extract_json_object(text):
    text = _clean_text(text)

    # Try direct parse
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    # Fallback: extract first {...} block
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except Exception:
        return None


def extract_json_array(text):
    text = _clean_text(text)

    # Try direct parse
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass

    # Fallback: extract first [...] block
    match = re.search(r"\[[\s\S]*\]", text)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except Exception:
        return None

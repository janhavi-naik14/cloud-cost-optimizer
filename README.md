# Cloud Cost Optimization – LLM-Driven Pipeline

This project automatically analyzes a natural-language project description,
extracts a structured project profile, generates synthetic cloud billing data,
and produces a cloud cost optimization report — all powered entirely by an LLM.

No rule-based cost logic is embedded in the system. All analysis and
recommendations are generated purely by the LLM based on the project and billing
context.

---

## 🚀 Features

- Converts unstructured project description into a clean JSON project profile
- Handles spelling variations, informal wording, and noisy text inputs
- Supports descriptions containing **multiple technology options**
  (e.g., “AWS or GCP”, “MySQL / PostgreSQL”, “React js / Angular”)
- Generates realistic synthetic cloud billing records
- Produces an LLM-generated cost optimization report
- JSON-first, modular, and deterministic pipeline design

---

## 🧩 Pipeline Stages

1. **Profile Extraction** → `project_profile.json`  
2. **Mock Billing Generation** → `mock_billing.json`  
3. **Cost Optimization Report** → `cost_optimization_report.json`

All artifacts are stored in the `data/` directory.

---

## 🛠️ Tech Stack

- Python 3.x
- Groq LLM API (`llama-3.1-8b-instant`)  
  👉 https://groq.com
- JSON-based data processing

---

## 📦 Project Structure

```
stages/
  profile_extraction.py
  billing_generation.py
  cost_analysis.py

utils/
  groq_client.py
  json_utils.py

data/
  project_description.txt
  project_profile.json
  mock_billing.json
  cost_optimization_report.json

main.py
requirements.txt
.env.example
README.md
```

---

## 🔑 Environment Setup (Important)

The `.env` file is **not included in the repository** for security reasons.

Create a `.env` file in the project root and add your Groq API key manually:

```
GROQ_API_KEY=your_groq_api_key_here
```

Do **not** commit or upload your `.env` file.

---

## 🧪 Input Description Behavior

The system is designed to work with **real-world, messy descriptions**, including:

- multiple technology alternatives  
- informal wording  
- mixed casing  
- spelling mistakes  

Example interpretation:

```
"react js or angular, mongo or mysql"
→ Normalized to: "React", "Angular", "MongoDB", "MySQL"
```

The model **does not enforce rules** — it interprets and generates outputs
autonomously.

---

## ▶️ Run the Pipeline

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

Generated outputs will appear in `data/`.

---

## 🧾 Sample Artifacts (Included)

- `project_description.txt`
- `project_profile.json`
- `mock_billing.json`
- `cost_optimization_report.json`


## ✨ Notes

- Recommendations are **fully LLM-generated**  
- No deterministic or rule-based cost logic is applied  
- Outputs reflect the model’s reasoning based on the inputs provided

---

---
## 🛠️ Tools & References Used

- **Groq LLM API** – Primary LLM inference platform  
  https://groq.com

- **ChatGPT (OpenAI)** – Used as a development assistant during implementation  
  https://chat.openai.com

- **Hugging Face** – Referenced initially during experimentation and API testing  
  https://huggingface.co

- **Python** – Programming language used for pipeline implementation  
  https://www.python.org

- **Git & GitHub** – Version control and project repository hosting  
  https://git-scm.com  
  https://github.com

---

## 👤 Author

Janhavi Naik 
janhavi.141620@gmail.com


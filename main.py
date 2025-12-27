import os
import sys
import json
from stages.profile_extraction import extract_project_profile
from stages.billing_generation import generate_mock_billing
from stages.cost_analysis import generate_cost_report
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = "data"


def reset_project():
    for f in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, f))


def enter_project_description():
    reset_project()
    print("Enter project description (blank line to finish):")

    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    with open(os.path.join(DATA_DIR, "project_description.txt"), "w") as f:
        f.write("\n".join(lines))


def run_pipeline():
    extract_project_profile()
    generate_mock_billing()
    generate_cost_report()
    print("✅ Pipeline completed")


def view_recommendations():
    with open(os.path.join(DATA_DIR, "cost_optimization_report.json")) as f:
        report = json.load(f)

    for i, r in enumerate(report["recommendations"], 1):
        print(f"{i}. {r['title']} → Save ₹{r['potential_savings']}")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    while True:
        print("""
1. Enter new project
2. Run complete analysis
3. View recommendations
0. Exit
""")
        choice = input("Choice: ").strip()

        if choice == "1":
            enter_project_description()
        elif choice == "2":
            run_pipeline()
        elif choice == "3":
            view_recommendations()
        elif choice == "0":
            sys.exit()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

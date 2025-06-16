import yaml

# Threshold: how many criteria need to be True for a fact to be common knowledge
CK_THRESHOLD = 4

def is_common_knowledge(criteria: dict) -> bool:
    return sum(criteria.values()) >= CK_THRESHOLD

def main():
    with open("facts.yaml", "r", encoding="utf-8") as file:
        facts = yaml.safe_load(file)

    for entry in facts:
        fact = entry["fact"]
        criteria = entry["criteria"]
        score = sum(criteria.values())
        result = "✅ CK" if is_common_knowledge(criteria) else "❌ not CK"
        
        print(f"\nФакт: {fact}")
        print(f"Выполнено критериев: {score}/6 — {result}")
        for k, v in criteria.items():
            status = "✓" if v else "✗"
            print(f"  {k.replace('_', ' ')}: {status}")

if __name__ == "__main__":
    main()

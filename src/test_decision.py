
from agent.decision_engine import decide_action

test_cases = [
    {
        "labels": ["Business"],
        "priority": "High"
    },
    {
        "labels": [],
        "priority": "Low"
    },
    {
        "labels": ["Reminders", "Business"],
        "priority": "Medium"
    }
]

for case in test_cases:
    result = decide_action(
        case["labels"],
        case["priority"]
    )

    print("\nPredicted categories:", case["labels"])
    print("Priority:", case["priority"])
    print("Agent action:", result["action"])
    print("Reason:", result["reason"])

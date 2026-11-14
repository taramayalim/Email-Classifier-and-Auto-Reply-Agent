
from reply_generator.reply_generator import generate_reply


test_cases = [
    ["Business"],
    ["Reminders", "Business"],
    ["Customer Support"],
    []
]

for labels in test_cases:
    result = generate_reply(labels)

    print("\nPredicted categories:", labels)
    print("Selected template category:", result["category"])
    print("Suggested reply:", result["reply"])


from agent.priority_detector import detect_priority


test_emails = [
    {
        "subject": "URGENT: Account Locked",
        "body": "Please resolve this issue immediately."
    },
    {
        "subject": "Reminder: Project Meeting",
        "body": "Please attend the meeting tomorrow."
    },
    {
        "subject": "Weekly Newsletter",
        "body": "Here are this week's updates."
    }
]

for email in test_emails:
    result = detect_priority(email["subject"], email["body"])

    print("\nSubject:", email["subject"])
    print("Priority:", result["priority"])
    print("Reason:", result["reason"])

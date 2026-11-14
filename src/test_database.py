
from memory.database import (
    initialize_database,
    save_email,
    save_feedback,
    get_email_history,
    get_feedback_history
)

initialize_database()
print("Database initialized successfully.")

email_id = save_email(
    subject="Reminder: Project Meeting",
    body="Please attend tomorrow's project meeting.",
    categories=["Reminders", "Business"],
    priority="Medium",
    action="draft_reply",
    reply="Thank you for the reminder."
)

print("Saved email ID:", email_id)

save_feedback(
    email_id=email_id,
    feedback_type="approved",
    comments="The suggested reply is appropriate."
)

print("Feedback saved successfully.")

print("\n========== EMAIL HISTORY ==========")

for email in get_email_history():
    print(email)

print("\n========== FEEDBACK HISTORY ==========")

for feedback in get_feedback_history():
    print(feedback)

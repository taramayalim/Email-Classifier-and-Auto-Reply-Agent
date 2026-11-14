
from agent.email_agent import EmailAgent


# Create the email agent
agent = EmailAgent()

# Example email
subject = "Reminder: Project Meeting Tomorrow"

body = """
Dear Team,

This is a reminder that our project meeting
will take place tomorrow at 10 AM.
Please bring your project progress reports.

Regards,
Project Manager
"""

# Process the email
result = agent.process_email(subject, body)

# Display agent results
print("\n========== EMAIL AGENT RESULTS ==========")

print("Email ID:", result["email_id"])
print("Subject:", result["subject"])
print("Predicted categories:", result["categories"])
print("Priority:", result["priority"])
print("Priority reason:", result["priority_reason"])
print("Agent action:", result["action"])
print("Action reason:", result["action_reason"])

print("\n========== SUGGESTED REPLY ==========")

if result["suggested_reply"]:
    print(result["suggested_reply"])
else:
    print("No reply drafted. Human review is required.")

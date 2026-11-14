
import re


def detect_priority(subject, body):
    """
    Detect email priority using keyword-based rules.
    Returns priority level and the reason.
    """

    email_text = f"{subject} {body}".lower()
    email_text = re.sub(r"\s+", " ", email_text)

    high_keywords = [
        "urgent",
        "asap",
        "immediately",
        "emergency",
        "deadline today",
        "action required",
        "payment overdue",
        "account locked"
    ]

    medium_keywords = [
        "reminder",
        "follow up",
        "follow-up",
        "please respond",
        "deadline",
        "important",
        "due soon"
    ]

    # Check for high-priority keywords
    matched_high = [
        word for word in high_keywords if word in email_text
    ]

    if matched_high:
        return {
            "priority": "High",
            "reason": "Urgent keywords detected: " + ", ".join(matched_high)
        }

    # Check for medium-priority keywords
    matched_medium = [
        word for word in medium_keywords if word in email_text
    ]

    if matched_medium:
        return {
            "priority": "Medium",
            "reason": "Reminder or deadline keywords detected: "
                      + ", ".join(matched_medium)
        }

    # Default priority
    return {
        "priority": "Low",
        "reason": "No high- or medium-priority keywords detected."
    }

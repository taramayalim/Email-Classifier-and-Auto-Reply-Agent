
def decide_action(predicted_labels, priority):
    """
    Decide what action the email agent should take.
    """

    # High-priority emails require human attention
    if priority == "High":
        return {
            "action": "flag_for_review",
            "reason": "High-priority email requires human attention."
        }

    # Emails without a predicted category need manual review
    if not predicted_labels:
        return {
            "action": "manual_review",
            "reason": "The classifier could not identify a category."
        }

    # Other emails can receive a suggested reply
    return {
        "action": "draft_reply",
        "reason": "Email category identified and priority is manageable."
    }

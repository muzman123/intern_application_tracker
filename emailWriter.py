
def saveRejectionEmail(from_address, subject, body, filename="rejection_emails.txt"):
    """Saves the rejection email details to a text file."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"From: {from_address}\n")
        file.write(f"Subject: {subject}\n")
        file.write(f"Body: {body}\n")
        file.write("=" * 50 + "\n\n")

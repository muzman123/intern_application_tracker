import imaplib
import email
from email.header import decode_header
from emailWriter import saveRejectionEmail
from dynamoTable import saveToDynamoTable

subject_keywords = ["status", "application", "co-op", "coop", "internship", "position", "interest"]
        
rejection_keywords = [
    "decided",
    "unfortunately",
    "regret to inform",
    "careful consideration",
    "not be moving forward",
    "not be proceeding",
    "not selected",
    "proceed with another candidate",
    "proceeding with another candidate",
    "difficult decision",
    "at this time",
    "has been filled",
    "not to move forward",
    "regretfully",
    "you success",
    "future openings"
]
#blacklist replies from certain emails
blacklist = ["LinkedIn Job Alerts <jobalerts-noreply@linkedin.com>", "LinkedIn <jobs-noreply@linkedin.com>", "Arpita Rawal <careerbrew@substack.com>"
            , "LinkedIn <jobs-listings@linkedin.com>", "Team Unstop <noreply@unstop.news>", "APEX Internships <internships@apexearlycareers.com>"]

def countEmails(emailAddress, appPassword, date="1-Nov-2024"):
    # Set your email and app-specific password
    username = emailAddress
    #"oisi avtu cazp qxvi"
    password = appPassword
    # Connect to the IMAP server (Gmail example)
    imap_server = "imap.gmail.com"
    dateString = date

    # Create an IMAP client session
    with imaplib.IMAP4_SSL(imap_server) as mail:
        # Log in to your email account
        mail.login(username, password)

        # Select the mailbox you want to use; "INBOX" is the primary inbox
        mail.select("inbox")

        # Search for all emails in the inbox
        status, messages = mail.search(None, 'SINCE', dateString)

        # Get the list of email IDs
        email_ids = messages[0].split()

        rejectionCount = 0
        # Loop through email IDs
        print("Number of emails found in inbox: " + str(len(email_ids)))
        for email_id in email_ids:
            # Fetch the email by ID
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                
                if isinstance(response_part, tuple):
                    # Parse the bytes email into a message object
                    msg = email.message_from_bytes(response_part[1])

                    # Get the sender's email address
                    from_ = msg.get("From")
                    
                    if from_ in blacklist:
                        continue

                    # Check if "noreply" is in the sender's address
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    subject_lower = subject.lower()
                    matching_keywords = sum(1 for keyword in subject_keywords if keyword.lower() in subject_lower)
                    #print(matching_keywords)
                    if matching_keywords >= 1:
                        print(f"From: {from_}")
                        print(f"Subject: {subject}")
                        print("="*50)
                        if msg.is_multipart():
                    # If the email has multiple parts (e.g., plain text and HTML)
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))

                                # Check if it's plain text or HTML
                                if "attachment" not in content_disposition:
                                    if content_type == "text/plain":  # Plain text part
                                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        else:
                            # If the email is not multipart (i.e., plain text or HTML only)
                            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                        for i in rejection_keywords:
                            if i in body.lower():
                                rejectionCount += 1
                                #print("bruv")
                                saveRejectionEmail(from_, subject, body)
                                saveToDynamoTable(from_, subject, body)
                                print(i)
                                print("="*50)
                                break
                                
    return rejectionCount

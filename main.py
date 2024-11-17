import imaplib
import email
from email.header import decode_header
from emailWriter import saveRejectionEmail
from rejectionCounter import countEmails

if __name__ == "__main__":
    rejection_count = countEmails("[email]", "[password]")
    print(f"Total Rejection Emails: {rejection_count}")
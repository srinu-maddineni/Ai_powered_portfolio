import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
THANK_YOU_SUBJECT = "Thanks for Visiting! 🎉"

THANK_YOU_BODY = """\
<!DOCTYPE html>
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
    <div style="max-width: 500px; margin: auto; background: #ffffff;
                border-radius: 10px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
      <h2 style="color: #4A90E2;">Thanks for Visiting! 🎉</h2>
      <p style="color: #555; font-size: 16px;">
        We really appreciate you stopping by. We hope you had a great experience!
      </p>
      <p style="color: #555; font-size: 16px;">
        Feel free to reach out anytime — we're always happy to help.
      </p>
      <br>
      <p style="color: #999; font-size: 13px;">— Srinu Maddineni</p>
    </div>
  </body>
</html>
"""

def send_email(recipient_email: str) -> dict:

    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        return {
            "success": False,
            "error": "Email credentials are not configured. Check your .env file.",
        }

    try:
        # Build the email message using EmailMessage
        msg = EmailMessage()
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient_email
        msg["Subject"] = THANK_YOU_SUBJECT
        msg.set_content(THANK_YOU_BODY, subtype="html")

        # Connect to Gmail SMTP and send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()          # Upgrade connection to TLS
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)   # send_message works natively with EmailMessage

        return {"success": True, "message": f"Email sent successfully to {recipient_email}"}

    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "error": (
                "Authentication failed. Make sure you are using a Gmail App Password, "
                "not your regular Gmail password."
            ),
        }
    except smtplib.SMTPRecipientsRefused:
        return {
            "success": False,
            "error": f"Recipient address '{recipient_email}' was refused by the server.",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

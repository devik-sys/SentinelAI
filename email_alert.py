import smtplib
from email.message import EmailMessage

# ----------------------------
# YOUR GMAIL DETAILS
# ----------------------------

EMAIL_ADDRESS = "YOUR_EMAIL"
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"

# ----------------------------
# CREATE EMAIL
# ----------------------------

msg = EmailMessage()

msg["Subject"] = "🚨 SentinelAI Alert"

msg["From"] = EMAIL_ADDRESS

msg["To"] = EMAIL_ADDRESS

msg.set_content(
    """
Intruder detected by SentinelAI.

Motion and face detected.

Please check your surveillance recordings.
"""
)

# ----------------------------
# SEND EMAIL
# ----------------------------

try:

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        smtp.send_message(msg)

    print("✅ Email sent successfully!")

except Exception as e:

    print("❌ Error:", e)
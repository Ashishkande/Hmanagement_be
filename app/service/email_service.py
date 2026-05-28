import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def send_email(receiver_email, otp):

    print("EMAIL FUNCTION STARTED")

    subject = "OTP Verification"

    body = f"Your OTP is {otp}"

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = receiver_email

    try:

        server = smtplib.SMTP_SSL(
            EMAIL_HOST,
            EMAIL_PORT
        )

        print("SMTP CONNECTED")

        server.login(
            EMAIL_HOST_USER,
            EMAIL_HOST_PASSWORD
        )

        print("LOGIN SUCCESS")

        server.sendmail(
            EMAIL_FROM,
            receiver_email,
            msg.as_string()
        )

        print("MAIL SENT SUCCESSFULLY")

        server.quit()

    except Exception as e:

        print("EMAIL ERROR")
        print(str(e))

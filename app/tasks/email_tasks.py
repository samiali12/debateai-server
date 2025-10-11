import os
import asyncio
import smtplib
from dotenv import load_dotenv
from celery import shared_task
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SMTP_EMAIL")
SENDER_PASSWORD = os.getenv("SMTP_PASSWORD")


@shared_task
def send_reset_password_link(to_email: str, reset_token: str):
    reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={reset_token}"
    subject = "Password Reset Request"
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>Hi,</p>
        <p>Click the button below to reset your password:</p>
        <p>
          <a href="{reset_link}"
             style="background-color:#007bff;color:white;padding:10px 20px;
                    text-decoration:none;border-radius:5px;display:inline-block;">
             Reset Password
          </a>
          <br>
          or
          <br>
          {reset_link}
        </p>
        <p>This link will expire in <strong>15 minutes</strong>.</p>
        <p>If you didn’t request this, you can ignore this email.</p>
      </body>
    </html>
    """


    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

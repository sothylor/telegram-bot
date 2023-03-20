import smtplib
import random
from myapi import TwilioCredentials as twilio
from twilio.rest import Client

client = Client(twilio.account_sid, twilio.auth_token)

def email_verify(receiver_email):
    verification_code = str(random.randint(100000, 999999))

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your-password"
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    subject = "Email Verification Code"
    body = f"Your verification code is <b style='font-size: 15px;'>{verification_code}</b>"
    message = f"Subject: {subject}\nContent-type: text/html\n\n{body}"

    server.sendmail(sender_email, receiver_email, message)
    server.quit()
    return verification_code

def send_verify(phone_number):

    try:
        verification = client.verify.v2.services(twilio.verify_sid) \
        .verifications \
        .create(to=phone_number, channel="sms")
        print(verification.status)
        return verification.status
    except: 
        return

def otp_acceptance(verified_number, otp_code):
    try:
        verification_check = client.verify.v2.services(twilio.verify_sid) \
            .verification_checks \
            .create(to=verified_number, code=otp_code)
        return verification_check.status
    except:
        return

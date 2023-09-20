import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sending_mail(email: str, password: str, random_number: int):
    
    smtplib_object = smtplib.SMTP('smtp.gmail.com', 587)

    print(smtplib_object.starttls())
    print(smtplib_object.login(email, password))

    from_address = email
    to_address = email
    subject = "[AUTHORIZATION - MIDDLEWARE] Please verify your device"
    
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email  # Replace with the recipient's email address
    msg['Subject'] = subject
    message = "Hey {0}!, Verification code: {1}".format(email, random_number)
    msg.attach(MIMEText(message, 'plain'))

    print(smtplib_object.sendmail(from_address, to_address, msg.as_string()))

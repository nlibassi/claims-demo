from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(insured):
    token = insured.get_reset_password_token()
    send_email('[AIR Claims] Reset Your Password',
        sender=app.config['ADMINS'][0],
        recipients=[insured.email],
        text_body=render_template('email/reset_password.txt',
            insured=insured, token=token),
        html_body=render_template('email/reset_password.html',
            insured=insured, token=token))
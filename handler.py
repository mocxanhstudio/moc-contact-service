import os
import sys
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from datetime import datetime

class User:
    def __init__(self, name, phone, content):
        self.name = name.title()
        self.phone = phone
        self.content = content.title()


def generate_email(type, user):    
    data = 'NULL'
    if type == 'contact':
        with open("./templates/contact.html", "r") as f:
            data = f.read().rstrip()
        for r in (
            ("REPLACE_USER_NAME",  user.name), 
            ("REPLACE_USER_PHONE", str(user.phone)), 
            ("REPLACE_USER_CONTENT", user.content)):
            data = data.replace(*r)
    return data


def send_email(content):      
    m = MIMEMultipart('alternative')
    
    # -- hardcode title subject email
    m['Subject'] = f"Chân Mày - Cần Tư Vấn - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    m['From'] = email.utils.formataddr((os.environ['SENDER_NAME'], os.environ['SENDER_EMAIL']))
    m['To'] = os.environ['RECIPIENT_NAME']
    m.attach(MIMEText(content, 'html'))

    try:
        s = smtplib.SMTP(os.environ['SES_HOST'], os.environ['SES_PORT'])
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(os.environ['SES_USERNAME'], os.environ['SES_PASSWORD'])
        s.sendmail(os.environ['SENDER_EMAIL'], os.environ['RECIPIENT_NAME'], m.as_string())
        s.close()
    except Exception as e:
        print (f"[ERROR] send_email: {e}")
        sys.exit(1)
    else:
        print (f"[INFO] send_email: sent")


def _9NPAAbfB(event, context):
    print("[DEBUG] event: ", event)
    print("[DEBUG] context: ", context)
    body = json.loads(event['body']) 
    send_email(
        generate_email(
            'contact', User(
                body['name'],
                body['phone'],
                body['content']
            )
        )
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST"
        },
        "body": json.dumps({
            "trello": "9NPAAbfB",
            "status": "tracked"
        })
    }

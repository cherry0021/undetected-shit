from smtplib import SMTP_SSL
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

class Smtp:
    
    is_logged_in = False
    
    def __init__(self, EMAIL, PASSWORD, SERVER = '', PORT = 465):
        EMAIL = EMAIL.strip()
        if not EMAIL or not PASSWORD:
            print('Unable to connect Smtp. Email or Password is None.')
            exit()
        
        if SERVER == '':    
            if EMAIL.endswith('@gmail.com'):
                SERVER = 'smtp.gmail.com'
                PORT = 465
            elif EMAIL.endswith('@outlook.com'):
                SERVER = 'smtp.office365.com'
                PORT = 587
            elif EMAIL.endswith('@zohomail.eu'):
                SERVER = 'smtp.zoho.com'
                PORT = 587
            elif EMAIL.endswith('@aol.com'):
                SERVER = 'smtp.aol.com'
                PORT = 465
            
        try:
            self.mail = SMTP_SSL(SERVER, port=PORT)
            # self.mail.set_debuglevel(1)  # Show SMTP server interactions
            self.mail.login(EMAIL, PASSWORD)
            self.is_logged_in = True
            # print('SMTP connected.')
        except Exception as e:
            print(f'Email: {EMAIL}, Exception: {e}')
            # exit()
    
    def logout(self):
        self.mail.quit()
        print('Successfully logged out from SMTP server')
        
    def send_email(self, mailtext, headers, mailhtml=None, files=[], origin=None):
        msg = MIMEMultipart('mixed')
        body = MIMEMultipart('alternative')
        
        # headers['From'] = sender
        # headers['To'] = recipient
        for k,v in headers.items():
            if isinstance(v, list):
                v = ', '.join(v)
            msg.add_header(k, v)
        
        if origin:
            sub = origin["subject"].replace("Re: ", "").replace("RE: ", "") if origin["subject"] else ""
            msg["Subject"] = "RE: " + sub
            msg['In-Reply-To'] = origin["Message-ID"]
            msg['References'] = origin["Message-ID"] + ' ' + origin["References"].strip()
            msg['Thread-Topic'] = origin["Thread-Topic"]
            msg['Thread-Index'] = origin["Thread-Index"]

        body.attach(MIMEText(mailtext, 'plain'))
        if mailhtml:
            body.attach(MIMEText(mailhtml, 'html'))
        
        for f in files:
            with open(f, "rb") as file:
                part = MIMEApplication(
                    file.read(),
                    Name=basename(f)
                )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            body.attach(part)
        
        msg.attach(body)
        self.mail.sendmail(msg['From'], msg['To'], msg.as_string())
        

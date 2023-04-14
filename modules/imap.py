from sys import exit
import email
import imaplib

class Imap:
    
    is_logged_in = False
    
    def __init__(self, EMAIL, PASSWORD, SERVER = '', PORT = 993):
        EMAIL = EMAIL.strip()
        if not EMAIL or not PASSWORD:
            print('Unable to connect Imap. Email or Password is None.')
            exit()
            
        if SERVER == '':    
            if EMAIL.endswith('@gmail.com'):
                SERVER = 'imap.gmail.com'
            elif EMAIL.endswith('@outlook.com'):
                SERVER = 'outlook.office365.com'
            elif EMAIL.endswith('@zohomail.eu'):
                SERVER = 'imap.zoho.eu'
            elif EMAIL.endswith('@aol.com'):
                SERVER = 'imap.aol.com'
            
        try:
            self.mail = imaplib.IMAP4_SSL(SERVER)
            self.mail.login(EMAIL, PASSWORD)
            self.is_logged_in = True
            # print('Imap connected.')
        except Exception as e:
            print(f'Email: {EMAIL}, Exception: {e}')
            # exit()

    def logout(self):
        self.mail.close()
        self.mail.logout() 
        print('Successfully logged out from IMAP server')

    def get_email_ids(self, folder='inbox', from_email='', to_email=''):
        folder = '"[Gmail]/Sent Mail"' if folder == 'sent' and to_email.endswith('@gmail.com') else folder
        self.mail.select(folder)
        
        if from_email:
            query = f'(FROM "{from_email}")'
        elif to_email:
            query = f'(TO "{to_email}")'
        else:
            query = 'ALL'
            
        status, data = self.mail.search(None, query)  # Search criteria
        
        mail_ids = data[0].split()
        # print('Total email: ', len(mail_ids))
        return status, mail_ids
        
    def fetch_message(self, id, console_print=False):
        status, data = self.mail.fetch(id, '(RFC822)')
        message, msg_body = None, []

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes((response_part[1]))
                
                if console_print:
                    # print(message)
                    print("Message-ID:", message['Message-ID'])
                    print("Date:", message['Date'])
                    print("From:", message['From'])
                    print("To:", message['To'])
                    print("Subject:", message['Subject'])
                    print("In-Reply-To:", message['In-Reply-To'])
                    print("References:", message['References'])
                    print("Body:")
                for i, part in enumerate(message.walk()):
                    # print('content type:', part.get_content_type())
                    if part.get_content_type() == 'text/plain':
                        text = part.get_payload(decode=True).decode('UTF-8').strip()
                        if text:
                            msg_body.append(text)
                            if console_print:
                                print(f'--------Part[{i}]--------')
                                print(text)
        
        return status, message, msg_body

                

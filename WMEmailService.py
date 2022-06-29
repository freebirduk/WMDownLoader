import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from IWMEmailService import IWMEmailService


class WMEmailService(IWMEmailService):
    host = None
    port = None
    username = None
    password = None
    from_address = None
    from_name = None
    to_address = None
    to_name = None

    def __init__(self, host, port, username, password, from_address, from_name, to_address, to_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_address = from_address
        self.from_name = from_name
        self.to_address = to_address
        self.to_name = to_name

    def send_email(self, message):
        # Create message
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = Header("WMDownloader alert", 'utf-8')
        msg['From'] = formataddr((str(Header(self.from_name, 'utf-8')), self.from_address))
        msg['To'] = self.to_address

        # Send message
        try:
            with smtplib.SMTP_SSL(self.host, self.port) as server:
                server.login(self.username, self.password)

                server.sendmail(self.from_address, [self.to_address], msg.as_string())
                server.quit()

            return True

        except (smtplib.SMTPException, TimeoutError):
            logging.warning(f'Failed to send e-mail message "{message}"', exc_info=True)

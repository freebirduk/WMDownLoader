import logging
import smtplib
import sys
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from IWMErrorService import IWMErrorService


# Handles WMDownloader errors of whatever severity. Options to perform logging,
# send e-mail alerts and terminate the program.
class WMErrorService(IWMErrorService):
    host = None
    port = None
    username = None
    password = None
    from_address = None
    from_name = None
    to_address = None
    to_name = None
    stored_email_messages: str = None

    def __init__(self, host, port, username, password, from_address, from_name, to_address, to_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_address = from_address
        self.from_name = from_name
        self.to_address = to_address
        self.to_name = to_name

    # Called at the end of processing to send an e-mail with batched together messages, if any.
    def finalise_error_handling(self):

        if self.stored_email_messages is not None:
            self._send_email(self.stored_email_messages)

    # Handles error logging, alert e-mail sending and program termination as necessary.
    # If batch_message = true and send_email = True then an e-mail will not be generated.
    # Rather the message will be stored and an email sent only when finalise_error_handling is called.
    def handle_error(self,
                     message: str,
                     severity: str = 'Warning',
                     send_email: bool = False,
                     batch_message: bool = False,
                     terminate: bool = False,
                     exc_info=None):

        match severity:
            case "Info":
                logging.info(message)
            case "Warning":
                logging.warning(message)
            case "Error":
                logging.error(message)
            case _:
                if exc_info is None:
                    logging.critical(message)
                else:
                    logging.critical(message, exc_info=exc_info)

        if send_email:
            if batch_message:
                if self.stored_email_messages is None:
                    self.stored_email_messages = message
                else:
                    self.stored_email_messages = (self.stored_email_messages + "\n" + message)
            else:
                self._send_email(message)

        if terminate:
            self.finalise_error_handling()
            sys.exit()

    def _send_email(self, message):
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

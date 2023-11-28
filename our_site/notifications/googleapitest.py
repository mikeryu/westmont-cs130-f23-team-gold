import base64
from email.mime.text import MIMEText
from requests import HTTPError

from .__init__ import service


def send_notification(recipient: str, subject: str, body: str) -> bool:
    """
    send_notification sends an email with a message to someone.

    :param recipient: email address to send the email to.
    :param subject: subject of the email you want to send.
    :param body: body of the email you want to send.
    :return: True if the email was successfully send, False if the email did not send.
    """
    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        service.users().messages().send(userId="me", body=create_message).execute()
        return True
    except HTTPError as error:
        print(F'An error occurred: {error}')
        return False

import smtplib
import ssl

from email.mime.nonmultipart import MIMENonMultipart

from secret_config import mail_server, mail_user, mail_password


def send_mail(recipient, name, message):
    """
    Send a mail to a user with a specific message and the server options from the secret config

    :param recipient: the mail address of the recipient
    :param name: the name of the recipient
    :param message: the html message string
    """
    print(f'\tSending mail to {name} <{recipient}>')

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMENonMultipart("text", "html")
    msg['Subject'] = "Dualis update?!"
    msg['From'] = mail_user
    msg['To'] = recipient

    # Create the body of the message (a plain-text and an HTML version).
    html = '<html><head></head><body>' \
           f'<h3>Hello {name}</h3>' \
           f'<p>There has been recent activity regarding the grades of your course at dualis.<br>Probably something ' \
           f'changed for you as well, go <a href="https://dualis.gahr.dev">check it out!</a></p>{message}' \
           '</body></html>'
    msg.set_payload(html)

    _DEFAULT_CIPHERS = (
        'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
        'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
        '!eNULL:!MD5')

    smtp_server = smtplib.SMTP(mail_server, port=587)
    # only TLSv1 or higher
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3

    context.set_ciphers(_DEFAULT_CIPHERS)
    smtp_server.starttls(context=context)
    smtp_server.login(mail_user, mail_password)

    smtp_server.sendmail(mail_user, recipient, msg.as_string())
    smtp_server.quit()

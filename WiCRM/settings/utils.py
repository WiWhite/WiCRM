import uuid

from django.core.mail.message import EmailMessage
from django.core.mail import get_connection


def generate_ref_code():
    return str(uuid.uuid4()).replace('-', '')[:30]


def create_connection(email_service):

    if email_service.email_use_ssl:
        return get_connection(
                    host=email_service.email_host,
                    port=email_service.email_port,
                    username=email_service.email_login,
                    password=email_service.email_password,
                    use_ssl=email_service.email_use_ssl,
                )

    elif email_service.email_use_tls:
        return get_connection(
            host=email_service.email_host,
            port=email_service.email_port,
            username=email_service.email_login,
            password=email_service.email_password,
            use_ssl=email_service.email_use_tls,
        )


def send_invite(from_, to, connection, msg):
    subj = 'Invite for you!'
    mail = EmailMessage(
        subject=subj,
        body=msg,
        from_email=from_,
        to=to,
        connection=connection,
    )
    mail.send()

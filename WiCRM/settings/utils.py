import uuid
from smtplib import SMTP, SMTP_SSL
import ssl

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
            use_tls=email_service.email_use_tls,
        )

    else:
        return get_connection(
            host=email_service.email_host,
            port=email_service.email_port,
            username=email_service.email_login,
            password=email_service.email_password,
        )


def send_invite(from_, to, connection, body):
    subj = 'Invite for you!'
    mail = EmailMessage(
        subject=subj,
        body=body,
        from_email=from_,
        to=to,
        connection=connection,
    )
    mail.send()


def check_connection(cleaned_data):

    if cleaned_data['email_use_ssl']:
        context = ssl.create_default_context()
        with SMTP_SSL(
                cleaned_data['email_host'],
                cleaned_data['email_port'],
                context=context,
        ) as server:
            server.login(
                cleaned_data['email_login'],
                cleaned_data['email_password'],
            )

    elif cleaned_data['email_use_tls']:
        with SMTP(
                cleaned_data['email_host'],
                cleaned_data['email_port'],
        ) as server:
            server.starttls()
            server.login(
                cleaned_data['email_login'],
                cleaned_data['email_password'],
            )

    else:
        with SMTP(
                cleaned_data['email_host'],
                cleaned_data['email_port'],
        ) as server:
            server.login(
                cleaned_data['email_login'],
                cleaned_data['email_password'],
            )

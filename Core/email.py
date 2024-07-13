import pickle
import os.path
from jinja2 import Template
from flask import current_app, url_for
from flask_mail import Message
from threading import Thread

from FoodyCore.extensions import MailServer
from FoodyConfig import GetConfig
from celery import shared_task

BASE_DIR = GetConfig()
templates = {
    "activeAccount": BASE_DIR / "FoodyCore" / "MailTemplate" / "ActivateAccount.html",
    "ResetPassword": BASE_DIR / "FoodyCore" / "MailTemplate" / "ResetPassword.html",
}


def ReadTemplateContent(path):
    """This function take a template name and return content of that template"""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return " "


def async_send_email_thread(app, msg):
    """
    Sending email asynchronously using threading
    """
    with app.app_context():
        MailServer.send(msg)


@shared_task(ignore_result=True)
def async_send_email_celery(msg):
    """
    Sending email asynchronously using celery
    """
    msg = pickle.loads(msg)
    MailServer.send(msg)


def send_email(recipients, subject, sender, text_body="", html_body="",
               attachments=None, async_thread=False, async_celery=False):
    """
        this function send mail via flask-mail

        recipients:list =  (user's email address)
        subject:sre = subject of email to send
        sender:str = sender email address
        text_body:str = email body
        html_body:str= if you want to send html email to can pass raw html
        attachments:byte = attachment files to be attached in email

        sending methods:
            async_thread:bool : send email asynchronously using threading
            async_celery:bool : send email asynchronously using celery
        without this parameter this function send email in sync mode
    """

    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    if async_thread:
        current_app.logger.info(f"\n[Thread Async] Mail Address: {recipients}")
        Thread(target=async_send_email_thread, args=(
            current_app._get_current_object(), msg)).start()

    elif async_celery:
        current_app.logger.info(f"\n[Celery Async] Mail Address: {recipients}")
        async_send_email_celery.delay(pickle.dumps(msg))

    else:
        current_app.logger.info(f"\n[Sync Normal] Mail Address: {recipients}")
        MailServer.send(msg)


def sendActivAccounteMail(context: dict, recipients: list, **kwargs):
    """
    This Function send Activate Account mail

        context: dict
        values:
            token: slug url for activate user Account
    """

    template = Template(
        ReadTemplateContent(templates["activeAccount"])
    ).render(**context, **{"ActivateLink": url_for("auth.active_account", token=context['token'], _external=True)})

    send_email(
        subject="Active Account",
        sender=(('فعال سازی حساب کاربری'), current_app.config.get(
            "MAIL_DEFAULT_SENDER", ":)")),
        recipients=recipients,
        html_body=template,
        **kwargs
    )

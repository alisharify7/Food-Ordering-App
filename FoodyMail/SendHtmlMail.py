from flask_mail import Message
from FoodyMail.MailParser import ParseMail
from FoodyCore.extension import MailServer


def SerilizeOrderObject(orderDB) -> dict:
    """
        Convert Order Object to A dict for sending digital factor to users
    """
    temp = {}
    temp["factor_number"] = f"#FD-DG-{orderDB.id}"
    temp['factor_date'] = str(orderDB.GetJalaliDate())
    temp["name"] = orderDB.GetFoodName()
    temp["datetime"] = str(orderDB.GetJalaliDate())
    return temp


def Send_Factor_Mail(recipients: list, order_db) -> bool:
    '''
        send Factor Mail For users
    '''
    if not isinstance(recipients, list):
        recipients = [recipients]

    message = Message(
        recipients=recipients,
        charset="utf-8",
        sender=("اتوماسیون تغذی هوشمند", "temp@temp.ir"),
        subject="فاکتور اتوماسیون تغذیه"
    )
    context = SerilizeOrderObject(order_db)
    mailHtml = ParseMail(path="MailHtml/Factor.html", context=context)
    if not mailHtml:
        return False
    message.html = mailHtml
    result = MailServer.send(message)
    return True

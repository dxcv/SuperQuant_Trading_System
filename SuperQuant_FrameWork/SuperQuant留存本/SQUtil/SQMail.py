# coding=utf-8


from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def SQ_util_send_mail(msg, title, from_user, from_password, to_addr, smtp):
    """邮件发送

    Arguments:
        msg {[type]} -- [description]
        title {[type]} -- [description]
        from_user {[type]} -- [description]
        from_password {[type]} -- [description]
        to_addr {[type]} -- [description]
        smtp {[type]} -- [description]
    """

    msg = MIMEText(msg, 'plain', 'utf-8')
    msg['Subject'] = Header(title, 'utf-8').encode()

    server = smtplib.SMTP(smtp, 25)  # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_user, from_password)
    server.sendmail(from_user, [to_addr], msg.as_string())




# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
import smtplib
from email.mime.text import MIMEText, MIMENonMultipart

def send_mail(username, passwd, recv, title, content, mail_host, port):
    """
    发送邮件模块
    :param username: 账号
    :param passwd: 密码
    :param recv: 接收账号
    :param title: 标题
    :param content: 内容
    :param mail_host: 邮件服务器主机
    :param port: 邮件服务器端口
    :return:
    """
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = title
    msg['From'] = username
    msg['to'] = recv
    smtp = smtplib.SMTP(mail_host, port=port)
    smtp.login(username, passwd)
    smtp.sendmail(username, recv, msg.as_string())
    smtp.quit()
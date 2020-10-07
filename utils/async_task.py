# coding=utf-8
import threading
from .save_data import *
from .parse_xml import *
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

SENDER = 'junwen-pan@qq.com'
SENDER_NAME = 'Disqus2Leancloud'
SENDER_PASS = 'ccbxajztgjrjggch'


def send_mail(receiver, subject, content):
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr([SENDER_NAME, SENDER])
        msg['To'] = formataddr([receiver, receiver])
        msg['Subject'] = subject
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(SENDER, SENDER_PASS)
        server.sendmail(SENDER, [receiver, ], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)


class ProcessThread(threading.Thread):
    def __init__(self, appid, appkey, email, file_path):
        threading.Thread.__init__(self)
        self.appid = appid
        self.appkey = appkey
        self.file_path = file_path
        self.email = email

    def run(self):
        init_account(self.appid, self.appkey)
        parsed = parse_all_posts(self.file_path)
        status = u'您好，您的评论数据迁移完成!\n\n XML文件解析结果为：' + parsed ['status'] + u'\n Leancloud存储结果为：'

        try:
            if parsed['data'] is None:
                status += u'Parser error.'
            else:
                save_all([build_object(p) for p in parsed['data']])
                status += u'Saved successfully.'
        except Exception as e:
            status += str(e)
        finally:
            send_mail(self.email, u'Disqus2Leancloud数据迁移结果通知', status)





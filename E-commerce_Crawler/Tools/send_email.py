from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def send_email(infofile):
    #创建一个带附件的实例
    msg = MIMEMultipart()
    #构造附件1
    att1 = MIMEText(open(infofile, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="result_store.csv"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)
    to_list=['hengwei@starmerx.com','chengli@starmerx.com','zhaolei@starmerx.com']
    msg['to'] = ';'.join(to_list)
    msg['from'] = 'user@starmerx.com'
    msg['subject'] = 'bestbuy店铺信息'
    #发送邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.exmail.qq.com')
        server.login('user@starmerx.com','pwd')#XXX为用户名，XXXXX为密码
        server.sendmail(msg['from'], to_list,msg.as_string())
        print ('发送成功',infofile)
    except Exception as e:
        print ('发送失败',e)
        #server.quit()
        send_email(infofile)
    finally:
        server.quit()

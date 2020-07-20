# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:16:48 2020

@author: j-3
"""
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import utils as Utils
import socket
import ssl
import urllib.request 
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def sendmail(to,subject,content):
    msg = MIMEText(content)
    lable_pwd="89812869"
    msg['from'] = 'site-check@gsgoldprice.com'
    msg['to'] = to
    msg['subject'] = subject
    msg['date'] = Utils.formatdate(localtime=1)
    msg['message-id'] = Utils.make_msgid()

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect("smtp.gsgoldprice.com:25")
        try:
            smtpObj.login("site-check@gsgoldprice.com",lable_pwd)
            me = "site-check@gsgoldprice.com"
            smtpObj.sendmail(me,to,msg.as_string())
            print("Congratulations !Your mail have been sended Success !")
        except smtplib.SMTPException:
            print("Login failed ,Please check the username/password.")
        finally:
            try:
                smtpObj.close()
            except smtplib.SMTPException:
                pass
    except smtplib.SMTPException as e:
        print("Error: unable to send email %s" %(e))

#Use socket
def check_server(f):
    try:
        fo = open(f,"r+")
  
        for line in fo:
            now = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
#            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s = ssl.wrap_socket(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
            line = line.rstrip('\n')
            print('正在检测%s的443端口是否正常 %s:......' % (line,now))
            
            try:
                s.connect((line,443))
                print("地址%s检测正常" % line)
            except socket.error as e:
                print("地址%s检测挂啦 %s" % (line,e))
#                sc = 'The web server %s is down '% line
#                cc = 'The web server %s is down at %s' % (line,now)
#                sendmail('jiangjijun@163.com',sc,cc)
            finally:
                s.close()
    except IOError as e:
        print("error: %s" % e)
    finally:
        try:
            fo.close()
        except IOError as e:
            print("error : %s" % e)


import https
#Use Request
def check_serverWithRequest():
    #获取地址
    https.getUrlData()
    print('Get URLs Done')
    
    UrlFile = r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/url.txt' 
    #表示忽略未经核实的SSL证书认证
    context = ssl._create_unverified_context()
    headers ={

"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",

}
    errorArr= []
    
    try:
        urlList = open(UrlFile,"r+")
        for url in urlList:
            now = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            url = url.rstrip('\n')
            # url 作为Request()方法的参数，构造并返回一个Request对象
            request = urllib.request.Request(url,headers=headers)
            print('正在检测%s是否正常 %s:......' % (url,now))
            
            try:
                # Request对象作为urlopen()方法的参数，发送给服务器并接收响应
                response = urllib.request.urlopen(request,context = context)
                code = response.code
                if code ==200:
                    print("地址%s检测正常" % url)
                else:
                    print("地址%s检测挂啦,code:%s" % (url,code))
                    errorArr.append("异常地址:\n%s \nerror:%s \n" % (url,code))
            except IOError as e:
                print("地址%s检测异常,code:%s" % (url,e))
                errorArr.append("异常地址:\n%s \nerror:%s \n" % (url,e))
#                print(e)
                    
    except IOError as e:
        print("error: %s" % e)
        
    finally:
        try:
            urlList.close()
            
            #把异常url写入TXT
            f_error = open(r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/errorUrl.txt', "w")
            for errorurl in errorArr:
                f_error.write(errorurl+'\n')
            f_error.close()
            
            #发邮件通知有错误URL
            errorList = open(r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/errorUrl.txt',"r+")
            sc = 'The error web server List'
            cc = errorList.read()
            sendmail('jiangjijun@163.com',sc,cc)
            errorList.close()
        except IOError as e:
            print("error : %s" % e)
            



if __name__=='__main__':
#    check_server('C:/Users/j-3/Desktop/web_check-master/web_check-master/url.txt')
#    check_serverWithRequest()
#     sendmail('site-check@gsgoldprice.com','test','test')
    
    #自动调度
    schedule = BackgroundScheduler()
    schedule.add_job(
                     func=check_serverWithRequest,
                     trigger='interval',
                     minutes=20, #minutes
                     next_run_time=datetime.datetime.now()#少这句会先等待20分钟，才执行方法
                     )
    schedule.start()
#    print('press ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#    try:
#        while True:
#            time.sleep(60)
#            print('working!')
#    except (KeyboardInterrupt,SystemExit):
#        schedule.shutdown()
#        print('Exit The Job!')
        
    
              
from urllib import parse

import urllib.request
import ssl
import re 
import requests

context = ssl._create_unverified_context()

url = 'https://gold-star.vigorddns.com/userlogin/phonelogin.aspx'

headers ={

"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",

}


# url 作为Request()方法的参数，构造并返回一个Request对象

request = urllib.request.Request(url,headers=headers)

# Request对象作为urlopen()方法的参数，发送给服务器并接收响应

response = urllib.request.urlopen(request,context = context)

html = response.read().decode('utf-8')
#print(html)


code = response.code

print(code)

opener=urllib.request.build_opener()
opener.add_handler=headers
htmlData = opener.open(url).read()

fhandle= open(r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/data.txt','wb')
fhandle.write(htmlData)
fhandle.close()


# 获取网页内容
#UrlFile = 'C:/Users/j-3/Desktop/web_check-master/web_check-master/data.txt' 
#urlList = open(UrlFile,"r+")

#r = requests.get('https://gold-star.vigorddns.com/userlogin/phonelogin.aspx')
#data = r.text
#
## 利用正则查找所有连接
#link_list =re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')" ,data)
#for url in link_list:
#    print(url)
    
#

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains


def getUrlData():
    print('start getting URL,please waiting......')
    #加载启动项--隐藏打开浏览器
    option = webdriver.FirefoxOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')

    #驱动器路径
    path = r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/geckodriver.exe'

    url="https://gold-star.vigorddns.com/userlogin/phonelogin.aspx"
    brower = webdriver.Firefox(executable_path=path,options=option)
    brower.get(url)
    time.sleep(3) #页面等待足够长时间，显示内容才完整，获取的URL才完整

    #获取鼠标焦点，模拟鼠标
    mouse = ActionChains(brower)

    #定位到要点击的地方
    clickLoginBtnElemet = brower.find_element_by_id("ImgLoginShow")
    #鼠标移动到登录按钮，并左键点击
    mouse.move_to_element(clickLoginBtnElemet)
    mouse.click().perform()
    #定位账号栏 输入账号
    mouse.reset_actions()#记得清除刚才的动作
    PutInNameLabElemet = brower.find_element_by_id("txtname")
    PutInNameLabElemet.send_keys("gs_wxh")
    #定位密码栏 输入密码
    PutInPwdLabElemet = brower.find_element_by_id("txtpwd")
    PutInPwdLabElemet.send_keys("123456")
    #定位到登录按钮 左键点击
    clickLoginBtnElemet = brower.find_element_by_id("dengImg")

    mouse.move_to_element(clickLoginBtnElemet)
    mouse.click().perform()

    time.sleep(10)
    pagesoures = brower.page_source  # 抓取网页源代码
    restr = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'  # 如果不带括号会输出全部,只要()内的数据如果政策抓取不到也许他前面有空格
    rex = re.compile(restr, re.IGNORECASE)
    mylist = rex.findall(pagesoures)
    brower.close()
    print(mylist) 
    urlData = open(r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/urlData.txt', 'w+')
    print(mylist, file=urlData)
    urlData.close()
    #分割字符串，装到数组里
    arr = []
    with open(r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/urlData.txt', "r") as fff:
        for lines in fff:
            ls = re.split(r' |\,|\[|\'|\"',lines)  #正则分割多个字符串 空格 ， 【 ' "
            for i in ls:
                if len(i)>5:
                    arr.append(i) 
    fff.close()
    
    #逐条写入
    endUrl = '?LoginName=gs_wxh&LoginPwd=123456'
    f1 = open(r'C:/Users/j-3/Desktop/pyDamo/web_check-master/web_check-master/url.txt', "w") #写入
    for j in arr:
        if j.endswith('png'):#图片格式忽略
            continue
        if j.endswith('version.asp'):
            f1.write(j+endUrl+'\n')
        elif j.endswith('version.aspx'):
            f1.write(j+endUrl+'\n')
        elif j.endswith('_ck.aspx'):
            f1.write(j+endUrl+'\n')
        else:
            f1.write(j+'\n')
    f1.close()         
               
    
   
if __name__=='__main__':
    getUrlData()
    








    
        
        
            
                   


   
       
    



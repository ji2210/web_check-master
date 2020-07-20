#coding:utf-8
import ctypes
import requests
import time
'''
检查网页是否可以正常访问
不能访问时会有滴声提示
'''
player=ctypes.windll.kernel32
f_url=open('./url.txt')#网站列表url.txt
while True:
    time.sleep(10)#设置监控频率 单位：秒
    for url in f_url:
        url=url.strip('\n')
        re=requests.get(url)
        if re.status_code!=200:
            print('erro!')
            player.Beep(1000,2000)#滴声提示，第一个参数是声音频率，第二个参数是时间
# -*- coding: utf-8 -*-
import scrapy
import pickle
import re
import time
import sys
import globalvar
# import globalvar as gl 
from scrapy_redis.spiders import RedisSpider
class DuanhaomaSpider(RedisSpider):
    name = "duanhaoma"
    redis_key = 'duanhaomaspider:start_urls'
    handle_httpstatus_list = [404, 302]#拦截404 302请求 
    

    def __init__(self):
        globalvar._init()
        self.anquan = 0
        globalvar.set_value("anquan", self.anquan)
        self.slinger = 0
        globalvar.set_value("slinger", self.slinger)
        # gl.globalvar.set_value('anquan', 90)
        # gl.globalvar.set_value('anquan', 90)
        # print(gl.globalvar.get_value("anquan"))
    def parse(self, response):
        self.s = False
        title = response.xpath('/html/head/title/text()').extract()
        url = response.url
        phone = re.findall(r'\d+', url)
        print(phone[0])
        print(title)

        try :
            if response.status==302 or response.status==404:
                return {
                    'phone':phone[0], 
                    'label':"出现302 or 404"
                }
                self.slinger += 1
                globalvar.set_value("slinger", self.slinger)
                if self.slinger>=3:
                    print('等待3分钟',response.status)
                    time.sleep(300)
            else:
                self.slinger = 0
                globalvar.set_value("slinger", self.slinger)
        except:
            self.slinger = 0
            globalvar.set_value("slinger", self.slinger)
        if title ==['百度安全验证'] or title ==[]:
            self.anquan+=1
            globalvar.set_value("anquan", self.anquan)
            return {
                'phone':phone[0],
                'label':"跳过访问号码"
            }
            if self.anquan>=3:
                # 就要在这个地方实现整套的换参数
                self.anquan=0
                globalvar.set_value("anquan", self.anquan)
                time.sleep(300)
                pass
        
        flag = re.findall(r'class="(c-border.*?)"', response.text)
        print(flag)
        if flag:
            # print( '//*[@class="{}"]'.format(flag[0]))
            cxpath = '//*[@class="{}"]'.format(flag[0])
            contents = response.xpath(
                cxpath
            ).extract()
            conten = re.findall(r'>(.*?)<', contents[0])#所有内容数组
            while '' in conten:
                conten.remove('')
            cont = ''
            for i in range(len(conten)):
                conten[i] = conten[i].replace(' ', "").replace("\xa0", " ").replace("\n", "").strip()
                cont += conten[i]
            if flag[0]=='c-border':
                adders = conten[3]
                name = conten[1]
                if adders== "号码报错":
                    adders = conten[2]
                    name = conten[0]
                print(adders, name, cont)
            elif flag[0]=='c-border op_fraudphone_container':
                adders = conten[1]
                name = conten[4]
                print(adders, name, cont)
            # elif flag[0]=='':
            #     pass
            else:
                adders=''
                name =''
            # print(key, phone, adders, name, cont)
            if len(re.findall(r'^公司名称自动识别EMS申通快递', cont))==0:
                print(adders, name, cont)
                return {
                    'phone':phone[0], 
                    'adders':adders, 
                    'name':name, 
                    'cont':cont
                }
            else:
                pass
    '''
    步骤
        首先判断状态码302 404 
            1.出现5次以上等待3分钟
            2.一旦出现写入 未访问成功跳过.csv
        进入页面了在判断是否是百度安全验证页面或者无名字页面
            1.出现5次以上等待3分钟
            2.一旦出现写入 未访问成功跳过.csv
        如果两种情况都未出现获取到正常页面
            对页面内容提取保存
    '''
                    
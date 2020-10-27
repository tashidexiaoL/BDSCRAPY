# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import random
import requests
import globalvar
'''
定期更换ip步骤
    a判断ip的使用次数
    b判断是否更换ip
    getiplist定义需要更换参数
    changeip拼接参数到请求头上
    重要参数 ua ip cookie
'''
'''
生成16进制字符串
from random import *
 
print (  "".join([choice("0123456789ABCDEF") for i in range(12)]) )
print (  "".join([choice("0123456789ABCDEF") for i in range(30)]) )
a = "".join([choice("0123456789ABCDEF") for i in range(12)]) )
print (bytes.fromhex("a"))
'''
# 定期更换ip cookie 等参数
class ChangeIpMiddleware(object):
    """docstring for ClassName"""
    # 获取一个ip 使用一百条之后在替换下一个ip
    def __init__(self):
        # http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=
        self.get_url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='#获取十条ip
        self.count = 0
        self.evecount = 0
        self.cookie = ''
        self.useragent=''
        print('ip中间件的执行')
        # 获取ip 改变代理ip  判断是否要获取ip是否要更换ip
    def getiplist(self, request):
        self.temp_data = requests.get(url=self.get_url).text#获取ipjson
        print('*************')
        print(self.temp_data)
        print('***************************')
        COOKIE_LIST = [
        'PSTM=1584623944; BAIDUID=684329DDF31DE9C2E3028B72C21519AA:FG=1; BIDUPSID=2EF3C8DD52F8C2DCAEAFE8010B606982; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ispeed_lsm=2; __yjsv5_shitong=1.0_7_686caa55d1a253698ede338cf671aec79ee5_300_1602423015437_119.36.10.243_89935a56; yjs_js_security_passport=ae93798bdf1ec81bed33023b195e31e2503bed1d_1602423016_js; delPer=0; BD_CK_SAM=1; PSINO=3; BD_HOME=1; ZD_ENTRY=baidu; H_PS_PSSID=7513_32617_1423_7566_31253_32706_32230_7516_32115_32719; shifen[133492395591_21487]=1602424756; BCLID=7380781490700298531; BDSFRCVID=nnKOJeC62mEIhgbrAIeIM6-n6B0vwPvTH6ao4kPBcFFi6dZxw6VQEG0PHx8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRk8oI85JDvDqTrP-trf5DCShUFsWM3mB2Q-XPoO3KO6s-_RKxLb5b-IjmcXtjjiWbRn_xbgylRp8P3y0bb2DUA1y4vpK-5Xb2TxoUJ2WJkKKJjqqtnWbJ_ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hCPGjT--ejJM5pJfeJbKaDr03RrK-P8_Hn7zeUO5XM4pbt-qJtr4bgJ9-Pop2lvT8DLzh6DKDRFbhGonBT5Kaa5pafn4MqQCqqOJ26rNKltkQN3TQhLO5bRiLRoMbxFKDn3oyUvJXp0n3tvly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJPKtfJuO_I-yJDLMbP365IT0M-FD-q5t546B2C6XsJOOaCvNohjOy4oTj6DjhtrL2tJH06TDBpCKHRu-VDbdMUnC3MvB-fnNKxQtJnTKoDONLnQmJbvLQft20h4beMtjBbQa-IvUWn7jWhvdep72yhodQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCHqT0JfnFq_Iv5b-0_JRnYhtQK5t_HMxrK2D62aKDsWJrcBhcqEIL4hfozM--VK4QAKxcuJtjX_q_Mbt3mfxbSj4Qoj-PrLxbl0tFq5NQOLKQCLl5nhMJS257JDMP0-l3ML-7y523i2n3vQpnl8hQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0-nDSHHD8JjjP; COOKIE_SESSION=1076_5_7_4_6_12_0_1_7_5_0_4_51187_9119_0_0_1602423889_1602408142_1602424755%7C9%2316625_21_1602424755%7C7; H_PS_645EC=7847SxiFgzPy2g72YPji%2BcoKXXlOLqfn4UdV4DoOM1owh%2Bjcg1UMZHoBiks',
        'PSTM=1584623944; BAIDUID=684329DDF31DE9C2E3028B72C21519AA:FG=1; BIDUPSID=2EF3C8DD52F8C2DCAEAFE8010B606982; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=AXAOJeC62lmImncrAuqhM6-n6Q4hkORTH6aoReEu45a23EPfPxkZEG0P_x8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tRk8oI85JDvDqTrP-trf5DCShUFsWM3mB2Q-XPoO3KO6s-_RKxLb5b-IjmcXtjjiWbRn_xbgylRp8P3y0bb2DUA1y4vpK-5Xb2TxoUJ2WJkKKJjqqtnWbJ_ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hCPGjT--ejJM5pJfeJbKaDr03RrK-P8_Hn7zeUO5XM4pbt-qJtr4bgJ9-Pop2lvT8DLzh6DKDRFbhGonBT5Kaa5pafn4MqQCqqOJ26rNKltkQN3TQhLO5bRiLRoMbxFKDn3oyUvJXp0n3tvly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJPKtfJuO_I-yJDLMbP365IT0M-FD-q5t546B2C6XsJOOaCvNohjOy4oTj6DjhtrL2tJH06TDBpCKHRu-VDbdMUnC3MvB-fnNKxQtJnTKoDONLnQmJbvLQft20h4beMtjBbQa-IvUWn7jWhvdep72yhodQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjH62btt_tRcP; ispeed_lsm=2; __yjsv5_shitong=1.0_7_686caa55d1a253698ede338cf671aec79ee5_300_1602420313537_119.36.10.243_addb7d6c; yjs_js_security_passport=36ddc93598b3313a538053fa2e0984b90efcb179_1602420314_js; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_645EC=2a84nw7t3Q1cXeky30vLtAEVamhk4N9bZnJVlJegoMoiJnqtavP5Nf5bOcw; H_PS_PSSID=7513_32617_1423_31253_32706_32230_7516_32115_32719; BDSVRTM=0',
        'PSTM=1584623944; BAIDUID=684329DDF31DE9C2E3028B72C21519AA:FG=1; BIDUPSID=2EF3C8DD52F8C2DCAEAFE8010B606982; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=AXAOJeC62lmImncrAuqhM6-n6Q4hkORTH6aoReEu45a23EPfPxkZEG0P_x8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tRk8oI85JDvDqTrP-trf5DCShUFsWM3mB2Q-XPoO3KO6s-_RKxLb5b-IjmcXtjjiWbRn_xbgylRp8P3y0bb2DUA1y4vpK-5Xb2TxoUJ2WJkKKJjqqtnWbJ_ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hCPGjT--ejJM5pJfeJbKaDr03RrK-P8_Hn7zeUO5XM4pbt-qJtr4bgJ9-Pop2lvT8DLzh6DKDRFbhGonBT5Kaa5pafn4MqQCqqOJ26rNKltkQN3TQhLO5bRiLRoMbxFKDn3oyUvJXp0n3tvly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJPKtfJuO_I-yJDLMbP365IT0M-FD-q5t546B2C6XsJOOaCvNohjOy4oTj6DjhtrL2tJH06TDBpCKHRu-VDbdMUnC3MvB-fnNKxQtJnTKoDONLnQmJbvLQft20h4beMtjBbQa-IvUWn7jWhvdep72yhodQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjH62btt_tRcP; ispeed_lsm=2; __yjsv5_shitong=1.0_7_686caa55d1a253698ede338cf671aec79ee5_300_1602423015437_119.36.10.243_89935a56; yjs_js_security_passport=ae93798bdf1ec81bed33023b195e31e2503bed1d_1602423016_js; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_PSSID=7513_32617_1423_31253_32706_32230_7516_32115_32719; H_PS_645EC=580dZTc8HHav2HrqsyrDoC0V2wM5ikhEQ9e%2F%2Bft7LVrlnPlvBCUKCK6iz2A',
        'PSTM=1584623944; BAIDUID=684329DDF31DE9C2E3028B72C21519AA:FG=1; BIDUPSID=2EF3C8DD52F8C2DCAEAFE8010B606982; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=AXAOJeC62lmImncrAuqhM6-n6Q4hkORTH6aoReEu45a23EPfPxkZEG0P_x8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tRk8oI85JDvDqTrP-trf5DCShUFsWM3mB2Q-XPoO3KO6s-_RKxLb5b-IjmcXtjjiWbRn_xbgylRp8P3y0bb2DUA1y4vpK-5Xb2TxoUJ2WJkKKJjqqtnWbJ_ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hCPGjT--ejJM5pJfeJbKaDr03RrK-P8_Hn7zeUO5XM4pbt-qJtr4bgJ9-Pop2lvT8DLzh6DKDRFbhGonBT5Kaa5pafn4MqQCqqOJ26rNKltkQN3TQhLO5bRiLRoMbxFKDn3oyUvJXp0n3tvly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJPKtfJuO_I-yJDLMbP365IT0M-FD-q5t546B2C6XsJOOaCvNohjOy4oTj6DjhtrL2tJH06TDBpCKHRu-VDbdMUnC3MvB-fnNKxQtJnTKoDONLnQmJbvLQft20h4beMtjBbQa-IvUWn7jWhvdep72yhodQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjH62btt_tRcP; ispeed_lsm=2; __yjsv5_shitong=1.0_7_686caa55d1a253698ede338cf671aec79ee5_300_1602423015437_119.36.10.243_89935a56; yjs_js_security_passport=ae93798bdf1ec81bed33023b195e31e2503bed1d_1602423016_js; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_PSSID=7513_32617_1423_7566_31253_32706_32230_7516_32115_32719; H_PS_645EC=1260DNgbufP%2FbN19pC3ZuLUqr1nmWoOXdinf5T618B7ScwEBjUD6cxnLtZM',
        'PSTM=1584623944; BAIDUID=684329DDF31DE9C2E3028B72C21519AA:FG=1; BIDUPSID=2EF3C8DD52F8C2DCAEAFE8010B606982; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ispeed_lsm=2; BDSFRCVID=ZTPOJeC62mEIhgbrATpQM6-n6B0vwPvTH6ao4kPBcFFi6dZxw6VQEG0PHx8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRk8oI85JDvDqTrP-trf5DCShUFsWM3mB2Q-XPoO3KO6s-_RKxLb5b-IjmcXtjjiWbRn_xbgylRp8P3y0bb2DUA1y4vpK-5Xb2TxoUJ2WJkKKJjqqtnWbJ_ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hCPGjT--ejJM5pJfeJbKaDr03RrK-P8_Hn7zeUO5XM4pbt-qJtr4bgJ9-Pop2lvT8DLzh6DKDRFbhGonBT5Kaa5pafn4MqQCqqOJ26rNKltkQN3TQhLO5bRiLRoMbxFKDn3oyUvJXp0n3tvly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJPKtfJuO_I-yJDLMbP365IT0M-FD-q5t546B2C6XsJOOaCvNohjOy4oTj6DjhtrL2tJH06TDBpCKHRu-VDbdMUnC3MvB-fnNKxQtJnTKoDONLnQmJbvLQft20h4beMtjBbQa-IvUWn7jWhvdep72yhodQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCHqT0JfnFq_Iv5b-0_JRnYhtQK5t_HMxrK2D62aKDsWJrcBhcqEIL4hfozM--VK4QAKxcuJtjX_q_Mbt3mfxbSj4Qoj-PrLxbl0tFq5NQOLKQCLl5nhMJS257JDMP0-l3ML-7y523i2n3vQpnl8hQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0D6v3jaAqtj0sb5vfstcS2R6Hq45ph46E-t6H-UnLqhTnLgOZ0l8KtJ6pOJnT-R5N3b8uXHDL2j5GtTcfbPQmWIQHDIbc0M5jQxKtjxOzhn-qQH64KKJxWPPWeIJo5t52bp-jhUJiBM7MBan7-lRIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TF5DTjbjfK; yjs_js_security_passport=e96aae112173b01638f9182575a87d80233d3f02_1602426997_js; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_645EC=b9b0sTqVs0YfVPcOZOMumr95rEllo4TfBGL7u%2Fwnf%2BkMx8JxsjCF%2FGAovH8; BDSVRTM=204; H_PS_PSSID=7513_32617_1423_7567_31253_32706_32230_7516_32115_32719',
        'BIDUPSID=4EEB924AB1A92704EEA1456D5B55CC9C; PSTM=1591750107; BAIDUID=A2CBBC03A3622196449D919732F5E223:FG=1; MCITY=-%3A; BD_UPN=12314753; BDSFRCVID=iyFOJeC62mEIhgbrAt5zT4DcrZ0vwPvTH6ao4kPBcFFi6dZxw6VQEG0PHx8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJ-J_IPKJD-3fP36qR6sMtu_KloK2tT0KC_X3b7EfbTBsl7_bf--D4ukyf7M5JjCbnTE-IbgK-oAh-Q60bjxy5K_hNOWQUj23ec0_JbuMP0-SxjHQT3mybvbbN3i-4jj5avQWb3cWhRJ8UbS3fvPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55utfRkD_MK; delPer=0; BD_CK_SAM=1; PSINO=7; BD_HOME=1; COOKIE_SESSION=13589_3_9_9_69_47_1_9_9_9_1_14_0_0_10_2_1602309470_1602308991_1602323049%7C9%2318696_62_1602308989%7C9; H_PS_645EC=d7f1fewLQKNA2WOpPOvR4stckRf8FkODVhXnsh%2FD3Xms%2FXzPDCHnhKziZkA; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSVRTM=13; H_PS_PSSID=32816_32617_1456_32790_31660_32706_32231_7517_7605_32116_32718_22160',
        'BIDUPSID=4EEB924AB1A92704EEA1456D5B55CC9C; PSTM=1591750107; BAIDUID=A2CBBC03A3622196449D919732F5E223:FG=1; MCITY=-%3A; BD_UPN=12314753; BDSFRCVID=iyFOJeC62mEIhgbrAt5zT4DcrZ0vwPvTH6ao4kPBcFFi6dZxw6VQEG0PHx8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJ-J_IPKJD-3fP36qR6sMtu_KloK2tT0KC_X3b7EfbTBsl7_bf--D4ukyf7M5JjCbnTE-IbgK-oAh-Q60bjxy5K_hNOWQUj23ec0_JbuMP0-SxjHQT3mybvbbN3i-4jj5avQWb3cWhRJ8UbS3fvPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55utfRkD_MK; delPer=0; BD_CK_SAM=1; PSINO=7; BD_HOME=1; COOKIE_SESSION=13589_3_9_9_69_47_1_9_9_9_1_14_0_0_10_2_1602309470_1602308991_1602323049%7C9%2318696_62_1602308989%7C9; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=32816_32617_1456_32790_7566_31660_32706_32231_7517_7605_32116_32718_22160; H_PS_645EC=0be3zVi2WhMXUX949F8sqform%2BtHb9BBelwk3JyRA42548ZOClKBeenQOJg',
        'BIDUPSID=4EEB924AB1A92704EEA1456D5B55CC9C; PSTM=1591750107; BAIDUID=A2CBBC03A3622196449D919732F5E223:FG=1; MCITY=-%3A; BD_UPN=12314753; BDSFRCVID=iyFOJeC62mEIhgbrAt5zT4DcrZ0vwPvTH6ao4kPBcFFi6dZxw6VQEG0PHx8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJ-J_IPKJD-3fP36qR6sMtu_KloK2tT0KC_X3b7EfbTBsl7_bf--D4ukyf7M5JjCbnTE-IbgK-oAh-Q60bjxy5K_hNOWQUj23ec0_JbuMP0-SxjHQT3mybvbbN3i-4jj5avQWb3cWhRJ8UbS3fvPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55utfRkD_MK; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=7; H_PS_PSSID=32816_32617_1456_32790_31660_32706_32231_7517_7605_32116_32718_22160; H_PS_645EC=c0e1CJqKtFzspN1nzwcbHiI3FF9Hls7BSgDchbBm5S3z3xT8kY872QKUhoE',
        'BIDUPSID=4EEB924AB1A92704EEA1456D5B55CC9C; PSTM=1591750107; BAIDUID=A2CBBC03A3622196449D919732F5E223:FG=1; MCITY=-%3A; BD_UPN=12314753; BDSFRCVID=iyFOJeC62mEIhgbrAt5zT4DcrZ0vwPvTH6ao4kPBcFFi6dZxw6VQEG0PHx8g0KubpgWlogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJ-J_IPKJD-3fP36qR6sMtu_KloK2tT0KC_X3b7EfbTBsl7_bf--D4ukyf7M5JjCbnTE-IbgK-oAh-Q60bjxy5K_hNOWQUj23ec0_JbuMP0-SxjHQT3mybvbbN3i-4jj5avQWb3cWhRJ8UbS3fvPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0exbH55utfRkD_MK; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=7; BD_HOME=1; H_PS_645EC=9339GkLMRb1%2FdfZOemy0YpjbqlVnU1qbEenCKl4H55yrGiIR3%2FlqwpVaabM; H_PS_PSSID=32816_32617_1456_32790_31660_32706_32231_7517_7605_32116_32718_22160; BDSVRTM=0',
        'BAIDUID=A2CBBC03A3622196449D919732F5E223:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BIDUPSID=4EEB924AB1A92704EEA1456D5B55CC9C; MCITY=-%3A; PSTM=1591750107; BD_UPN=12314753; COOKIE_SESSION=641_4_9_7_42_53_0_5_9_5_0_12_749_0_5_0_1602484531_1602308991_1602484526%7C9%23174752_73_1602483741%7C9; BD_HOME=1; delPer=0; BD_CK_SAM=1; H_PS_645EC=59b4dtlvm7oKAuJNLpdUMHo4huX3JXvBDda107HCwDZ4cZRQvs3rwu%2BJfts; PSINO=7; BDSVRTM=24; H_PS_PSSID=32816_32617_1456_32790_7567_31660_32706_32231_7517_7605_32116_32718_22160',
        ]
        # ACCEPT =[
            #     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #     # 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
            #     # '*/*',
            # ]
        self.cookie = random.choice(COOKIE_LIST)
        print('随机出来的cookie', self.cookie)
        rand_use = UserAgent().random
        if rand_use:
            self.useragent = rand_use
    # 更改代理ip
    def process_request(self, request, spider):
        # print('是否执行中间件')
        # 获取s的值 当s=1时触发更改函数
        print(globalvar.get_value("anquan"), globalvar.get_value('slinger'), "=================================")
        if globalvar.get_value("anquan")>=3 or globalvar.get_value('slinger'):
            print('302出现三次以上 需要更换一套参数')
            self.getiplist(request)
            globalvar.set_value("slinger", 0)
            globalvar.set_value("anquan", 0)
        self.evecount+=1
        if self.count <= 0:
            self.getiplist(request)#获取代理ip
            self.count+=1
        if self.evecount>=80:
            self.count=0
            self.evecount=0
        else:
            pass
        self.changeip(request)
    def changeip(self, request):
        request.headers['user-agent'] = self.useragent
        request.headers['cookie']= self.cookie
        try:
            request.meta["proxy"] = 'http://'+str(self.temp_data)
            # .replace('/n','').replace('/n','')
            print('设置定期更改的proxy_ip', request.meta["proxy"])
        except :
            print('代理ip未获取到')
# 其他相关参数模拟
class HeaderscanshuMiddleware(object):
    def process_request(self, request, spider):
        request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # request.headers['cookie']= cookies,
        # request.headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        request.headers['Accept-Encoding'] = 'gzip, deflate, br',
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8',
        request.headers['Cache-Control'] = 'max-age=0',#控制缓存开关
        request.headers['Connection'] = 'keep-alive',
        request.headers['Host'] = 'www.baidu.com',
        request.headers['Sec-Fetch-Dest'] = 'document',
        request.headers['HoSec-Fetch-Modest'] = 'navigate',
        request.headers['Sec-Fetch-Site'] = 'same-origin',
        request.headers['Sec-Fetch-User'] = '?1',
        request.headers['Upgrade-Insecure-Requests'] = '1'
        # print('cookie', request.headers['cookie'])
# 随机referer中间件
class RandomRefererMiddleware(object):
    def process_request(self, request, spider):
        request.headers['referer'] = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}&fenlei=256&rsv_pq=d1800bac00058ab0&rsv_t=0dd3C%2B%2BhcSELg7hy9azb5dKxdWJruGoIIcDBr6BW1%2FuKulgDrC5Gebzbpck&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=6&rsv_sug1=5&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=4274&rsv_sug4=4274'.format(str(random.randint(0, 100000000)))
        print('中间件设置referer',request.headers['referer'])

















































# class RandomUserAgentMiddleware:
    #     ua = UserAgent()
    #     referers = [
    #         r"https://www.baidu.com/s?wd=%E6%9C%89%E5%93%AA%E4%BA%9B%E5%8F%B7%E7%A0%81&rsf=8&rsp=7&f=1&oq=96%E5%8F%B7%E7%A0%81&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=f0214ac700006428&rsv_t=0bf5voT5y4Heot4EBg0uWIMuV%2F3gYYTBVn2MKQXcifAo%2F5OyfNb9PsfPx4w&rqlang=cn&rs_src=1&rsv_pq=f0214ac700006428&rsv_t=0bf5voT5y4Heot4EBg0uWIMuV%2F3gYYTBVn2MKQXcifAo%2F5OyfNb9PsfPx4w",
    #         r"https://www.baidu.com/s?wd=96%E5%87%A0%E7%9A%84%E5%8F%B7%E7%A0%81%E6%98%AF%E4%BB%80%E4%B9%88%E6%83%85%E5%86%B5&rsf=1000012&rsp=2&f=1&oq=96%E5%8F%B7%E7%A0%81&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=f0214ac700006428&rsv_t=0bf5voT5y4Heot4EBg0uWIMuV%2F3gYYTBVn2MKQXcifAo%2F5OyfNb9PsfPx4w&rqlang=cn&rs_src=0&rsv_pq=f0214ac700006428&rsv_t=0bf5voT5y4Heot4EBg0uWIMuV%2F3gYYTBVn2MKQXcifAo%2F5OyfNb9PsfPx4w",
    #         r"https://www.baidu.com/s?wd=96%E5%8F%B7%E7%A0%81%E7%94%B3%E8%AF%B7%E6%9D%A1%E4%BB%B6&rsf=1000013&rsp=0&f=1&oq=96%E5%8F%B7%E7%A0%81&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=f0214ac700006428&rsv_t=0bf5voT5y4Heot4EBg0uWIMuV%2F3gYYTBVn2MKQXcifAo%2F5OyfNb9PsfPx4w&rqlang=cn&rs_src=0&rsv_pq=f0214ac700006428&rsv_t=0bf5voT5y4Heot4EBg0uWIMuV%2F3gYYTBVn2MKQXcifAo%2F5OyfNb9PsfPx4w",
    #         r"https://www.baidu.com/s?wd=96%E5%BC%80%E5%A4%B4%E6%98%AF%E4%BB%80%E4%B9%88%E7%94%B5%E8%AF%9D&rsf=27&rsp=0&f=1&oq=96%E5%BC%80%E5%A4%B4%E7%9A%84%E7%94%B5%E8%AF%9D&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=9916774d00005c1d&rsv_t=3076Owz3IA3rsjXwj%2BWJ9JHJsmVO0TUI%2FR4%2FVv9pJpxpwQgfllT%2BDJ0E24Q&rqlang=cn&rs_src=0&rsv_pq=9916774d00005c1d&rsv_t=3076Owz3IA3rsjXwj%2BWJ9JHJsmVO0TUI%2FR4%2FVv9pJpxpwQgfllT%2BDJ0E24Q",
    #         r"https://www.baidu.com/s?wd=960%E5%BC%80%E5%A4%B4%E6%98%AF%E4%BB%80%E4%B9%88%E7%94%B5%E8%AF%9D&rsf=27&rsp=1&f=1&oq=96%E5%BC%80%E5%A4%B4%E7%9A%84%E7%94%B5%E8%AF%9D&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=9916774d00005c1d&rsv_t=3076Owz3IA3rsjXwj%2BWJ9JHJsmVO0TUI%2FR4%2FVv9pJpxpwQgfllT%2BDJ0E24Q&rqlang=cn&rs_src=0&rsv_pq=9916774d00005c1d&rsv_t=3076Owz3IA3rsjXwj%2BWJ9JHJsmVO0TUI%2FR4%2FVv9pJpxpwQgfllT%2BDJ0E24Q",
    #         r"https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=96%E5%BC%80%E5%A4%B4%E7%9A%84%E7%94%B5%E8%AF%9D&oq=96%25E5%258F%25B7%25E7%25A0%2581&rsv_pq=f0214ac700006428&rsv_t=0bf5voT5y4Heot4EBg0uWIMuV%2F3gYYTBVn2MKQXcifAo%2F5OyfNb9PsfPx4w&rqlang=cn&rsv_enter=1&rsv_dl=ts_0&inputT=4114&rsv_sug3=17&rsv_sug1=19&rsv_sug7=100&rsv_sug2=0&prefixsug=96%25E5%25BC%2580%25E5%25A4%25B4%25E7%259A%2584&rsp=0&rsv_sug4=5014",
    #         r"https://www.baidu.com/s?wd=ios%E6%80%8E%E4%B9%88%E6%8B%A6%E6%88%AA96%E5%BC%80%E5%A4%B4%E6%89%80%E6%9C%89%E7%94%B5%E8%AF%9D&rsf=1000008&rsp=0&f=1&oq=96%E7%94%B5%E8%AF%9D%E6%B3%9B%E6%BB%A5&ie=utf-8&rsv_idx=1&rsv_pq=bfe2f64f0000da2e&rsv_t=7991SksEppVtoouxFzGnbRJP4YUqluuAxEdDkC0gKzjliXcVOduFVNnBg%2BI&rqlang=cn&rs_src=0&rsv_pq=bfe2f64f0000da2e&rsv_t=7991SksEppVtoouxFzGnbRJP4YUqluuAxEdDkC0gKzjliXcVOduFVNnBg%2BI",
    #         r"https://www.baidu.com/s?wd=96%E5%BC%80%E5%A4%B4%E5%8F%B7%E7%A0%81%E5%A6%82%E4%BD%96%E6%8B%A6%E6%88%AA&rsf=1000009&rsp=1&f=1&oq=96%E7%94%B5%E8%AF%9D%E6%B3%9B%E6%BB%A5&ie=utf-8&rsv_idx=1&rsv_pq=bfe2f64f0000da2e&rsv_t=7991SksEppVtoouxFzGnbRJP4YUqluuAxEdDkC0gKzjliXcVOduFVNnBg%2BI&rqlang=cn&rs_src=0&rsv_pq=bfe2f64f0000da2e&rsv_t=7991SksEppVtoouxFzGnbRJP4YUqluuAxEdDkC0gKzjliXcVOduFVNnBg%2BI",
    #         r"https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=96%E5%BC%80%E5%A4%B4%E7%9A%84%E5%8F%B7%E7%A0%81&oq=96%25E7%2594%25B5%25E8%25AF%259D%25E6%25B3%259B%25E6%25BB%25A5&rsv_pq=bfe2f64f0000da2e&rsv_t=0601AvMJSHP%2FHRHptmKIbvryQoHwl45zYklwPaPv4XqhByD0ogv2hFzg3r8&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=9663&rsv_sug3=52&rsv_sug1=47&rsv_sug7=100&rsv_sug2=0&rsv_sug4=10364",
    #         r"https://www.baidu.com/s?wd=96741%E6%98%AF%E4%BB%80%E4%B9%88%E7%94%B5%E8%AF%9D%E5%8F%B7%E7%A0%81&rsf=1000001&rsp=4&f=1&oq=96%E5%BC%80%E5%A4%B4%E7%9A%84%E5%8F%B7%E7%A0%81&ie=utf-8&rsv_idx=1&rsv_pq=eeb8ef78000071d4&rsv_t=5960ZXPS3d%2FB8Cad9eLxlvc%2ByrrCbuB40ndhHfJ%2BH7pzvvTAgNeLPspH%2F28&rqlang=cn&rs_src=0&rsv_pq=eeb8ef78000071d4&rsv_t=5960ZXPS3d%2FB8Cad9eLxlvc%2ByrrCbuB40ndhHfJ%2BH7pzvvTAgNeLPspH%2F28",
    #         r"https://www.baidu.com/s?wd=96%E5%BC%80%E5%A4%B4%E7%9A%84%E7%94%B5%E8%AF%9D%E6%9C%89%E5%93%AA%E4%BA%9B&rsf=1000013&rsp=1&f=1&oq=96%E5%BC%80%E5%A4%B4%E7%9A%84%E5%8F%B7%E7%A0%81&ie=utf-8&rsv_idx=1&rsv_pq=a23840370000ce20&rsv_t=58ebEFQhOvfDIPet8sASwDlfEp6hSf5F9yCWrlDBomIcxNHL54b2V%2Bp8Vp0&rqlang=cn&rs_src=0&rsv_pq=a23840370000ce20&rsv_t=58ebEFQhOvfDIPet8sASwDlfEp6hSf5F9yCWrlDBomIcxNHL54b2V%2Bp8Vp0",
    #         r"https://www.baidu.com/s?wd=%E4%B9%B0%E9%9D%93%E5%8F%B7%E9%AA%97%E5%B1%80&rsf=1000001&rsp=2&f=1&oq=96%E5%BC%80%E5%A4%B4%E7%9A%84%E5%8F%B7%E7%A0%81&ie=utf-8&rsv_idx=1&rsv_pq=b6709d590000ef28&rsv_t=86fbKLNZaXWoXOtqLV8x7V9ol0kzFO5yCLNPfG4NbrtdFWtq1V8zkVIMV90&rqlang=cn&rs_src=0&rsv_pq=b6709d590000ef28&rsv_t=86fbKLNZaXWoXOtqLV8x7V9ol0kzFO5yCLNPfG4NbrtdFWtq1V8zkVIMV90",
    #     ]

    #     def process_request(self, request, spider):
    #         # request.meta["proxy"] = "http://127.0.0.1:1080" # 代理
    #         request.headers["User-Agent"] = self.ua.random  # 随机User-Agent
    #         request.headers["Referer"] = random.choice(self.referers)  # 伪造Referer


    # class BaiduSpiderMiddleware(object):
    #     # Not all methods need to be defined. If a method is not defined,
    #     # scrapy acts as if the spider middleware does not modify the
    #     # passed objects.

    #     @classmethod
    #     def from_crawler(cls, crawler):
    #         # This method is used by Scrapy to create your spiders.
    #         s = cls()
    #         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #         return s

    #     def process_spider_input(self, response, spider):
    #         # Called for each response that goes through the spider
    #         # middleware and into the spider.

    #         # Should return None or raise an exception.
    #         return None

    #     def process_spider_output(self, response, result, spider):
    #         # Called with the results returned from the Spider, after
    #         # it has processed the response.

    #         # Must return an iterable of Request, dict or Item objects.
    #         for i in result:
    #             yield i

    #     def process_spider_exception(self, response, exception, spider):
    #         # Called when a spider or process_spider_input() method
    #         # (from other spider middleware) raises an exception.

    #         # Should return either None or an iterable of Response, dict
    #         # or Item objects.
    #         pass

    #     def process_start_requests(self, start_requests, spider):
    #         # Called with the start requests of the spider, and works
    #         # similarly to the process_spider_output() method, except
    #         # that it doesn’t have a response associated.

    #         # Must return only requests (not items).
    #         for r in start_requests:
    #             yield r

    #     def spider_opened(self, spider):
    #         spider.logger.info("Spider opened: %s" % spider.name)


    # class BaiduDownloaderMiddleware(object):
    #     # Not all methods need to be defined. If a method is not defined,
    #     # scrapy acts as if the downloader middleware does not modify the
    #     # passed objects.

    #     @classmethod
    #     def from_crawler(cls, crawler):
    #         # This method is used by Scrapy to create your spiders.
    #         s = cls()
    #         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #         return s

    #     def process_request(self, request, spider):
    #         # Called for each request that goes through the downloader
    #         # middleware.

    #         # Must either:
    #         # - return None: continue processing this request
    #         # - or return a Response object
    #         # - or return a Request object
    #         # - or raise IgnoreRequest: process_exception() methods of
    #         #   installed downloader middleware will be called
    #         return None

    #     def process_response(self, request, response, spider):
    #         # Called with the response returned from the downloader.

    #         # Must either;
    #         # - return a Response object
    #         # - return a Request object
    #         # - or raise IgnoreRequest
    #         return response

    #     def process_exception(self, request, exception, spider):
    #         # Called when a download handler or a process_request()
    #         # (from other downloader middleware) raises an exception.

    #         # Must either:
    #         # - return None: continue processing this exception
    #         # - return a Response object: stops process_exception() chain
    #         # - return a Request object: stops process_exception() chain
    #         pass

    #     def spider_opened(self, spider):
    #         spider.logger.info("Spider opened: %s" % spider.name)

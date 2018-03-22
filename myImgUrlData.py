#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import json,time
def save_cookit():
    LOGIN_URL = 'admin/login' #请求地址只留下后缀了
    values = {'username': 'admin', 'password': 'f7c3bc1d808e04732adf679965ccc34ca7ae3441'} # , 'submit' : 'Login'
    postdata = urllib.parse.urlencode(values).encode('utf-8')
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    cookie_filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象来保存cookie，之后写入文件
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    #创建cookie处理器
    handler = urllib.request.HTTPCookieProcessor(cookie)
    #构建opener
    opener = urllib.request.build_opener(handler)

    request = urllib.request.Request(LOGIN_URL, postdata, headers)

    try:
        response = opener.open(request)
        page = response.read().decode()
        # print(page)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError:%d" % e.code)
        elif hasattr(e, 'reason'):
            print("URLError:%s" % e.reason)

    cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
    print('保存cookie成功')
'''
    get_url = ''  # 利用cookie请求訪问还有一个网址
    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = opener.open(get_request)
    print(get_response.read().decode())
    # print('You have not solved this problem' in get_response.read().decode())
'''

def get_cookit():
    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
    return cookie

def post(url, data):
    req = urllib.request.Request(url)
    data = urllib.parse.urlencode(data).encode(encoding='UTF8')
    #enable cookie
    cookie = get_cookit()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    response = opener.open(req, data)
    return response.read()

def getUrlArr(posturl,data):
    jsons = json.loads(post(posturl, data)) #转为json
    arr_data = jsons['res']
    all_img = []
    for obj in arr_data:
        if obj['urls'] != None:
            for val in obj['urls']:
                all_img.append(val)
    return all_img

def getIdArr(posturl,data):
    jsons = json.loads(post(posturl, data)) #转为json
    arr_data = jsons['res']
    all_id = []
    try:
        for obj in arr_data:
                all_id.append(obj['id'])
    except:
        all_id.append('24101')
    return all_id
def killOneNode(id):
    posturl = 'change_audit' #请求地址只留下后缀了
    data =  {'type': 0,'r_id': id }
    post(posturl,data)

def forbidden(uid):
    stop_days = time.strftime("%Y-%m-%d",time.localtime(time.time() + 2592000))
    posturl = "admin/user_change" #请求地址只留下后缀了
    data =  {'uid': uid,'stop_days': stop_days}
    post(posturl,data)

def main():  #返回所有图片url

    posturl = 'admin/audit' #请求地址只留下后缀了
    data = {'page': "",'r_id': "",'date': "",'title': "",'content': "",'status':1,'uid': ""}
    #  print (post(posturl, data))  #打印post请求返回数据
    return getUrlArr(posturl,data)

if __name__ == '__main__':
    save_cookit()
    #print(main())
    #forbidden(1511811)

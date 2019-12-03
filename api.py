from flask import request
import json, urllib
from urllib.request import urlopen

#API key for google civic
#AIzaSyBkXSJMObWSWQ7x8fpkGbksi-MQxbWvbj8

#API key for open weather
#da19d101a993403bd4ab9a3284ec0f0d

#Get IP: request.environ['REMOTE_ADDR']
#IP Stack key: 143e7f36d3776304d9bca36e109fc225
#http://ip-api.com/json/165.155.139.162?fields=status,message,isp,org,as,asname,reverse,mobile,proxy,query

def getIP():
    ipstack = urllib.request.urlopen("http://api.ipstack.com/check?access_key=143e7f36d3776304d9bca36e109fc225&format=1").read()
    ipstackData = json.loads(ipstack)
    return ipstackData["ip"]

def getCity():
    ipstack = urllib.request.urlopen("http://api.ipstack.com/"+getIP()+"?access_key=143e7f36d3776304d9bca36e109fc225&format=1").read()
    ipstackData = json.loads(ipstack)
    return ipstackData["city"]

def getISP():
    ipapi = urllib.request.urlopen("http://ip-api.com/json/"+getIP()+"fields=status,message,isp,org,as,asname,reverse,mobile,proxy,query").read()
    ipapiData = json.loads(ipstack)
    return ipapiData["isp"]

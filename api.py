from flask import request
import json, urllib

#API key for Full Contact
#fQqUtVhwiJSAtMWCpe9zR8MTOTFxoTZ6

#API key for google civic
#AIzaSyBkXSJMObWSWQ7x8fpkGbksi-MQxbWvbj8

#Get IP: request.environ['REMOTE_ADDR']
#IP Stack key: 143e7f36d3776304d9bca36e109fc225
#http://ip-api.com/json/165.155.139.162?fields=status,message,isp,org,as,asname,reverse,mobile,proxy,query
def getIP():
    return request.environ['REMOTE_ADDR']
    
def getCity():
    ipstack = urllib.urlopen("http://api.ipstack.com/"+getIP()+"?access_key=143e7f36d3776304d9bca36e109fc225&format=1").read
    ipstackData = json.loads(ipstack)
    return ipstackData["city"]
    
def getISP():
    ipapi = urllib.urlopen("http://ip-api.com/json/"+getIP()+"fields=status,message,isp,org,as,asname,reverse,mobile,proxy,query")
    ipapiData = json.loads(ipstack)
    return ipapiData["isp"]
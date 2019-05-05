#/bin/env python
#-*- coding:utf-8-*-
import os, sys, json
import httplib, urllib, urllib2
from optparse import OptionParser

class WeChat:

    def __init__(self, argement):
 
        self.corpID = "xxxxxx"
        self.secret = "xxxxxx"
        self.agentId = argement['agentId']
        self.toParty = argement['toParty']
        self.content = argement['content']

    def getToken(self):

        params = urllib.urlencode({'corpid':self.corpID, 'corpsecret':self.secret})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        httpClient = httplib.HTTPSConnection('qyapi.weixin.qq.com', 443)
        httpClient.request("POST", "/cgi-bin/gettoken?%s" % params, headers=headers)
        response = httpClient.getresponse()
        ret = response.read()
        token = json.loads(ret)['access_token']
        httpClient.close()
        self.toKen = token.encode('utf-8')

    def sendMsg(self):
        data = {
               "toparty":self.toParty,
               "msgtype":"text",
               "agentid":int(self.agentId),
               "text":{
                      "content":self.content,
                      },
               "safe":"0",
              }
        data = json.dumps(data, ensure_ascii=False)
        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s'%(self.toKen,), data)
        resp = urllib2.urlopen(req)
        msg = resp.read()    

def main():

    optParser = OptionParser()

    optParser.add_option("-a","--agent",action = "store",
                         type="string",dest = "agentId",
                         help="enterprise application id")
    
    optParser.add_option("-g","--toparty",action = "store",
                         type="string",dest = "toParty",
                         help="department id")
    
    optParser.add_option("-m","--content",action = "store",
                         type="string",dest = "content",
                         help="send message")
                         
                         
    (options, args) = optParser.parse_args()
    
    if not options.agentId or not options.toParty or not options.content:
        sys.exit(-1)

    wechat = WeChat(options.__dict__)
    wechat.getToken()
    wechat.sendMsg()
    
if __name__ == "__main__":
    main()
    
    
    
    
    

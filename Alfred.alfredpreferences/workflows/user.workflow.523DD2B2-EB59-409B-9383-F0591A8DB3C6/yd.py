#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import json
import sys



LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"
#logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
#logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class icon:
    def __init__(self,typ,path):
        self.typ = typ
        self.path = path
    def jsonStr(self):
        return """
    {{
        "type":"{}",
        "path":"{}"
    }}
    """.format(self.typ,self.path)

class item:
    def __init__(self,uid,typ,title,subtitle,arg,autocomplete,icon):
        self.uid = uid
        self.typ = typ
        self.title = title
        self.subtitle = subtitle
        self.arg = arg
        self.autocomplete = autocomplete
        self.icon = icon

    def jsonStr(self):
        return """
    {{
        "uid":"{}",
        "type":"{}",
        "title":"{}",
        "subtitle":"{}",
        "arg":"{}",
        "autocomplete":"{}",
        "icon":{}
    }}
    """.format(self.uid,self.typ,self.title,self.subtitle,self.arg,self.autocomplete,self.icon.jsonStr())

class items:
    def __init__(self,*item):
        self._items = []
        for i in item:
            self._items.append(i)
    def addItem(self,*item):
        for i in item:
            self._items.append(i)

    def jsonStr(self):
        jsonArray = [i.jsonStr() for i in self._items]
        body = ",".join(jsonArray)

        ret =  """{{
        "items":[
            {}
        ]
        }}
        """.format(body)
        o = json.loads(ret)
        return json.dumps(o,indent=4,ensure_ascii=False)
def main():
    scriptFilter(sys.argv[1])


url = "http://fanyi.youdao.com/openapi.do"
i = icon("","")

def query(word):
    import json
    cfg = None

    try:
        with open('config.json') as f:
            cfg = json.load(f)
    except:
        errorItem = item("uid","default","load config.json error","failed","","",i)
        resultItems = items(errorItem)
        print(resultItems.jsonStr())
        sys.exit()
    
    payload = {
            "keyfrom":cfg['keyfrom'],
            "key":cfg['key'],
            "type":"data",
            "doctype":"json",
            "version":"1.1",
            "q":word
            }
    try:
        import requests
    except ModuleNotFoundError:
        errorItem = item("uid","default","Not found module 'requests'","failed","","",i)
        resultItems = items(errorItem)
        print(resultItems.jsonStr())
        sys.exit()
    resp = requests.get(url,params=payload)
    if resp.ok:
        return resp.text
    else:
        return ""

def scriptFilter(word):
    res = query(word)
    #for DEBUG,otherwise comment it
    # print("res:{}".format(res))
    resultItems = items()
    if len(res) == 0:
        # it = item("uid","mytype","title","subtitle","arg","autocomplete",i)
        errorItem = item("query error","default","query error","failed","","",i)
        # resultItems = items(errorItem)
        resultItems.addItem(errorItem)
        print(resultItems.jsonStr())
    else:
        o  = json.loads(res)
        if 'errorCode' in o:
            if o['errorCode'] != 0:
                errorItem = item("error","default","errorCode not 0","failed","","",i)
                # resultItems = items(errorItem)
                resultItems.addItem(errorItem)
                print(resultItems.jsonStr())
                sys.exit()

        phonetic = ''
        if 'basic' in o:
            if 'us-phonetic' in o['basic']:
                phonetic = "[ {} ]".format(o['basic']['us-phonetic'])
            if 'explains' in o['basic']:
                for e in o['basic']['explains']:
                    trans = item("uid","default",e,phonetic,e,"",i)
                    resultItems.addItem(trans)
        if 'translation' in o:
            trans = item("uid","default",o['translation'][0],phonetic,o['translation'][0],"",i)
            resultItems.addItem(trans)
        
        if 'web' in o:
            for w in o['web']:
                t = []
                for v in w['value']:
                    t.append(v)
                trans = item("uid","default",w['key'],';'.join(t),w['key'],"",i)
                resultItems.addItem(trans)


        print(resultItems.jsonStr())


if __name__ == '__main__':
    main()


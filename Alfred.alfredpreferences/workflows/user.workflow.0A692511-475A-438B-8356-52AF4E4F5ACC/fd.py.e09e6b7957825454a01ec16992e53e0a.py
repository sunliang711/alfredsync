#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys

"""
alfred script filter的输出内容是一个json字符串, 它的格式如下:
    {
        "items":[
            {
                "uid":"",
                "type":"",
                "title":"",
                "subtitle":"",
                "arg":"",
                "autocomplete":"",
                "icon":{
                    "type":"",
                    "path":""
                }
            },
            {},
            ...
        ]
    }

整体是上是一个json对象，里面有一个键值对，键名称为items，值是一个json数组；数组中成员是一个json对象，这个对象包括：
"uid","type","title","subtitle","arg","autocomplete","icon"成员，其中除了icon又是一个对象外，其他都是字符串。icon
对象包括了"type"和"path"成员。具体信息参考:https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
 
 uid:可选，每个item的uid要唯一；
 TODO

上面所说的items，items的成员，icon分别由下面的3个python class来表示:items, item, icon
"""

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

class icon:
    """
    type设置为fileicon时，alfred会取得path指定路径的图标作为script filter显示的图标:path是目录则显示这个目录的图标，是go文件则显示go文件的图标；
    """
    def __init__(self,typ,path):
        self.typ = typ
        self.path = path
    def jsonStr(self):
        if self.typ != "" and self.path != "":
            return """
            {{
            "type":"{}",
            "path":"{}"
            }}
            """.format(self.typ,self.path)
        elif self.typ != "":
            return """
            {{
                "type":"{}"
            }}
            """.format(self.typ)
        elif self.path != "":
            return """
            {{
            "path":"{}"
            }}
            """.format(self.path)
        else:
            return "{}"

def main():
    items1 = items()
    icon1 = icon("","")

    ## test BEGIN
    # item1 = item("uid1","file","title1","subtitle1","arg1","autocomplete1",icon1)
    # item2 = item("uid2","file","title2","subtitle2","arg2","autocomplete2",icon1)


    # items1.addItem(item1)
    # items1.addItem(item2)

    # print(items1.jsonStr())
    ## test END

    import subprocess
    import os

    fd_executable=sys.argv[1]
    option = sys.argv[2]
    pattern = sys.argv[3]
    dest = sys.argv[4]

    if len(option) > 2:
        option=option[1:len(option)-1]
    #debug
    # print("fd_executable: {}".format(fd_executable))
    # print("pattern: {}".format(pattern))
    # print("dest: {}".format(dest))
    # print("option: {}".format(option))

    # find files
    cmd="{} {} {} {}".format(fd_executable, option, pattern, dest)
    # print("cmd: {}".format(cmd))
    process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    stdout,stderr = process.communicate()
    # print("after run")
    files_found = stdout.decode('utf-8').split('\n')
    # print("files_found: {}".format(len(files_found)))
    for f in files_found:
        if f == '':
            continue
        # print("f: {}".format(f))
        fields = f.split("/")
        basename = fields[len(fields)-1]
        icon1 = icon("fileicon",f)
        # print("{} {}".format(basename,f))
        if os.path.isdir(f):
            icon1 = icon("fileicon","~/Desktop")
        itemFound = item(f,"file",basename,f,f,"autocomplete",icon1)
        items1.addItem(itemFound)

    print(items1.jsonStr())



if __name__ == '__main__':
    main()


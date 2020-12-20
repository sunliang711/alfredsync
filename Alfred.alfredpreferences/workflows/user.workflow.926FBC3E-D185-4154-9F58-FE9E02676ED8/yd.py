# check py verion
# check requests library
# make query string

import json
import requests
import sys

url = "http://fanyi.youdao.com/openapi.do"

configFile = "config.json"
def config(keyfrom,key):
    """config key to config.json file"""
    payload = {
            "keyfrom":keyfrom,
            "key":key,
            "type":"data",
            "doctype":"json",
            "version":"1.1",
            }
    with open(configFile,"w") as cf:
        cf.write(json.dumps(payload))


def query(word):
    """query word"""
    with open(configFile) as cf:
        payload = json.loads(cf.read())
	  
        payload["q"] = word
        resp = requests.get(url,params=payload)
        return resp.text
# config("myiosworkflow","884997728")

def Query(word):
	payload = {
            "keyfrom":"myiosworkflow",
            "key":"884997728",
            "type":"data",
            "doctype":"json",
            "version":"1.1",
		    "q":word
            }
	resp = requests.get(url,params=payload)
	jsonObj = json.loads(resp.text)
	return json.dumps(jsonObj,indent=4,ensure_ascii=False)
	#return resp.text
print(Query(sys.argv[1]))
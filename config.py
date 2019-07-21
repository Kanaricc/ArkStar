import json
import os

pointdata=None
gconfig=None
with open('pointdata.json','r') as f:
    pointdata=json.load(f)
with open('config.json','r') as f:
    gconfig=json.load(f)

def unpack(poslr):
    return poslr[0:2],poslr[2:4]

def save():
    with open('pointdata.json','w+') as f:
        f.write(json.dumps(pointdata, indent=4, sort_keys=True,ensure_ascii=False))
    
    with open('config.json','w+') as f:
        f.write(json.dumps(gconfig, indent=4, sort_keys=True,ensure_ascii=False))
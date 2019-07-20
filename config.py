import json
import os

pointdata=None
with open('pointdata.json','r') as f:
    pointdata=json.load(f)

def unpack(poslr):
    return poslr[0:2],poslr[2:4]
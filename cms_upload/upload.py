"""
   upload images to cms.ishield.cn
"""

import json
import requests
import os
import datetime
from PIL import Image

def evaluate_model(items, name, fields, index=None, search=None):

    session = requests.session()

    resp = session.post('http://cms.ishield.cn/login',

                        data={'username': 'admin', 'password': 'qwert54321'})

    print("login finished: %s" % resp)

    data = {"fields": fields,

            "index": index,

            "search": search,

            "items": items}

    data = dict(filter(lambda x: x[1], data.items()))

    url = 'http://cms.ishield.cn/model/%s' % name

    resp = session.post(url, data=json.dumps(data))

    print resp



def get_items_for_evaluation(file_name, key, thre):

    ret = []

    doc = open(file_name).readlines()

    for i, line in enumerate(doc):

        try:

            item = json.loads(line.strip())

            im = Image.open(item['file'])

            w, h = im.size

            if w < 150 or h < 224:

                continue

            if item[key] >= thre:

                tag = 1

            else:

                tag = 0

            item.update({'image': '<img src="%s" width=300 height=300>' % item['url'],

                         'score': item[key],

                         'tag': tag})

            ret.append(item)
    #        print 'append item!'

        except Exception, e:

            print("exception: %s" % traceback.format_exc())

    #ret = sorted(ret, key=lambda x: x['total_impression'], reverse=True)

    #ret = ret[:10000]

    #random.shuffle(ret)

    #ret = ret[:1000]

    return ret



def main():

    file_name = '/data/yangqianwen/istock/upload.data'
   
    key = 'score'

    thre=0.0

    items = get_items_for_evaluation(file_name, key, thre)

    name = 'istock2'

    fields = ['group_id:str', 'image:str', 'score:float', 'total_impression:int', 'tag:int']

    evaluate_model(items, name, fields)

if __name__=="__main__":

    main()

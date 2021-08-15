import pymongo
import utils.class_fetch as class_fetch
import utils.wiki_fetch as wiki_fetch
import requests
import os
import sys
from gridfs import *
import random


ip = "localhost"
db_name = 'FGRec'
collection_name = 'WikiData'

mongo_client = pymongo.MongoClient(ip, 27017)
db = mongo_client[db_name]
collection = db[collection_name]
img_collection = db['WikiImages']

img_root_path = '/home/zhaoxue/services/flask_service/WikiImages/'


def download_img(img_url, img_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        "Mozilla/5.0 (Windows NT 10.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.3; …) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Windows NT 10.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
    headers['User-Agent'] = random.choice(user_agent_list)
    r = requests.get(img_url, headers=headers, stream=True)
    # print(r.status_code) # 返回状态码
    if r.status_code == 200:
        with open(img_path, 'wb') as f:
            f.write(r.content)
        print("Saved: "+image_path)
        return True
    else:
        print("Failed to download")

def save_img_to_collection(path, img_id):
    file = open(path, 'rb')
    gridfs_put = GridFS(img_collection)
    gridfs_put.put(file)


# Read CUB-200-2011 classes file to get class name
for i in range(190, 200):
    class_id = i+1
    class_name = class_fetch.get_class_name(class_id)
    ########### Get Wiki data
    summary, order_name, family_name, genus_name, species_name, page_url, image_url = wiki_fetch.get_wiki_data(class_name)

    ########### Download images
    split = image_url.split('.')
    image_type = split[len(split) - 1]
    image_path = img_root_path + str(class_id) + '.' + image_type
    # download_img(image_url, image_path)

    ########### Save other info to MongoDB, WikiData collection
    class_entry = {
        'class_id': class_id,
        'class_name': class_name,
        'summary': summary,
        'taxonomy': {
            'order': order_name,
            'family': family_name,
            'genus': genus_name,
            'species': species_name,
        },
        'page_url': page_url,
        'image_url': image_url,
        'image_path': image_path,
    }

    collection.insert_one(class_entry)
    print(str(class_id)+' inserted')

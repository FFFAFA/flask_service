import json

import pymongo

ip = "localhost"
db_name = 'FGRec'
collection_name = 'records'

mongo_client = pymongo.MongoClient(ip, 27017)
db = mongo_client[db_name]
collection = db[collection_name]


def insert(rec):
    collection.insert_one(rec)


def update(rec):
    query = {
        'record_id': rec['record_id']
    }
    to_update = {
        '$set': {
            'location': rec['location']
        }
    }
    collection.update_one(query, to_update)


def find_wiki(class_name):
    col = db['WikiData']
    wiki_data = col.find_one({"class_name": class_name})
    return wiki_data


def find_pinned_records_locations():
    query = {
        'location': {
            '$exists': True
        }
    }
    records = collection.find(query)
    pinned_records_locations = [{'latitude': rec['location']['latitude'], 'longitude': rec['location']['longitude'], 'record_id': rec['record_id']} for rec in records]
    return pinned_records_locations


def find_pinned_record_detail(record_id):
    query = {
        'record_id': record_id
    }
    record = collection.find_one(query)
    return record

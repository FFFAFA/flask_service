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


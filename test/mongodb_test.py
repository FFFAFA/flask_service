import pymongo

ip = "localhost"
mongo_client = pymongo.MongoClient(ip, 27017)

dblist = mongo_client.list_database_names()
print(dblist)

db = mongo_client['local']
print(db.list_collection_names())
collection = db['startup_log']
print(collection.count_documents({}))

# Create
# Update
# Read
# Delete


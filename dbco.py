from pymongo import MongoClient, errors

# TODO: Move this to a config file.
localConnection = 'mongodb://127.0.0.1:27017/'
client = MongoClient(localConnection)
db = client['hgp']

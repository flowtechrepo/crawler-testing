import pymongo


mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongoclient["facebook"]
mycol = db["groups"]
groups = []
for x in mycol.find({}, {"plafform":"facebook"}):
    groups.append(x["_id"])
print(groups)
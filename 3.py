import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['291db']
collection = db['dblp']

n = int(input("Enter the number of venues to list: "))

pipeline = [
    {
        "$match": {"venue": "international conference on human-computer interaction"}
    },
    
    {
        "$limit": n
    }
]

results = collection.aggregate(pipeline)

print("Result Number | Venue | Number of Articles | Number of References")
print("-----------------------------------------------------------------")

i = 0
for result in results:
    num_articles = collection.aggregate({"$count": {}})
   
    string = "{:<13} | {:<25} | {:<13} | {:<13}".format(i, result['venue'], )
    print(result['title'])

    i += 1

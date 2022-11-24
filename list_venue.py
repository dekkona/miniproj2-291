def list_venue(db):
    ven = db.dblp.aggregate([{"$group": {"_id": "$venue", "count": {"$sum": 1}}},
                             {"$project": {"venue": "$_id", "count": 1, "_id": 0}},
                             {"$sort": {"venue": -1}}])
    val = False
    n_venue = list(ven)
    try:
        while not val:
            n = int(input("Enter the number n of top venues to see list:"))
            if n >= len(n_venue):
                print("n exceeds venue count. Please enter smaller number.")
            elif n <= 0:
                print("n must be greater than 0")
            else:
                val = True
    except(Exception):
        print("Invalid entry")
        return
    venue_refs = db.vendb.aggregate([{"$lookup":
                             {"from": "dblp",
                              "localField": "id",
                              "foreignField": "references",
                              "as": "refs"}},
                                     {"$addFields": {"num": {"$size": "$refs"}}},
                        {"$group":
                             {"_id": "$venue", "references": {"$sum": "$num"}}},
                        {"$project":{"venue": "$_id", "references": 1, "_id": 0}},
                                     {"$sort": {"references": -1}}, {"$limit": n}])
    for i, j in zip(venue_refs, n_venue):
        print("{venue: " + i["venue"] + " | Articles: " + str(j["count"]) + " | Referenced by: " + str(i["references"])+"}")

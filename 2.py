def searchAuthor(db):
    auth = input("Search for an author: ")
    query = {"$search": "(\"{}\"".format(auth)}
    results = db.dblp.aggregate([{"$match": {"$text": query}},
                                 {"$unwind": "$authors"},
                                 {"$match": {"authors": {"$regex": auth, "$options": "i"}}},
                                 {"$group": {"_id": "$authors",
                                             "Publications": {"$sum": 1}}},
                                 {"$sort": {"year": -1}},
                                 {"$addFields": {"Author": "$_id"}},
                                 {"$project": {"_id": 0, "Author": 1, "Publications": 1}}])
    count = 1
    resArr = list(results)
    for i in resArr:
        print(f"{count}. {i}")
        count += 1
    opt = int(input("Select an author to view all publications. 0 to return to main menu: "))
    if opt in range(1, len(resArr) + 1):
        get_pubs = db.dblp.find({"authors": resArr[opt - 1].get('Author')},
                                {"_id": 0, "title": 1, "year": 1, "venue": 1})
        for i in get_pubs:
            print(i)
    else:
        pass

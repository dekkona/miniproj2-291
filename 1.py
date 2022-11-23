def searchArticles(db):
    word = input("Search for an article: ")
    try:
        word = int(word)
        results = db.dblp.find({"year": word})
    except:
        query = {"$search": "(\"{}\"".format(word)}
        results = db.dblp.find({"$text": query},
                                {"_id": 1, "title": 1, "year": 1, "venue": 1})
    count = 1
    resArr = list(results)
    for i in resArr:
        print(f"{count}. {i}")
        count += 1
    opt = int(input("Select an article to view more. 0 to return to main menu: "))
    if opt in range(1, len(resArr) + 1):
        get_one = db.dblp.find_one({"_id": resArr[opt - 1].get('_id')},
                               {"_id": 1, "title": 1, "abstract": 1, "venue": 1, "authors": 1,
                                "year": 1})
        refs = db.dblp.aggregate([{"$unwind": "$references"},
                                  {"$match": {"references": resArr[opt - 1].get('_id')}},
                                  {"$group": {"_id":"$_id"}},
                                  {"$project": {"_id": 1, "title": 1, "year": 1}}
        ])
        print(get_one)
        print("Article referenced by:")
        for i in refs:
            print(i)
        # return to main menu here
    else:
        pass
        # return to main menu here

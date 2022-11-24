def searchArticles(db):
    word = input("Search for an article: ")
    try:
        word = int(word)
        results = db.dblp.find({"year": word})
    except:
        query = {"$search": "(\"{}\"".format(word)}
        results = db.dblp.find({"$text": query},
                                {"_id": 0, "id": 1, "title": 1, "year": 1, "venue": 1})
    count = 1
    num = 0
    for i in results:
        num = 1
        print(f"{count}. {i}")
        count += 1
    results.rewind()
    resArr = list(results)
    if num == 0:
        # return to main menu
        print("No matching articles found")
        pass
    opt = int(input("Select an article to view more. Any other input to return to main menu: "))
    if opt in range(1, count):
        oid = resArr[opt - 1].get('id')
        get_one = db.dblp.find_one({"id": oid},
                               {"_id": 0, "id": 1, "title": 1, "abstract": 1, "venue": 1, "authors": 1,
                                "year": 1})
        print(get_one)
        refs = db.dblp.find({"references": oid},
                            {"_id": 0, "title": 1, "year": 1, "id": 1})
        print("Article referenced by:")
        for i in refs:
            print(i)
        # return to main menu here
    else:
        pass
        # return to main menu here

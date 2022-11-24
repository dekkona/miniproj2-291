
def list_venues(db):
    collec = db['dblp'] 

    # get distinct venues for venue_count
    venues = collec.distinct("venue")
    venue_count = len(venues)
    # get user input for top n venues
    valid_n = False
    while not valid_n:
        inp_n = input("Enter a number n and see a listing of top n venues: ")
        try:
            inp_n = int(inp_n)
            if inp_n > venue_count:
                print("n exceeds number of venues. Please enter a smaller number.")
            elif inp_n <= 0:
                print("n must be greater than zero.")
            else:
                valid_n = True
        except ValueError:
            print("n must be an integer.")    

    # for each distinct venue get count
    top_venues = list(collec.aggregate([{"$group": {"_id": "$venue", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": inp_n}]))
    print(top_venues)
    top_refs = {}
    top_count = {}
    # get articles that fall under top n venues
    for venue in top_venues:
        articles = list(collec.aggregate([{'$match': {'venue': {'$eq': venue['_id']}}}, {'$project': {"id": '$id', '_id': 0}}]))
        ids = []
        for article in articles:
            ids.append(article["id"])
        
        article_refs = list(collec.aggregate([{'$match': {'references': {'$elemMatch': {'$in': ids}}}}]))
        top_count.update({venue['_id']: venue['count']})
        top_refs.update({venue['_id']: len(article_refs)})
    
    #top_refs = {k: v for k, v in sorted(top_refs.items(), key=lambda item: item[1][1], reverse = True)}
    print(top_count)    
    print(top_refs)

    i=1
    print('\nTop Venues')
    for k, v in top_count.items():
        print(('-'*50)+'\n#'+str(i)+ '\nVenue: ' + k + '\nArticles in Venue: ' + str(top_count[k]) + '\nReferences: ' + str(top_refs[k]))
        i += 1

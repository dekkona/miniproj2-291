from pymongo import MongoClient
from pymongo import TEXT
import json
import datetime

def valid_port():
    server_input = ''
    invalid_server_input = True
    while invalid_server_input:
        server_input = input("Please input a mongodb server: ")
        try:
            server_input = int(server_input)
            invalid_server_input = False
        except ValueError:
            print("Please enter an integer for the server")

    return server_input

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
    #print(top_venues)
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


def add_article(db):
    collec = db['dblp'] 

    unique_aid = False

    while not unique_aid:
        aid = input('Enter a unique article id: ')
        aid_exists = collec.find_one({'id': aid})

        if aid_exists:
            print('Article id already exists. Please try again')

        else:
            unique_aid = True

    title = input('Enter an article title: ')

    authors = []
    done_adding = False
    while not done_adding:
        author = input("Enter an author name: ")
        authors.append(author)
        valid_yn = False
        while not valid_yn:
            cont_add = input("Continue adding authors? (y/n) ").strip().lower()
            if cont_add == 'y' or cont_add == 'n':
                valid_yn = True
            else:
                print("Please enter 'y' for yes and 'n' for no.")
        if cont_add == 'n':
            done_adding = True
    
    valid_year = False
    today = datetime.date.today()
    curr_year = today.year

    while not valid_year:
        year = input("Enter a year: ")
        try:
            year = int(year)
            if year <= curr_year and year >= 0:
                valid_year = True 
            else:
                print("Please enter a valid year.")
        except ValueError:
            print("Please enter an int for year.")
    
    article = {"abstract": None, "authors": authors, "n_citation": 0, "references": [], 
    "title": title, "venue": None, "year": year, "id": aid}

    collec.insert_one(article)
    print(f'Article: "{title}" (id: {aid}) has been added')


def main():
    port = valid_port()

    # connect to server
    client = MongoClient(f'mongodb://localhost:{port}')
   
    # create or connect to the database
    db_name = '291db'
    db = client[db_name] 
    print(f"Connected to {db_name}")

    # create document store menu
    option = None
    while option != 'e':
        option = input("\nMenu\n" + ('-'*50) + "\n'sar' to Search for Articles,\n'sa' to Search for Authors,\n'lv' to List the Venues,\n'aa' to Add an Article,\nor 'e' to Exit: ").strip().lower()

        if option == 'aa': 
            add_article(db)
        elif option == 'lv':
            list_venues(db)
        elif option == 'sar':
            searchArticles(db)
        elif option == 'sa':
            searchAuthor(db)

main()

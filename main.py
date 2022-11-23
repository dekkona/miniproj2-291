from pymongo import MongoClient
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

def list_venues(db):
    collec = db['dblp'] 
    # get distinct venues
    venues = collec.distinct("venue")
    # for each n venue get count
    all_venues = {}
    for v in venues:
        if v != None and v != '':
            cursor = collec.aggregate([{'$match': {'venue': {'$eq': v}}},{'$count': v}])
            venue_info = list(cursor)[0]
            for key, value in venue_info.items():
                all_venues[key] = value
    # sort venues by count
    all_venues = {k: v for k, v in sorted(all_venues.items(), key=lambda item: item[1])}
    venue_count = len(all_venues)
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
    # newdict 'top_venues' for top n venues
    rev = list(reversed(list(all_venues)))[0:inp_n]
    top_venues = {}
    for key in rev:
        top_venues[key]=all_venues.get(key)
    
    # get articles that fall under top n venues
    all_articles = list(collec.find())

    reference_counts = []
    for ven, num in top_venues.items():
        #print(key, values)
        cursor = collec.aggregate([{'$match': {'venue': {'$eq': ven}}}])
        articles = list(cursor)
        all_article_refs = []
        for article in articles:
            cursor = collec.aggregate([{'$match': {'references': {'$elemMatch': {'$eq': article['id']}}}}])
            article_refs = list(cursor)
            if article_refs not in all_article_refs:
                all_article_refs.append(article_refs)
        top_venues[ven] = [num, len(all_article_refs)] # top_venues = {venue: [count, ref_count]}
    
    # sort venues by reference count
    top_venues = {k: v for k, v in sorted(top_venues.items(), key=lambda item: item[1][1], reverse = True)}
    
    i=1
    print('\nTop Venues')
    for k, v in top_venues.items():
        print(('-'*50)+'\n#'+str(i)+ '\nVenue: ' + k + '\nArticles in Venue: ' + str(v[0]) + '\nReferences: ' + str(v[1]))
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
    #port = valid_port()

    # connect to server
    #client = MongoClient(f'mongodb://localhost:{port}')
    client = MongoClient(f'mongodb://localhost:27012')
    # create or connect to the database
    db_name = '291db'
    db = client[db_name] 
    print(f"Connected to {db_name}")

    # create document store menu
    option = None
    while option != 'e':
        option = input("\nEnter\n" + ('-'*50) + "\n'sar' to Search for Articles,\n'sa' to Search for Authors,\n'lv' to List the Venues,\n'aa' to Add an Article,\nor 'e' to Exit: ").strip().lower()

        if option == 'aa': 
            add_article(db)
        elif option == 'lv':
            list_venues(db)

main()

# def test():
#     client = MongoClient(f'mongodb://localhost:27012')
#     # create or connect to the database
#     db_name = '291db'
#     db = client[db_name] 
#     print(f"Connected to {db_name}")
#     collec = db['dblp'] 

#     cursor = collec.aggregate([{'$match': {'references': {'$elemMatch': {'$eq': "6b727e8c-85bf-42ae-8bf4-715f82aedd9a"}}}}])
#     #cursor = collec.find({'references': {'$elemMatch': {'$eq': '0102f234-e30b-4b35-88a4-27e57838947a'}}})
#     article_refs = list(cursor)
#     print(len(article_refs))
# test()
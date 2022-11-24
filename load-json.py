from pymongo import MongoClient
from pymongo import TEXT
import os

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
def createIndex(col):
    print("creating indexes...")
    col.create_index([("abstract", TEXT), ("authors", TEXT), ('title', TEXT), ('venue', TEXT), ('references', TEXT)],
                     default_language="none")    

def init_collection(db, collec_name, c_file, portNum):

    # Create the collection in the db
    collec = db[collec_name]

    # delete all previous entries in the collection
    # specify no condition.
    collec.delete_many({})

    # insert the loaded data into the collection    
    print(f"Adding into collection: {collec_name}\n")
    print("\nadding data:")
    os.system(f'mongoimport --host localhost:{portNum} --db 291db --collection dblp --file {c_file} --batchSize 1000')     
    createIndex(collec)


def main():
    port = valid_port()
    json_file = input('json file name: ')

    # connect to server
    client = MongoClient(f'mongodb://localhost:{port}')

    # create or connect to the database
    db_name = '291db'
    db = client[db_name] 
    
    print(f"Created database {db_name}")

    # init a collection with its name and its imported json file data
    init_collection(db, 'dblp', json_file, port)

main()

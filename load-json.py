from pymongo import MongoClient
import json



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

def init_collection(db, collec_name, c_file):

    # Create the collection in the db
    collec = db[collec_name]

    # delete all previous entries in the collection
    # specify no condition.
    collec.delete_many({})

    # insert the loaded data into the collection
    # file large so intert row by row in for loop

    print(f"Adding into collection: {collec_name}\n")
    curr_row = 1
    with open(c_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            print(f"Adding in row #{curr_row}", end='\r')
            collec.insert_one(data)
            curr_row += 1

    print(f"\nAll {curr_row-1} rows inserted")


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
    init_collection(db, 'dblp', json_file)

main()

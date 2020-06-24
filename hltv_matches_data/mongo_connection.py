from pymongo import MongoClient
import time

def get_connection(collection, database='matches_data'):
    client = MongoClient('mongo_link')
    db = client[database]
    collection = db[collection]
    return collection

def match_in_database(match_link):
    upcoming_matches = get_connection('upcoming_matches_data')
    match_id = int(match_link.split("/")[4])
    match_in_database = upcoming_matches.find_one( { "match_id": {"$eq": match_id } })
    document_count = upcoming_matches.count_documents({"match_id": {"$eq": match_id}})
    
    if document_count > 0:
        return True
    else:
        return False

def update_match_timestamp(match_id, match_timestamp):
    match_timestamp = int(match_timestamp)
    upcoming_links = get_connection('upcoming_matches_links')
    myquery = { "match_id": {"$eq": match_id } }
    newvalues = { "$set": { "match_timestamp": match_timestamp } }
    upcoming_links.update_one(myquery, newvalues)

def link_in_database(match_id):
    upcoming_matches = get_connection('upcoming_matches_links')
    # match_in_database = upcoming_matches.find_one( { "match_id": {"$eq": match_id } })
    document_count = upcoming_matches.count_documents({"match_id": {"$eq": match_id}})
    
    if document_count > 0:
        return True
    else:
        return False

def get_upcoming_links():
    minutes5 = int(time.time()+300)
    minutes65 = int(time.time()+39000)

    upcoming_matches = get_connection('upcoming_matches_links')
    matches_database = upcoming_matches.find( { "$and": [ { "match_timestamp": {"$gt": minutes5 } },{ "match_timestamp": {"$lt": minutes65 } }]})
    return matches_database

def odds_added(match_id):
    odds_in_database = get_connection('betting_odds')
    match_in_database = odds_in_database.find( { "match_id": {"$eq": match_id } })
    document_count = odds_in_database.count_documents({"match_id": {"$eq": match_id}})
    if document_count > 0:
        return True
    else:
        return False



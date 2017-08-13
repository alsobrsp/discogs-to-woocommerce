#!/usr/bin/env python
# TODO: Create release updated table
# TODO: Instances that are no longer in a store folder should be deactivated in the store

from __future__ import print_function
#from datetime import date, datetime, timedelta
import mysql.connector
import discogs_client
#import os
import pprint
from woocommerce import API
import sys
import traceback
import dbqueries as dbq
import hashlib
pp = pprint.PrettyPrinter(indent=4)

# DB connection setup
importdb = mysql.connector.connect(user='alsobrsp', 
                                                            password='spanky5', 
                                                            host='db.seasies.com', 
                                                            database='webuser_decadesofvinyl.com')
dbcursor = importdb.cursor()
dbcursor_dict = importdb.cursor(dictionary=True)


# WooCommerce API setup
wcapi = API(
    url="https://www.decadesofvinyl.com",
    consumer_key="ck_f839dfe156f0253a7b4a7cd810a40de86d1b1519",
    consumer_secret="cs_220b8c6746a0733df9c73c656ef699db8baaceca",
    wp_api=True,
    version="wc/v2"
)

# Discogs API setup
UserAgent = 'DoV/0.1 +https://www.decadesofvinyl.com'
AuthToken = "DiSiupFPDVYxsOqpOtwjXmfENbNeLNfhhaCYqbso"
d = discogs_client.Client(UserAgent, user_token=AuthToken)
user = d.identity()

# Hash instance notes
def hashNotes(instance_notes):
    try:
        notes_chksum = hashlib.md5()
        notes_chksum.update(str(instance_notes).encode())
    except:
        pass
    else:
        return notes_chksum
    finally:
        del notes_chksum

# TODO: Update woo_id
# Probably need two functions
def updateInstanceWoo(instance_id):
    pass

# Get Discogs instance info
# TODO: change folder id in table on folder change
def discogsImport (store_folder):
    query = None
    hashing_note = ''
    
    try:
        # Clear db in_store flag
        dbcursor.execute(dbq.clear_in_store_flag)
        
        # Get instance list from db
        dbcursor.execute(dbq.get_instance_id_list,  (store_folder,  ))
        db_instances = dbcursor.fetchall()
        db_instances = [i[0] for i in db_instances]
    except :
        pp.pprint(dbcursor.statement)
        traceback.print_exc(file=sys.stdout)
        sys.exit(5)
    else:
        importdb.commit()
    
    # Set collection
    collection = user.collection_folders

    # Get folder index
    for idxFolder in range(len(collection)):
        if collection[idxFolder].id == store_folder:
            store_folder = idxFolder

    # Populate import table
    for album in collection[store_folder].releases:
        # Remove instance from list
        # FIXME: remove wont work. We get a list of tuples
        # Suggestion is to use temp table
        db_instances.remove(album.instance_id)

        # Concatenate notes
        hashing_note = None
        for idx in range(len(album.notes)):
            hashing_note = str(hashing_note) + str(album.notes[idx]['field_id']) + str(album.notes[idx]['value'])

        # Hash the notes
        notes_chksum = hashNotes(hashing_note)

        #  Check import table
        try:
            dbcursor_dict.execute(dbq.check_instance,  (album.instance_id, ))
            db_instance = dbcursor_dict.fetchone()
        except :
            pp.pprint(dbcursor.statement)
            traceback.print_exc(file=sys.stdout)
            sys.exit(5)
            
        # Set in_store flag
        query_data = {'instance_id': album.instance_id}
        query = dbq.still_in_store

        # New items
        if db_instance == None:
            
            # Build insert data
            query_data = {'instance_id': album.instance_id,
                                    'rating': album.rating,
                                    'title': album.release.title,
                                    'folder_id': album.folder_id,
                                    'discogs_date_added':  album.date_added,
                                    'notes': str(album.notes),
                                    'notes_chksum': notes_chksum.hexdigest(),
                                    'release_id': album.id, 
                                    'in_store': True, 
                                    'update_store': True}
            query = dbq.add_instance

        # Update notes if hash is different
        elif db_instance['instance_id'] == album.instance_id and db_instance['notes_chksum'] != notes_chksum.hexdigest():
            pass
            query_data = {'notes': str(album.notes),
                                     'notes_chksum': notes_chksum.hexdigest(),
                                     'in_store': True,
                                     'update_store': True,  
                                     'instance_id': album.instance_id}
                                     
            query = dbq.update_instance_notes_chksum

        # Return instance to store
        elif db_instance['instance_id'] == album.instance_id and db_instance['not_in_store'] == 1:
            query_data = {'instance_id': album.instance_id}
            query = dbq.return_in_store
            
        # Execute queries
        if query != None:
            try:
                dbcursor.execute(query,  query_data )
            except :
                pp.pprint(dbcursor.statement)
                traceback.print_exc(file=sys.stdout)
                sys.exit(5)
        importdb.commit()

# Query DB for instance data
def getInstanceData(instance_id):
    dbcursor_dict.execute(dbq.get_instance_info,  (instance_id,))
    instance_data = dbcursor_dict.fetchone()
    return instance_data

# TODO: genre match table
def getGenres():    
    pass



# Create Product
def createWooProduct (instance_id):
    pass
    # Create Woo Product
#   data = {
#        "name": "Premium Quality",
#        "type": "simple",
#        "regular_price": "21.99",
#        "description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.",
#        "short_description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
#    }
#    
#   product = wcapi.post("products", data).json()
    

# TODO: updates based on instance notes and release update
def updateWooProduct(instance_id):
    pass

def getStorefolders():
    # Find store folders
    store_folders = []
    folders = user.collection_folders
    for i in range(len(folders)):
        if folders[i].name.find("Store") == 0 :
            store_folders.append(folders[i].id)
    return store_folders
    

def main():
    # Get store folders
    store_folders = getStorefolders()

    # Update Instance Table
    # TODO: move for loop to discogsImport
    for idxSF in range(len(store_folders)):
        discogsImport (store_folders[idxSF])
    
    
    # TODO: get release check update field
    # TODO: get labels flag for create 
    # TODO: get genres flag for create
    # TODO: get artists flag for create
    # TODO: get decades? flag for create
    # TODO: populate catagories
    
    # TODO: releases updated
    
    # TODO: Process Woo
    # TODO: create catagories
    # TODO: create new products
    # TODO: update / reactivate existing products 
    # TODO: deactivate removed products
    # TODO: Sold products Woo -> Discogs

    pp.pprint(getInstanceData('239477059'))
    sys.exit(0)


if __name__ == "__main__":
    main()




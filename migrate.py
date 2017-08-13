#!/usr/bin/env python
# TODO: Create release updated table
# NOTE: May be able to remove columns not_in_store and update_store
# TODO: Convert using custom fields for store designation

from __future__ import print_function
# from datetime import date, datetime, timedelta
import mysql.connector
import discogs_client
# import os
import pprint
import sys
import traceback
import dbqueries as dbq
import hashlib

# Import config
from config import *

pp = pprint.PrettyPrinter(indent=4)

# DB connection setup
importdb = mysql.connector.connect(**dbconfig)
dbcursor = importdb.cursor()
dbcursor_dict = importdb.cursor(dictionary=True)

# Discogs API setup
d = discogs_client.Client(UserAgent, user_token=AuthToken)
user = d.identity()


def main():
    # TODO: Custom field names and and ID
    getcustomfields()

    # TODO: Delete this when done with custom field change
    # Get store folders
    store_folders = getStorefolders()

    # TODO: Delete this when done with custom field change
    # Update Instance Table
    for idxSF in range(len(store_folders)):
        discogsImport(store_folders[idxSF])
    
    # TODO: get release, check update field
    
    getrelease_data(release_id)
    # TODO: get labels / flag for create 
    # TODO: get genres / flag for create
    # TODO: get artists / flag for create
    # TODO: get decades? / flag for create
    # TODO: populate catagories table
    # TODO: Valuations from discogs
    # TODO: releases updated
    
    pp.pprint(getInstanceData('239477059'))
    sys.exit(0)


# Hash instance notes
def hashNotes(instance_notes):
    """
    Sums the concatenated notes field.
    This provides a check for updates
    """
    try:
        notes_chksum = hashlib.md5()
        notes_chksum.update(str(instance_notes).encode())
    except:
        pass
    else:
        return notes_chksum
    finally:
        del notes_chksum


# Get Discogs instance info
# FIXME: change folder id in table on folder change
def discogsImport (store_folder):
    """
    Imports discogs collections to table
    """
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
        db_instances.remove(album.instance_id)

        # Concatenate notes
        hashing_note = None
        for idx in range(len(album.notes)):
            hashing_note = str(hashing_note) + str(album.notes[idx]['field_id']) + str(album.notes[idx]['value'])

        # Hash the notes
        notes_chksum = hashNotes(hashing_note)

        #  Check import table
        try:
            dbcursor_dict.execute(dbq.get_instance_info,  (album.instance_id, ))
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


def getStorefolders():
    # Find store folders
    store_folders = []
    folders = user.collection_folders
    for i in range(len(folders)):
        if folders[i].name.find("Store") == 0 :
            store_folders.append(folders[i].id)
    return store_folders

def getinstancelist():
    """
    Get the list of albums from discogs_instance_import
    """
    dbcursor_dict.execute(dbq.get_instance_list,  )
    db_instance_list = dbcursor_dict.fetchall()
    return db_instance_list

    
if __name__ == "__main__":
    main()


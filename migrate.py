#!/usr/bin/env python
# TODO: Create release updated table
# NOTE: May be able to remove columns not_in_store and update_store
# TODO: Convert using custom fields for store designation

from __future__ import print_function
from datetime import datetime
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
    # Custom field name and ID, populate database
    getcustomfields()

    # Update Instance Table
    discogsImport(discogs_folder)
    
    # TODO: get release information
    # new_releases = get_new_releases()
    #getrelease_data(release_id)

    
    # TODO: get labels / flag for create 
    # TODO: get genres / flag for create
    # TODO: get artists / flag for create
    # TODO: get decades? / flag for create
    # TODO: populate catagories table
    # TODO: Valuations from discogs
    # TODO: releases updated
    # TODO: Move sold to zz Sold folder
    # TODO: Get images
    
    pp.pprint(exec_db_query_get(dbq.get_instance_info, '239477059'))
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
def discogsImport (discogs_folder):
    """
    Imports discogs collections to table
    """
    
    # Set collection
    collection = user.collection_folders

    # Populate import table
    for album in collection[discogs_folder].releases:
        query = None

        # Concatenate notes
        hashing_note = None
        for idx in range(len(album.notes)):
            hashing_note = str(hashing_note) + str(album.notes[idx]['field_id']) + str(album.notes[idx]['value'])

        # Hash the notes
        notes_chksum = hashNotes(hashing_note)

        #  Query instance table for instance
        db_instance = exec_db_query_get(dbq.get_instance_info, album.instance_id)
            
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
                                    'create_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            query = dbq.add_instance

        # Update notes if hash is different
        elif db_instance['instance_id'] == album.instance_id and db_instance['notes_chksum'] != notes_chksum.hexdigest():
            pass
            query_data = {'notes': str(album.notes),
                                     'notes_chksum': notes_chksum.hexdigest(),
                                     'update_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
                                     'instance_id': album.instance_id}
                                     
            query = dbq.update_instance_notes_chksum

        # Update folder id
        elif db_instance['instance_id'] == album.instance_id and db_instance['folder_id'] != album.folder_id:
            pass
            query_data = {'folder_id': album.folder_id,
                                     'update_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
                                     'instance_id': album.instance_id}
                                     
            query = dbq.update_instance_folder_id

        # Execute queries
        exec_db_query(query, query_data)


# Query DB for instance data
def getInstanceData(instance_id):
    dbcursor_dict.execute(dbq.get_instance_info,  (instance_id,))
    instance_data = dbcursor_dict.fetchone()
    return instance_data


# TODO: genre match table
def getGenres():
    pass


def getinstancelist():
    """
    Get the list of albums from discogs_instance_import
    """
    dbcursor_dict.execute(dbq.get_all_instance_list,  )
    db_instance_list = dbcursor_dict.fetchall()
    return db_instance_list

def getcustomfields():
    for idx in range(len(user.collection_fields)):
        query = None

        #  Check field table for field
        db_instance = exec_db_query_get(dbq.get_field, user.collection_fields[idx].id)

        if db_instance == None:
            query = dbq.custom_field_insert
            query_data = {'field_id': user.collection_fields[idx].id,
                                     'field_name': user.collection_fields[idx].name, 
                                     'create_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  }

        elif db_instance['field_name'] != user.collection_fields[idx].name :
            query = dbq.custom_field_update
            query_data = {'field_id': user.collection_fields[idx].id,
                                     'field_name': user.collection_fields[idx].name, 
                                     'update_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S') }
        
        if query != None:
            exec_db_query(query, query_data)

def exec_db_query(query, query_data):
    try:
        dbcursor.execute(query,  query_data )
    except :
        pp.pprint(dbcursor.statement)
        traceback.print_exc(file=sys.stdout)
        importdb.close()
        sys.exit(5)
    else:
        importdb.commit()
        
def exec_db_query_get(query, query_data):
    try:
        dbcursor_dict.execute(query,  (query_data, ))
        return dbcursor_dict.fetchone()
    except :
        pp.pprint(dbcursor.statement)
        traceback.print_exc(file=sys.stdout)
        importdb.close()
        sys.exit(5)


if __name__ == "__main__":
    main()


#!/usr/bin/env python
# TODO: Create release updated table
# TODO: Convert using custom fields for store designation
# TODO: Can I remove the select in the instance loop? Load the instance table into a dict and test against that??? Line 143


from __future__ import print_function
from datetime import datetime

import discogs_client
# import os
import pprint
import sys
# import traceback
import dbqueries as dbq
import hashlib

# Import config
from config import *

pp = pprint.PrettyPrinter(indent=4)


# Discogs API setup
discogs = discogs_client.Client(UserAgent, user_token=AuthToken)
user = discogs.identity()


def main():
    # Custom field name and ID, populate database
    getcustomfields()

    # Update Instance Table
    discogsImport(discogs_folder)
    
    # Process sales channels
    stores = get_stores()
    saleschannels("new", stores)
    saleschannels("update", stores)

    # Populate release information
    discogs_new_releases()
    # TODO:    discogs_update_releases()

    # TODO: get labels / flag for create 

    # TODO: get genres / flag for create attribute
    getattribs("genres")
    
    # TODO: getstyles()
    
    # TODO: get artists / flag for create
    # TODO: get decades? / flag for create
    # TODO: populate catagories table
    # TODO: Valuations from discogs
    # TODO: releases updated
    # TODO: Move sold to zz Sold folder
    # TODO: Get images

    sys.exit(0)

def store_switcher(store_id,  stores):
    switcher = stores
    return switcher.get(store_id, None)

def get_stores():
    stores = {}
    store_fields = dbq.exec_db_query_dict(dbq.get_store_fields,  qty="all")
    for idx in range(len(store_fields)):
        stores[store_fields[idx]['field_id']] = store_fields[idx]['field_name']
    return stores

def saleschannels(type,  stores):
    """
    Type is either new or update
    """
    if type == "new":
        query = dbq.insert_sales_channels
        get_query = dbq.get_new_instance_notes
        date_field = "insert_date"
    elif type == "update":
        query = dbq.update_sales_channels
        get_query = dbq.get_updated_instance_notes
        date_field = "update_date"

    db_instance_notes = dbq.exec_db_query_dict(get_query,  qty="all")
    for inst_idx in range(len(db_instance_notes)):
        channels = {}
        notes = list(eval(db_instance_notes[inst_idx]['notes']))
        for notes_idx in range(len(notes)):
            store = store_switcher(notes[notes_idx]['field_id'],  stores)
            if store != None:
                notes[notes_idx]['value']
                channels[store] = notes[notes_idx]['value']

        query_data = {'instance_id': db_instance_notes[inst_idx]['instance_id'],
                                'sales_channels': str(channels),
                                date_field: datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        dbq.exec_db_query(query, query_data, query_type='insert')

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
# TODO: Fix how artists and labels are stored.
def discogs_new_releases():
    """
    Get/Update release table
    """
    import_new_releases = dbq.exec_db_query(dbq.get_new_release_list, qty='all')
    import_new_releases = [i[0] for i in import_new_releases]

    for index in range(len(import_new_releases)):
        print(import_new_releases[index])
        release = discogs.release(import_new_releases[index])
        release_data = {'release_id': release.id,
                                    'title': release.title,
                                    'artists': str(release.artists),
                                    'labels':str( release.labels),
                                    'styles': str(release.styles),
                                    'genres': str(release.genres),
                                    'url': str(release.url),
                                    'discogs_date_added': release.date_added, 
                                    'discogs_date_changed': release.date_changed, 
                                    'insert_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        dbq.exec_db_query(dbq.import_new_release,  release_data, query_type='insert')

        
def discogs_update_releases():
    """
    Get/Update release table
    """
    import_new_releases = dbq.exec_db_query(dbq.get_new_release_list, qty='all')
    import_new_releases = [i[0] for i in import_new_releases]

    for index in range(len(import_new_releases)):
        print(import_new_releases[index])
        release = discogs.release(import_new_releases[index])
        release_data = {'release_id': release.id,
                                    'title': release.title,
                                    'artists': str(release.artists),
                                    'labels':str( release.labels),
                                    'styles': str(release.styles),
                                    'genres': str(release.genres),
                                    'url': str(release.url),
                                    'discogs_date_added': release.date_added, 
                                    'discogs_date_changed': release.date_changed, 
                                    'insert_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        dbq.exec_db_query(dbq.import_update_release,  release_data, query_type='insert')

# Get Discogs instance info
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
        if album.notes != None:
            for idx in range(len(album.notes)):
                hashing_note = str(hashing_note) + str(album.notes[idx]['field_id']) + str(album.notes[idx]['value'])

        # Hash the notes
        notes_chksum = hashNotes(hashing_note)

        #  Query instance table for instance
        db_instance = dbq.exec_db_query_dict(dbq.get_instance_info, album.instance_id)

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
                                    'insert_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
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
        if query != None:
            dbq.exec_db_query(query, query_data, query_type='insert')


# Query DB for instance data
def getInstanceData(instance_id):
    dbcursor_dict.execute(dbq.get_instance_info,  (instance_id,))
    instance_data = dbcursor_dict.fetchone()
    return instance_data


# TODO: This is not working for labels and artists. The formating is wrong on the db data
def getattribs(attrib_name):
    query_data = []
    query = dbq.get_discogs_attribs.format(attrib_name)
    dbattribs = dbq.exec_db_query(query,  qty='all')

    for idx1 in range(len(dbattribs)):
        row = eval(dbattribs[idx1][0])
        for idx2 in range(len(row)):
            query_data.append(row[idx2])

    query_data = list(zip(set(query_data)))
    insert_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query_data = [ (attrib_name,) + xs + (insert_date,) for xs in query_data]
    query = dbq.insert_attribs_tmp
    dbq.exec_db_query(query, query_data, query_type="insert", query_many="yes")

    # insert new genres
    dbq.exec_db_query(dbq.update_attribs)

    # Truncate temp table
    dbq.exec_db_query(dbq.truncate_attribs_tmp)

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
        db_instance = dbq.exec_db_query_dict(dbq.get_field, user.collection_fields[idx].id)

        if db_instance == None:
            query = dbq.custom_field_insert
            query_data = {'field_id': user.collection_fields[idx].id,
                                     'field_name': user.collection_fields[idx].name, 
                                     'insert_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  }

        elif db_instance['field_name'] != user.collection_fields[idx].name :
            query = dbq.custom_field_update
            query_data = {'field_id': user.collection_fields[idx].id,
                                     'field_name': user.collection_fields[idx].name, 
                                     'update_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S') }

        if query != None:
            dbq.exec_db_query(query, query_data, query_type='insert')



if __name__ == "__main__":
    main()


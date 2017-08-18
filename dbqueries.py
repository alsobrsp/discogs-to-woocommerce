#!/usr/bin/env python
import pprint
import sys
import traceback
import mysql.connector
from config import *

pp = pprint.PrettyPrinter(indent=4)

# DB connection setup
importdb = mysql.connector.connect(**dbconfig)
dbcursor = importdb.cursor()
dbcursor_dict = importdb.cursor(dictionary=True)

def exec_db_query(query, query_data=None, qty="one",  query_type="select",  query_many="no"):
    try:
        if query_data == None and query_many == "no":
            dbcursor.execute(query)
        elif query_many == "no":
            dbcursor.execute(query,  query_data )
        elif query_type == "insert" and query_many == "yes":
            dbcursor.executemany(query,  query_data )
        
        
        if query_type == 'select':
            if qty == 'one':
                return dbcursor.fetchone()
            elif qty== 'all':
                return dbcursor.fetchall()
        

    except :
        pp.pprint(dbcursor.statement)
        traceback.print_exc(file=sys.stdout)
        importdb.close()
        sys.exit(5)
    else:
        importdb.commit()

def exec_db_query_dict(query, query_data=None,  qty="one"):
    try:
        if query_data == None:
            dbcursor_dict.execute(query)
        else:
            dbcursor_dict.execute(query,  (query_data, ))

        if qty == 'one':
            return dbcursor_dict.fetchone()
        elif qty== 'all':
            return dbcursor_dict.fetchall()

    except :
        pp.pprint(dbcursor.statement)
        traceback.print_exc(file=sys.stdout)
        importdb.close()
        sys.exit(5)

    else:
        importdb.commit()

# Add instance 
add_instance = ('INSERT INTO dov_discogs_instances '
                           '(instance_id, rating, title, folder_id, discogs_date_added, notes, notes_chksum, release_id, insert_date) '
                           'VALUES (%(instance_id)s, %(rating)s, %(title)s, %(folder_id)s, %(discogs_date_added)s, %(notes)s, %(notes_chksum)s, %(release_id)s, %(insert_date)s)')

update_instance_woo_id = ('UPDATE dov_discogs_instances '
                                            'SET woo_id = %(woo_id)s '
                                            'WHERE instance_id = %(instance_id)s')
                                            
get_all_instance_list = ('select * from dov_discogs_instances')
get_instance_info = ('select * from dov_discogs_instances WHERE instance_id = %s')

update_instance_notes_chksum = ('UPDATE dov_discogs_instances '
                                                        'SET notes = %(notes)s, '
                                                        'notes_chksum = %(notes_chksum)s, '
                                                        'update_date = %(update_date)s '
                                                        'WHERE instance_id = %(instance_id)s')
                                                        

update_instance_folder_id = ('UPDATE dov_discogs_instances '
                                                        'SET folder_id = %(folder_id)s, '
                                                        'update_date = %(update_date)s '
                                                        'WHERE instance_id = %(instance_id)s')

# Get field
get_field = ('select * from dov_discogs_fields WHERE field_id = %s')

# Get field list
get_field_list = ('select * from dov_discogs_fields')

# Insert custom fields to db
custom_field_insert = ('INSERT INTO dov_discogs_fields '
                                     '(field_id, field_name, insert_date) '
                                     'VALUES (%(field_id)s, %(field_name)s, %(insert_date)s)')

# Update custom fields in db
custom_field_update = ('UPDATE dov_discogs_fields '
                                      'SET field_name = %(field_name)s, '
                                      'update_date = %(update_date)s '
                                      'WHERE field_id = %(field_id)s')

# This is all releases that are now in the instance table but not in releases
get_new_release_list = ('select DISTINCT release_id from dov_discogs_instances where '
                                       'NOT EXISTS ( select release_id from dov_discogs_releases '
                                       'where dov_discogs_releases.release_id = dov_discogs_instances.release_id)')
                                       
import_new_release = ('INSERT INTO dov_discogs_releases '
                                     '(release_id, title, artists, labels, styles, genres, url, discogs_date_added, discogs_date_changed, insert_date) '
                                     'VALUES '
                                     '(%(release_id)s, %(title)s, %(artists)s, %(labels)s, %(styles)s, %(genres)s, %(url)s, %(discogs_date_added)s, %(discogs_date_changed)s, %(insert_date)s)')

# Genres
get_release_genres = ('select genres from dov_discogs_releases')
insert_genres_tmp = ('insert into dov_discogs_genres_tmp (genre) values (%s)')
update_genres = ('INSERT INTO dov_discogs_genres (genre) '
                              'SELECT DISTINCT genre '
                              'FROM dov_discogs_genres_tmp '
                              'WHERE NOT EXISTS( SELECT genre '
                              '      FROM dov_discogs_genres '
                              '      WHERE dov_discogs_genres.genre = dov_discogs_genres_tmp.genre)')

truncate_genres_tmp = ('TRUNCATE dov_discogs_genres_tmp')

# Sales Channels
get_store_fields = ('select field_id,field_name from dov_discogs_fields where field_name like "Sell%"')

get_new_instance_notes = ('SELECT DISTINCT instance_id, notes '
                                            'FROM  dov_discogs_instances '
                                            'WHERE notes != "None" and '
                                            '    NOT EXISTS( SELECT instance_id '
                                            '        FROM dov_sales_channel '
                                            '        WHERE dov_sales_channel.instance_id = dov_discogs_instances.instance_id);')

insert_sales_channels = ('INSERT INTO dov_sales_channel '
                                        '(instance_id, sales_channels, insert_date) '
                                        'VALUES '
                                        '(%(instance_id)s, %(sales_channels)s, %(insert_date)s)')

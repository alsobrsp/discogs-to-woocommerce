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

get_release_info = ('select * from dov_discogs_releases WHERE release_id = %s')

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
get_discogs_attribs = ('select {0} from dov_discogs_releases')

insert_attribs_tmp = ('insert into dov_woo_attribs_tmp (attrib_name, attrib_term, insert_date) values (%s, %s, %s)')

update_attribs = ('INSERT INTO dov_woo_attribs (attrib_name, attrib_term, insert_date) '
                              'SELECT DISTINCT attrib_name, attrib_term, insert_date '
                              'FROM dov_woo_attribs_tmp '
                              'WHERE NOT EXISTS( SELECT attrib_name, attrib_term '
                              '      FROM dov_woo_attribs '
                              '      WHERE dov_woo_attribs.attrib_name = dov_woo_attribs_tmp.attrib_name '
                              '        and dov_woo_attribs.attrib_term = dov_woo_attribs_tmp.attrib_term)')

truncate_attribs_tmp = ('TRUNCATE dov_woo_attribs_tmp')

woo_get_new_attribs = ('select id, attrib_term from dov_woo_attribs where attrib_name = %s and woo_attrib_id is Null')

update_attribs_woo_id = ('update dov_woo_attribs '
                                         'SET woo_attrib_id = %(woo_attrib_id)s, '
                                         'update_date = %(update_date)s '
                                         'WHERE id = %(id)s')

# Sales Channels
get_store_fields = ('select field_id,field_name from dov_discogs_fields where field_name like "Sell%"')

get_new_instance_notes = ('SELECT DISTINCT instance_id, notes '
                                            'FROM  dov_discogs_instances '
                                            'WHERE notes != "None" and '
                                            '    NOT EXISTS( SELECT instance_id '
                                            '        FROM dov_sales_channels '
                                            '        WHERE dov_sales_channels.instance_id = dov_discogs_instances.instance_id);')

insert_sales_channels = ('INSERT INTO dov_sales_channels '
                                        '(instance_id, sales_channels, insert_date) '
                                        'VALUES '
                                        '(%(instance_id)s, %(sales_channels)s, %(insert_date)s)')
                                        
get_updated_instance_notes = ('SELECT DISTINCT instance_id, notes '
                                                   'FROM dov_discogs_instances '
                                                   'WHERE notes != "None" '
                                                   '       AND EXISTS( SELECT instance_id '
                                                   '       FROM dov_sales_channels '
                                                   '       WHERE dov_sales_channels.instance_id = dov_discogs_instances.instance_id '
                                                   '               and dov_sales_channels.update_date < dov_discogs_instances.update_date);')

update_sales_channels = ('UPDATE dov_sales_channels '
                                          'SET sales_channels = %(sales_channels)s, '
                                          'update_date = %(update_date)s '
                                          'where instance_id = %(instance_id)s')
                                        

# Woo queries
get_new_woo_instances = ('SELECT A.instance_id, B.sales_channels '
                                            'FROM dov_discogs_instances A  '
                                            'INNER JOIN dov_sales_channels B ON A.instance_id = B.instance_id '
                                            'where A.woo_id is Null and ( B.sales_channels like "%DoV\': \'List%" or B.sales_channels like "%DoV\': \'Yes%")')

#!/usr/bin/env python

# Add instance 
add_instance = ('INSERT INTO discogs_instance_import '
                           '(instance_id, rating, title, folder_id, discogs_date_added, notes, notes_chksum, release_id, in_store, update_store) '
                           'VALUES (%(instance_id)s, %(rating)s, %(title)s, %(folder_id)s, %(discogs_date_added)s, %(notes)s, %(notes_chksum)s, %(release_id)s), %(in_store)s, %(update_store)s')

# Check if instance is in DB

update_instance_woo_id = ('UPDATE discogs_instance_import '
                                            'SET woo_id = %(woo_id)s '
                                            'WHERE instance_id = %(instance_id)s')
                                            
get_instance_info = ('select * from discogs_instance_import WHERE instance_id = %s')

get_instance_id_list = ('select instance_id from discogs_instance_import WHERE folder_id = %s')

update_instance_notes_chksum = ('UPDATE discogs_instance_import '
                                                        'SET notes = %(notes)s, '
                                                        'notes_chksum = %(notes_chksum)s, '
                                                        'update_store = %(update_store)s, '
                                                        'in_store = %(in_store)s '
                                                        'WHERE instance_id = %(instance_id)s')
                                                        
clear_in_store_flag = ('UPDATE discogs_instance_import '
                                    'SET in_store = FALSE ')

still_in_store = ('UPDATE discogs_instance_import '
                                     'SET in_store = TRUE, '
                                     'not_in_store = FALSE '
                                     'WHERE instance_id = %(instance_id)s')
                                     
return_in_store = ('UPDATE discogs_instance_import '
                                     'SET in_store = TRUE, '
                                     'not_in_store = FALSE '
                                     'WHERE instance_id = %(instance_id)s')

get_instance_list = ('select * from discogs_instance_import')

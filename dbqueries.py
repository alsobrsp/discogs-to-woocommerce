#!/usr/bin/env python

# Add instance 
add_instance = ('INSERT INTO dov_discogs_instances '
                           '(instance_id, rating, title, folder_id, discogs_date_added, notes, notes_chksum, release_id, in_store, update_store) '
                           'VALUES (%(instance_id)s, %(rating)s, %(title)s, %(folder_id)s, %(discogs_date_added)s, %(notes)s, %(notes_chksum)s, %(release_id)s), %(in_store)s, %(update_store)s')

update_instance_woo_id = ('UPDATE dov_discogs_instances '
                                            'SET woo_id = %(woo_id)s '
                                            'WHERE instance_id = %(instance_id)s')
                                            
get_instance_info = ('select * from dov_discogs_instances WHERE instance_id = %s')

update_instance_notes_chksum = ('UPDATE dov_discogs_instances '
                                                        'SET notes = %(notes)s, '
                                                        'notes_chksum = %(notes_chksum)s, '
                                                        'update_store = %(update_store)s, '
                                                        'in_store = %(in_store)s '
                                                        'WHERE instance_id = %(instance_id)s')
                                                        
clear_in_store_flag = ('UPDATE dov_discogs_instances '
                                    'SET in_store = FALSE ')

still_in_store = ('UPDATE dov_discogs_instances '
                                     'SET in_store = TRUE, '
                                     'not_in_store = FALSE '
                                     'WHERE instance_id = %(instance_id)s')
                                     
return_in_store = ('UPDATE dov_discogs_instances '
                                     'SET in_store = TRUE, '
                                     'not_in_store = FALSE '
                                     'WHERE instance_id = %(instance_id)s')

get_all_instance_list = ('select * from dov_discogs_instances')

# Get field list
get_field = ('select * from dov_discogs_fields WHERE field_id = %s')

# Insert custom fields to db
custom_field_insert = ('INSERT INTO dov_discogs_fields '
                                     '(field_id, field_name) '
                                     'VALUES (%(field_id)s, %(field_name)s)')

# Update custom fields in db
custom_field_update = ('UPDATE dov_discogs_fields '
                                      'SET field_name = %(field_name)s '
                                      'WHERE field_id = %(field_id)s')

#!/usr/bin/env python

# Add instance 
add_instance = ('INSERT INTO dov_discogs_instances '
                           '(instance_id, rating, title, folder_id, discogs_date_added, notes, notes_chksum, release_id, create_date) '
                           'VALUES (%(instance_id)s, %(rating)s, %(title)s, %(folder_id)s, %(discogs_date_added)s, %(notes)s, %(notes_chksum)s, %(release_id)s, %(create_date)s)')

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
                                     '(field_id, field_name, create_date) '
                                     'VALUES (%(field_id)s, %(field_name)s, %(create_date)s)')

# Update custom fields in db
custom_field_update = ('UPDATE dov_discogs_fields '
                                      'SET field_name = %(field_name)s, '
                                      'update_date = %(update_date)s '
                                      'WHERE field_id = %(field_id)s')

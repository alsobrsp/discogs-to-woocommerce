#!/usr/bin/env python

# Add instance 
add_instance = ('INSERT INTO discogs_instance_import '
                           '(instance_id, rating, title, folder_id, discogs_date_added, notes, notes_chksum, release_id) '
                           'VALUES (%(instance_id)s, %(rating)s, %(title)s, %(folder_id)s, %(discogs_date_added)s, %(notes)s, %(notes_chksum)s, %(release_id)s)')

# Check if instance is in DB
check_instance = ("SELECT instance_id,notes_chksum FROM discogs_instance_import WHERE instance_id = %s")

update_instance_woo_id = ('UPDATE discogs_instance_import '
                                            'SET woo_id = %(woo_id)s '
                                            'WHERE instance_id = %(instance_id)s')
                                            
get_instance_info = ('select * from discogs_instance_import WHERE instance_id = %s')

update_instance_notes_chksum = ('UPDATE discogs_instance_import '
                                                        'SET notes = %(notes)s, '
                                                        'notes_chksum = %(notes_chksum)s'
                                                        'WHERE instance_id = %(instance_id)s')

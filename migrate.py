#!/usr/bin/env python
# TODO: Pull folders to table
# TODO: Pull cool discogs_client commits from other forks

from __future__ import print_function
#from datetime import date, datetime, timedelta
import mysql.connector
import discogs_client
import os
import pprint
from woocommerce import API
import sys
import traceback

pp = pprint.PrettyPrinter(indent=4)

# DB connection setup
importdb = mysql.connector.connect(user='alsobrsp', password='spanky5', host='db.seasies.com', database='webuser_decadesofvinyl.com')
dbcursor = importdb.cursor()
add_instance = ('INSERT INTO discogs_instance_import '
                           '(instance_id, rating, title, folder_id, discogs_date_added, notes, release_id) '
                           'VALUES (%(instance_id)s, %(rating)s, %(title)s, %(folder_id)s, %(discogs_date_added)s, %(notes)s, %(release_id)s)')

check_instance = ("SELECT instance_id FROM discogs_instance_import WHERE instance_id = %s")

# WooCommerce API setup
wcapi = API(
    url="https://www.decadesofvinyl.com",
    consumer_key="ck_f839dfe156f0253a7b4a7cd810a40de86d1b1519",
    consumer_secret="cs_220b8c6746a0733df9c73c656ef699db8baaceca",
    wp_api=True,
    version="wc/v2"
)

# Discogs API setup
UserAgent = 'DoV/0.1'
AuthToken = "DiSiupFPDVYxsOqpOtwjXmfENbNeLNfhhaCYqbso"
d = discogs_client.Client(UserAgent, user_token=AuthToken)
user = d.identity()
collection = user.collection_folders 



for album in collection[0].releases:
   #  Check import table
   dbcursor.execute(check_instance,  (album.instance_id, ))
   db_instance_id = dbcursor.fetchone()
   if db_instance_id == None:
        insert_data = {'instance_id': album.instance_id,
                        'rating': album.rating,
                        'title': album.release.title,
                        'folder_id': album.folder_id,
                        'discogs_date_added':  album.date_added,
                        'notes': str(album.notes),
                        'release_id': album.id}
        try:
            dbcursor.execute(add_instance,  insert_data )
        except :
            pp.pprint(dbcursor.statement)
            traceback.print_exc(file=sys.stdout)
            os._exit(0)
        importdb.commit()
#        pp.pprint(insert_data)
#        os._exit(0)







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
    
    # Insert into 
    
#    print("Instance Id: ", album.instance_id)
#  print("Release Id: ", album.id)
#  print("Our Rating: ", album.rating)
#  print("Our Notes:")
#  pp.pprint(album.notes)
#  release = d.release(album.id)
#  pp.pprint(release.labels)
#  


#



os._exit(0)

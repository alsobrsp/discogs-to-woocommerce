#!/usr/bin/env python
# TODO: Instances that are no longer in a store folder should be deactivated in the store

from __future__ import print_function
from datetime import datetime
import discogs_client
# import os
import pprint
import sys
import dbqueries as dbq
# import hashlib
from woocommerce import API

# Import config
from config import *

pp = pprint.PrettyPrinter(indent=4)

# WooCommerce API setup
wcapi = API(**wooconfig)

# Discogs API setup
discogs = discogs_client.Client(UserAgent, user_token=AuthToken)
user = discogs.identity()

def main():
    # TODO: Process Woo
    # Get woo attributes, name to id mapping
    woo_attributes_list = get_woo_attributes_list()
    # TODO: Genres to attributes
    update_attrib_term_list('genre', woo_attributes_list['Genre'])

    # TODO: create catagories
    
    # TODO: create new products
#    db_new_products = dbq.exec_db_query_dict(dbq.get_new_woo_instances,  qty="all")
#    create_new_products(db_new_products)
    # TODO: update / reactivate existing products 
    # TODO: deactivate removed products
    # TODO: Sold products Woo -> Discogs
    sys.exit(0)


# TODO: Update woo_id
# Probably need two functions
def updateInstanceWoo(instance_id):
    pass

# TODO: updates based on instance notes, release update, in store status
def updateWooProduct(instance_id):
    pass

# Create Product
def create_new_products (db_new_products):
    """
    Take list of new instance id's, create product page and update instance table with Woo ID
    """
    for idx in range(len(db_new_products)):
        # Get instance data from db
        instance_data = dbq.exec_db_query_dict(dbq.get_instance_info,  db_new_products[idx]['instance_id'])
        # Get release data from db
        release_data = dbq.exec_db_query_dict(dbq.get_release_info, instance_data['release_id'])
        
        pp.pprint(instance_data)
        pp.pprint(release_data)
        
        
    
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
    
def formatproduct():
    pass
    
def get_woo_attributes_list():
    woo_attributes_list = {}
    attributes = wcapi.get("products/attributes").json()
    for idx in range(len(attributes)):
        woo_attributes_list[attributes[idx]['name']] = attributes[idx]['id']
    return woo_attributes_list

def update_attrib_term_list(attrib_name,  attrib_id):
    """
    Passed the Woo attribute type and woo id, query attribute table for new terms and populate Woo
    """
    query_data = attrib_name
    query = dbq.woo_get_new_attribs
    new_terms = dbq.exec_db_query_dict(query, query_data, qty="all")
    for idx in range(len(new_terms)):
        data = {"name": new_terms[idx]['attrib_term']}
        created = wcapi.post("products/attributes/" + str(attrib_id) + "/terms", data).json()
        query_data = {'woo_attrib_id': created["id"], 
                                'update_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'id':  new_terms[idx]['id'] }
        query = dbq.update_attribs_woo_id
        dbq.exec_db_query(query, query_data, query_type='insert')
    
    
    
if __name__ == "__main__":
    main()


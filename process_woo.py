#!/usr/bin/env python
# TODO: Instances that are no longer in a store folder should be deactivated in the store

from __future__ import print_function
#from datetime import datetime
import discogs_client
# import os
import pprint
import sys
import dbqueries as dbq
# import hashlib

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
    # TODO: create catagories
    # TODO: create new products
    create_product()
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
def createWooProduct (instance_id):
    pass
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
    


if __name__ == "__main__":
    main()


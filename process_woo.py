#!/usr/bin/env python
# TODO: Instances that are no longer in a store folder should be deactivated in the store


from woocommerce import API

# Import config
from config import *

# WooCommerce API setup
wcapi = API(
    wooUrl,
    wooConsumer_key,
    wooConsumer_secret,
    wooWP_api,
    wooVersion
)


def main():
    # TODO: Process Woo
    # TODO: create catagories
    # TODO: create new products
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


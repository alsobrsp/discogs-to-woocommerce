#!/usr/bin/env python
# TODO: Instances that are no longer in a store folder should be deactivated in the store

from __future__ import print_function
from datetime import datetime
import discogs_client
#from collections import defaultdict
# import os
import pprint
import sys
import dbqueries as dbq
import dblog
# import hashlib
from woocommerce import API
import htmlgen
from utilities import *
import urllib3

# Import config
from config import *

pp = pprint.PrettyPrinter(indent=4)

# WooCommerce API setup
wcapi = API(**wooconfig)

# Discogs API setup
discogs = discogs_client.Client(UserAgent, user_token=AuthToken)
user = discogs.identity()

process_name = "process woo"

def process_woo():
    check_db_version()
    run_id = dblog.startup(process_name)

    """ TODO: Remove this section
    Attribute terms can be created on the fly and will match existing
    
    # Manually create attribute name
    # Get woo attributes, name to id mapping
    woo_attributes_list = get_woo_attributes_list()
    # Genres to attribute terms
    update_attrib_term_list('genres', woo_attributes_list['Genres'])
    # Styles to attribute terms
    update_attrib_term_list('styles', woo_attributes_list['Styles'])
    """
    # Get category ids
    global categories
    categories = get_woo_categories()
    
    # Get attrib id dict.
    global attrib_ids
    attrib_ids = get_attrib_ids()

    # create new products
    db_new_products = dbq.exec_db_query_dict(dbq.get_new_woo_instances,  qty="all")
    process_products("new",  db_new_products)
    
    # Update existing products
    db_update_products = dbq.exec_db_query_dict(dbq.get_update_woo_instances,  qty="all")
    process_products("update", db_update_products)
    
    # TODO: group multiple products? SELECT release_id, title, COUNT(*) copies FROM dov_discogs_instances GROUP BY release_id HAVING copies > 1;
    # TODO: Calculate and set pricing
    # TODO: update / reactivate existing products 
    # TODO: Cross/Up sell items
    # TODO: Group items
    # TODO: deactivate removed products
    # TODO: Sold products Woo -> Discogs
    dblog.finished(run_id)

# Get category ids
def get_woo_categories():
    categories = {}
    woo_categories = wcapi.get("products/categories").json()
    for idx in range(len(woo_categories)):
        categories[woo_categories[idx]['name']] = woo_categories[idx]['id']
    return categories

# Attribute id list
def get_attrib_ids():
    attrib_ids = {}
    attrib_list = wcapi.get("products/attributes").json()
    for idx in range(len(attrib_list)):
        attrib_ids[attrib_list[idx]['name']] = attrib_list[idx]['id']
    return attrib_ids


# TODO: Update woo_id
# Probably need two functions
def updateInstanceWoo(instance_id):
    pass

# TODO: updates based on instance notes, release update, in store status
def updateWooProduct(instance_id):
    pass

# Create Product
def process_products(type,  db_products):
    """
    Take list of new instance id's, create product page and update instance table with Woo ID
    """
    if type == "new":
        query = dbq.insert_woo_instance_product
        date_field = "insert_date"
    elif type == "update":
        query = dbq.update_woo_instance_product
        date_field = "update_date"
    
    for idx in range(len(db_products)):
        # Get instance data from db
        instance_data = dbq.exec_db_query_dict(dbq.get_instance_info,  db_products[idx]['instance_id'])
        dov_sales_status = eval(dbq.exec_db_query_dict(dbq.get_sales_channels,  db_products[idx]['instance_id'])['sales_channels'])['Sell on DoV']
       

        # Get release data from Discogs
        # release_data = dbq.exec_db_query_dict(dbq.get_release_info, instance_data['release_id'])
        release_data = discogs.release(db_products[idx]['release_id'])

        # Send data to formater
        product_data = formatproduct(instance_data, release_data, dov_sales_status,  type)

        # Create Woo Product
        if type == "new":
            product_endpoint = "products"
        elif type == "update":
            product_endpoint = ("products/" + str(db_products[idx]['woo_id']))
        
        try:
            woo_product = wcapi.post(product_endpoint, product_data).json()
        except:
            print("Instance ID: " + str(db_products[idx]['instance_id']) + " threw an error during a " + type + " product operation talking to Woo. ")
            continue
        
        # Update DB with Woo Product ID
        query_data = {"woo_id":  woo_product['id'], 
                            "instance_id": db_products[idx]['instance_id'], 
                            date_field: datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        dbq.exec_db_query(query, query_data, query_type='insert')

def format_generic(object):
    """
    Works for artists, companies, credits, labels
    """
    html_string = ""
    for idx in range(len(object)):
#        if object[idx].id == 0 or object[idx].id == 194 :
#            html_string += object[idx].name
#        else:
        try:
            object_url = object[idx].url
        except discogs_client.exceptions.HTTPError:
            html_string += object[idx].name
        else:
            html_string += str(htmlgen.Link(object_url,  object[idx].name))

        if 'catno' in dir(object[idx]):
            html_string += ': {0}\n'.format(object[idx].catno)
        else:
            html_string += "\n"
    return html_string
    
def format_formats(object):
    string = ""
    for idx in range(len(object)):
        string += object[idx]['name']
        if 'descriptions' in object[idx]:
            string += (", " + ', '.join(object[idx]['descriptions']) + "\n")
        else:
            string += "\n"
    return string
    
def format_identifiers(object):
    string = ""
    for idx in range(len(object)):
        type = object[idx]['type']
        string += '{0} '.format(type)
        if 'description' in object[idx]:
            desc = object[idx]['description']
            string += '({0})'.format(desc)
        if 'value' in object[idx]:
            value = object[idx]['value']
            string += ': {0}\n'.format(value)
    return string

def format_image_array(object):
    images = []
    if object != None:
        for idx in range(len(object)):
            images.append({"src": object[idx]['uri'], "position": idx})
    return images

def format_instance_notes(object):
    notes = ""
    object = eval(object)
    for idx in range(len(object)):
        if object[idx]['field_id'] == 1:
            notes += "Media Condition: {0}\n".format(object[idx]['value'])
        if object[idx]['field_id'] == 2:
            notes += "Sleeve Condition: {0}\n".format(object[idx]['value'])
        if object[idx]['field_id'] == 3:
            notes += "Decades of Vinyl Notes\n{0}\n".format(object[idx]['value'])
    return notes
    
def format_atttributes(object,  attrib):
    attrib_id = attrib_ids[attrib]
    attribute = {'id': attrib_id, 'options': object}
    return attribute

def format_pricing(notes,  suggestions):
    pricing = {'regular': "", 'sale': ""}
    notes = eval(notes)
    media_cond = ""

    # Get media condition
    for idx in range(len(notes)):
        if notes[idx]['field_id'] == 1:
            media_cond = notes[idx]['value']

    if suggestions and media_cond != "":
        # Regular pricing is just the media condition.
        pricing['regular'] = format(round(suggestions[media_cond]['value'], 2))
        if float(pricing['regular']) <= 1:
            pricing['regular'] = str(2)
        
        # Sale price is a 10% discount
        pricing['sale'] = format(round(float(pricing['regular'])*.90, 2))

    return pricing


def formatproduct(instance_data, release_data, dov_sales_status, type="new"):
    """
    This will take the instance, release, artist, and label data to build the product page
    TODO: Will need an object processor function, there are a number of array/object lists.
    """

    # Artists list
    artists = format_generic(release_data.artists)
    # Company list
    companies = format_generic(release_data.companies)
    # Extra Artists / Credits
    credits = format_generic(release_data.credits)
    #  TODO: move Formats to attibutes    
    formats = format_formats(release_data.formats)
    # Identifiers - barcodes, runouts and such
    identifiers = format_identifiers(release_data.identifiers)
    # Labels
    labels = format_generic(release_data.labels)
    # TODO: some traks have extraartists in credits
#    tracklist = release_data.tracklist
    # Discogs release URL
    url = str(htmlgen.Link(release_data.url,  release_data.artists[0].name + " - " + release_data.title))
    # TODO: Embed videos
#    videos = release_data.videos

    short_description = format_instance_notes(instance_data['notes'])

    description = ("This is a first pass on the data import. The format will improve.\n"
                            "Artists\n" + artists + "\n"
                            "Country of Release: " + str(release_data.country) + "\n"
                            "Companies\n" + companies + "\n"
                            "Credits\n" + credits + "\n"
                            "Formats\n" + formats + "\n"
                            "Identifiers\n" + identifiers + "\n"
                            "Labels\n" + labels + "\n"
                            "Release Date: " + str(release_data.released) + "\n"
#                            "Tracklist\n" + tracklist + "\n"
                            "Discogs URL: " + url + "\n"
#                            "Videos\n" + videos + "\n"
                            "Year: " + str(release_data.year) + "\n"
                            "\n"
                            "Discogs release notes:\n" + str(release_data.notes) + "\n"
                            "**************\n"
                            "All data and photos unless otherwise noted are from Discogs"
                            )

    # Genres
    genres = format_atttributes(release_data.genres,  'Genres')
    # Styles
    styles = format_atttributes(release_data.styles,  'Styles')
    attributes = [genres,  styles]
    
    price = format_pricing(instance_data['notes'], release_data.price_suggestions)
    
    data = {"name": release_data.artists[0].name + " - " + release_data.title, 
                  "description": description, 
                  "short_description": short_description, 
                  "sku": str(instance_data['instance_id']), 
                  "attributes": attributes, 
                  "regular_price": price['regular'], 
                  "sale_price": price['sale']}

    if dov_sales_status == "List Only":
        MESSAGE_STR = ('Artist: ' +   release_data.artists[0].name + ' / Album: ' + release_data.title + ' / SKU: ' + str(instance_data['instance_id']))
        URLOPTS = {'your-subject': 'Pruduct Inquiry',
                             'your-message':  MESSAGE_STR}
        external_url=(CONTACTURL + urllib3.request.urlencode(URLOPTS))
        
        # TODO: Not for sale catagory
        data.update({"categories": [{"id": categories[LIST_ONLY_CAT]}]})
        
        data.update({"external_url": external_url,
                               "button_text": "Pruduct Inquiry", 
                               "type": 'external'})

    if dov_sales_status == "Yes":
        # TODO: For sale catagory
        data.update({"categories": [{"id": categories[FOR_SALE_CAT]}]})
        data.update({"type": 'simple'})

    if type == "new":
        images = format_image_array(release_data.images)
        data.update({"images": images})
    '''
    name	string	Product name.
    slug	string	Product slug.
    type	string	Product type. Options: simple, grouped, external and variable. Default is simple.
    status	string	Product status (post status). Options: draft, pending, private and publish. Default is publish.
    featured	boolean	Featured product. Default is false.
    catalog_visibility	string	Catalog visibility. Options: visible, catalog, search and hidden. Default is visible.
    description	string	Product description.
    short_description	string	Product short description.
    sku	string	Unique identifier.
    regular_price	string	Product regular price.
    sale_price	string	Product sale price.
    date_on_sale_from	date-time	Start date of sale price, in the site’s timezone.
    date_on_sale_from_gmt	date-time	Start date of sale price, as GMT.
    date_on_sale_to	date-time	End date of sale price, in the site’s timezone.
    date_on_sale_to_gmt	date-time	End date of sale price, in the site’s timezone.
    external_url	string	Product external URL. Only for external products.
    button_text	string	Product external button text. Only for external products.
    tax_status	string	Tax status. Options: taxable, shipping and none. Default is taxable.
    tax_class	string	Tax class.
    manage_stock	boolean	Stock management at product level. Default is false.
    stock_quantity	integer	Stock quantity.
    in_stock	boolean	Controls whether or not the product is listed as “in stock” or “out of stock” on the frontend. Default is true.
    backorders	string	If managing stock, this controls if backorders are allowed. Options: no, notify and yes. Default is no.
    sold_individually	boolean	Allow one item to be bought in a single order. Default is false.
    weight	string	Product weight.
    dimensions	object	Product dimensions. See Product - Dimensions properties
    shipping_class	string	Shipping class slug.
    reviews_allowed	boolean	Allow reviews. Default is true.
    upsell_ids	array	List of up-sell products IDs.
    cross_sell_ids	array	List of cross-sell products IDs.
    parent_id	integer	Product parent ID.
    purchase_note	string	Optional note to send the customer after purchase.
    categories	array	List of categories. See Product - Categories properties
    tags	array	List of tags. See Product - Tags properties
    images	object	List of images. See Product - Images properties
    attributes	array	List of attributes. See Product - Attributes properties
    default_attributes	array	Defaults variation attributes. See Product - Default attributes properties
    menu_order	integer	Menu order, used to custom sort products.
    meta_data	array	Meta data. See Product - Meta data properties
    '''
    
    return data
    
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
    process_woo()
    sys.exit(0)


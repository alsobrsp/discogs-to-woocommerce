db_version=1.1

# DB connection setup
dbconfig = {'user': 'alsobrsp', 
                'password': 'spanky5', 
                'host': 'db.seasies.com', 
                'database': 'webuser_decadesofvinyl.com'
                }


# WooCommerce API setup
wooconfig = {'url': "https://www.decadesofvinyl.com",
                        'consumer_key': "ck_f839dfe156f0253a7b4a7cd810a40de86d1b1519",
                        'consumer_secret': "cs_220b8c6746a0733df9c73c656ef699db8baaceca",
                        'wp_api': True,
                        'version': "wc/v2", 
                        'timeout': 20
                        }

# Discogs API setup
UserAgent = 'DoV/0.1 +https://www.decadesofvinyl.com'
AuthToken = "DiSiupFPDVYxsOqpOtwjXmfENbNeLNfhhaCYqbso"

# NOTE: This is the index not the id. folder 0 for ALL, 26 for 7up test
discogs_folder=0


# Value map
condition_values = {"Mint (M)": 7,
                                 "Near Mint (NM or M-)": 6,
                                 "Very Good Plus (VG+)": 5,
                                 "Very Good (VG)": 4,
                                 "Good Plus (G+)": 3,
                                 "Good (G)": 2,
                                 "Fair (F)": 1,
                                 "Poor (P)": 0}

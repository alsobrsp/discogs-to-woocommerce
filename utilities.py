#!/usr/bin/env python
import dbqueries as dbq
import sys
from config import *



def check_db_version():
    try:
        test = dbq.exec_db_query_dict(dbq.get_db_version,  db_version)
    except NameError:
        print ('Check your config.py file for db_version')
        sys.exit(10)
    else:
        if test is None:
            print("Update the database to version: " + str(db_version))
            sys.exit(10)

#!/usr/bin/env python
#from datetime import datetime
from datetime import datetime
import dbqueries as dbq
import uuid

def startup(process):
    run_id = str(uuid.uuid4())
    query = dbq.start_run
    query_data = {'process': process,
                             'run_id': run_id,
                              'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    dbq.exec_db_query(query, query_data, query_type='insert')
    return run_id
    
def finished(run_id):
    query = dbq.finish_run
    query_data = {'finish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                              'complete': True, 
                             'run_id': run_id}
    dbq.exec_db_query(query, query_data, query_type='insert')


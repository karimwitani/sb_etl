import pandas as pd
from sqlalchemy import create_engine
import requests

# Database configuration
DATABASE_URL = "postgresql://karim:mypassword@localhost:5432/sb_data"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Query to get records where event_name = 'UFC 289'
query = "SELECT * FROM odds_records WHERE event_id is null"

# Read the query results into a DataFrame
df = pd.read_sql(query, engine)

# FastAPI endpoint to map odds record to event ID
FASTAPI_URL = "http://localhost:8000/mapping_serv/event-mapping/odds-record-to-event-id"

# Iterate over the DataFrame and call the FastAPI route for each record
for index, row in df.iterrows():
    # Convert the row to a dictionary and call the FastAPI endpoint
    record_dict = row.to_dict()
    print(record_dict['id'])
    odds_record_id = record_dict['id']
    url_with_query = f"{FASTAPI_URL}?odds_record_id={odds_record_id}"

    response = requests.post(url_with_query)
    # response = requests.post(FASTAPI_URL, data={"odds_record_id":record_dict['id']})
    # print(dir(response))
    print(response.content)
    """
    ['__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__',
    '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__',
    '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
    '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', '_content_consumed', '_next',
    'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect',
    'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request',
    'status_code', 'text', 'url']
    """    
    # Check the response
    if response.status_code == 200:
        print(f"Record {record_dict['id']} mapped successfully: {response.json()}")
    else:
        print(f"Failed to map record {record_dict['id']}: {response.text}")

print("All records processed.")

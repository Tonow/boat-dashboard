from datetime import datetime
import streamlit as st
import pandas as pd
from data_computations import get_speeds
from gsheetsdb import connect
import numpy as np

from config import DATA_URL, DATE_COLUMN
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return (str(z))
        else:
            return super().default(z)

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def compute_data(data):
    data = data.sort_values(by=DATE_COLUMN)
    data = get_speeds(data)
    return data.set_index(DATE_COLUMN)

def get_data():
    data = load_data()
    return compute_data(data)


def get_data_from_gs_sheet():
    # Create a connection object.
    conn = connect()

    # Perform SQL query on the Google Sheet.
    # Uses st.cache to only rerun when the query changes or after 10 min.
    @st.cache(ttl=600)
    def run_query(query):
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        return rows

    sheet_url = st.secrets["public_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    # df = pd.DataFrame({'col':L})
    # st.write(rows)
    # st.write(type(rows))

    df = pd.read_json(json.dumps(rows, cls=DateTimeEncoder), orient='values')
    df.columns = ["datetimes", "lat","lon"]
    df["lat"] = df["lat"].astype(np.float16)
    df["lon"] = df["lon"].astype(np.float16)
    st.write(pd.api.types.is_float_dtype(df["lat"]))
    st.write(pd.api.types.is_float_dtype(df["lon"]))
    df = compute_data(df)
    return df

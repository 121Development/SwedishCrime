# https://www.geeksforgeeks.org/data-science-apps-using-streamlit/
# https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html
# import the required modules 
import streamlit as st 

import pandas as pd 
import panda as p
import numpy as np 
import pydeck as pdk 
import plotly.express as px 
  
# Dataset we need to import 
# DATA_URL = ( 
#     "accidents_2012_to_2014.csv"
# ) 

#@st.cache
def load_data():
    data = p.queryToDF
  #  data['latitude'] = pd.to_numeric(data['latitude'],errors='coerce')
   # data['longitude'] = pd.to_numeric(data['longitude'],errors='coerce')

    #data['longitude'] = data['longitude'].astype(float)
    #data['latitude'] = data['latitude'].astype(float)
    #data = pd.DataFrame(columns=['title', 'updated', 'event_time', 'category', 'category_detail', 'location', 'summary', 'title', 'latitude', 'longitude'])
    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    return data

data = p.queryToDF()

st.title("Crimes in Sweden") 
st.markdown("This app pulls the incidents from the Swedish Police RSS feed") 

# Create a text element and let the reader know the data is loading.
#data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
#data = load_data()
# Notify the reader that the data was successfully loaded.
#data_load_state.text("Done! (using st.cache)")

st.subheader('Raw data')
st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(
#     data['event_time'].dt.hour, bins=24, range=(0,24))[0]

# st.bar_chart(hist_values)

st.subheader('Map of all incidents')
st.map(data)

st.subheader('Number of each incident type')
chart_data = pd.DataFrame(
# np.random.randn(50, 3),
columns=["location"])

st.bar_chart(chart_data)
#https://discuss.streamlit.io/t/st-bar-chart/4922/3
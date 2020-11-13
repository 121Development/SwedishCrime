# https://www.geeksforgeeks.org/data-science-apps-using-streamlit/
# https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html
# import the required modules 
import streamlit as st 

import pandas as pd 
import panda as p
import numpy as np 
import pydeck as pdk 
import plotly.express as px 
import DBConnector as db

db.whichConnection(0)
  
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

# st.sidebar.checkbox("Choose categories", True, key=1)
# select = st.sidebar.selectbox('Select categories',data['category'])

#st.sidebar.multiselect("Choose categories", data['CATEGORIES'], default = None, key=1)


# Create a list of possible values and multiselect menu with them in it.
categories = data['category'].unique()
categories_selected = st.sidebar.multiselect('Select categories', categories)
# Mask to filter dataframe
mask_data = data['category'].isin(categories_selected)

data = data[mask_data]

#select = st.sidebar.multiselect('Select categories',data['category'])

#get the state selected in the selectbox
# category_data = data[data['category'] == select]
# select_status = st.sidebar.radio("Covid-19 patient's status", ('Confirmed',
# 'Active', 'Recovered', 'Deceased'))


# def get_total_dataframe(dataset):
#     total_dataframe = pd.DataFrame({
#     'Status':['Confirmed', 'Recovered', 'Deaths','Active'],
#     'Number of cases':(dataset.iloc[0]['confirmed'],
#     dataset.iloc[0]['recovered'], 
#     dataset.iloc[0]['deaths'],dataset.iloc[0]['active'])})
#     return total_dataframe

# state_total = get_total_dataframe(state_data)

# if st.sidebar.checkbox("Show Analysis by State", True, key=2):
#     st.markdown("## **State level analysis**")
#     st.markdown("### Overall Confirmed, Active, Recovered and " +
#     "Deceased cases in %s yet" % (select))
#     if not st.checkbox('Hide Graph', False, key=1):
#         state_total_graph = px.bar(
#         state_total, 
#         x='Status',
#         y='Number of cases',
#         labels={'Number of cases':'Number of cases in %s' % (select)},
#         color='Status')
#         st.plotly_chart(state_total_graph)




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
st.map(data, use_container_width=True)

# st.subheader('Number of each incident type')
# chart_data = data(columns=["category"])

#st.bar_chart(chart_data)
#https://discuss.streamlit.io/t/st-bar-chart/4922/3
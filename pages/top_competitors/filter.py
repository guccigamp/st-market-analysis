import streamlit as st
import pandas as pd
from utils.ind_graphs import create_map
from streamlit_extras.chart_container import chart_container
from streamlit_folium import folium_static



df = pd.read_csv("datasets/companies_locations.csv")

# Set the page title and favicon
st.set_page_config(
    page_title="Filter by Company",
    layout="wide",
    page_icon="assets/ALTOR white.png"
)

# Add title and subtitle
st.header("Filter by Company")
st.write("This Scatterplot plots facilities of the selected companies")

# Add Multiselect box 
companies = st.multiselect(
    label="Select Companies",
    options=df.company.unique(),
    default=df.company.unique()[:5],
    placeholder="Choose a Company",
    help="You can select multiple companies. Maximum 10 companies can be selected",
    max_selections=10
)
selected_df = df.query(f"company in {companies}")
if companies:
    with chart_container(selected_df):
        folium_static(create_map(selected_df), height=600, width=1280)

col1, col2, col3 = st.columns(3)
with col1:
    # Card for Number of Companies
    st.metric(label="Selected Companies", value=len(selected_df.company.unique()))
with col2:    
    # Card for Number of Warehouses
    st.metric(label="Facilities", value=len(selected_df))
with col3:    
    # Card for Number of States
    st.metric(label="States", value=len(selected_df.state.unique()))


col5, col6, col7 = st.columns([2, 1, 1], gap="small")
with col5:
    # Card for the Company with most warehouses
    st.metric(label='Company with most Facilities', value=selected_df.company.value_counts().index[1])

with col6:
    # Card for the State with most warehouses
    st.metric(label="State with most Facilities", value=selected_df.state.value_counts().index[0])

with col7:
    # Card for the State with the least warehouses
    st.metric(label="State with least Facilities", value=selected_df.state.value_counts().index[-1])





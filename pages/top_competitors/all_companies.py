# all_company.py
import streamlit as st
from streamlit_extras.chart_container import chart_container
import pandas as pd
from utils.ind_graphs import create_map
from streamlit_folium import folium_static
import streamlit.components.v1 as components

path_to_html = "notebooks/warehouse_proximity_map.html" 

with open(path_to_html,'r') as f: 
    html_data = f.read()

# Set the page config
st.set_page_config(
    page_title="All Companies",
    layout="wide",
    page_icon="assets/ALTOR white.png"
)

# Load data
df = pd.read_csv("datasets/companies_locations.csv")

# Add title and subtitle
st.header("All Companies")
st.write("This Scatterplot plots warehouse locations of all companies, including Altor Solutions")

# Add chart
with chart_container(df):
    folium_static(create_map(df=df), width=1280, height=600)

# Create metrics
col1, col2, col3, col4 = st.columns([1,1,1,3], vertical_alignment="top", gap="large")
with col1:
    st.metric(label="Companies", value=len(df.company.unique()))
with col2:
    st.metric(label="Warehouses", value=len(df))
with col3:    
    st.metric(label="States", value=len(df.state.unique()))

col5, col6, col7 = st.columns([2, 1, 1], vertical_alignment="top", gap="large")
with col5:
    st.metric(label="Company with most warehouses", value=df.company.value_counts().index[1])
with col6:
    st.metric(label="State with most warehouses", value=df.state.value_counts().index[0])
with col7:
    st.metric(label="State with least warehouses", value=df.state.value_counts().index[-1])

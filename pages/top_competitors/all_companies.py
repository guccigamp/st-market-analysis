import streamlit as st
from streamlit_extras.chart_container import chart_container
import pandas as pd
import plotly.graph_objects as go
from utils.graphs import all_companies_scattergeo

df = pd.read_csv("datasets/companies_locations.csv")

# Set the page title and favicon
st.set_page_config(
    page_title="All Companies",
    layout="wide",
    page_icon="assets/ALTOR white.png"
)

# Add title and chart
col1, col2 = st.columns([1, 4], vertical_alignment="top", gap="large")
with col1:
    st.header("All Companies")
    st.write("This Scatterplot plots warehouse locations of all companies, including Altor Solutions")
    # Card for Number of Companies
    st.metric(label="Companies", value=len(df.company.unique()))
    # Card for Number of Warehouses
    st.metric(label="Warehouses", value=len(df))
    # Card for Number of States
    st.metric(label="States", value=len(df.state.unique()))

with col2:
    with chart_container(df[["company", "location", 'latitude', 'longitude']]):
        # Display the map
        st.plotly_chart(all_companies_scattergeo())

col5, col6, col7 = st.columns([2, 1, 1], vertical_alignment="top", gap="large")

with col5:
    # Card for the Company with most warehouses
    st.metric(label="Company with most warehouses", value=df.company.value_counts().index[1])
with col6:
    # Card for the State with most warehouses
    st.metric(label="State with most warehouses", value=df.state.value_counts().index[0])
with col7:
    # Card for the State with the least warehouses
    st.metric(label="State with least warehouses", value=df.state.value_counts().index[-1])

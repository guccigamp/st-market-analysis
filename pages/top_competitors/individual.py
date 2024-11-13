import streamlit as st
from streamlit_extras.chart_container import chart_container
import pandas as pd
import plotly.graph_objects as go
from utils.ind_graphs import create_map
from streamlit_folium import folium_static

df = pd.read_csv("datasets/companies_locations.csv")

# Set the page title and favicon
st.set_page_config(
    page_title="Company's Facilities",
    layout="wide",
    page_icon="assets/ALTOR white.png"
)

# Add title and subtitle
st.header("Company's Facilities")
st.write("This map plots a company's facilities")



# Add chart
plot_col, selectbox_col = st.columns([6,1], vertical_alignment="center")
with selectbox_col:
    # Create a select box for the company
    company = st.selectbox(
        label="Select a company",
        options=sorted(df.company.unique().tolist()),
        # index=2,
        placeholder="Choice an option"
    )
    company_df = df.query(f"company == '{company}'")

    # Card for Number of Warehouses
    st.metric(label="Warehouses", value=len(company_df))
    # Card for Number of States
    st.metric(label="States", value=len(company_df.state.unique()))
     # Card for the State with most warehouses
    st.metric(label="State with most warehouses", value=company_df.state.value_counts().index[0])
    # Card for the State with the least warehouses
    st.metric(label="State with least warehouses", value=company_df.state.value_counts().index[-1])     

with plot_col:
    with chart_container(df):
        # Display the map
        folium_static(create_map(company_df), width=1070, height=600)

# col1, col2, col3, col4 = st.columns([1,1,1,1], vertical_alignment="top", gap="large")

# with col1:
#     # Card for Number of Warehouses
#     st.metric(label="Warehouses", value=len(company_df))
# with col2:    
#     # Card for Number of States
#     st.metric(label="States", value=len(company_df.state.unique()))
# with col3:
#      # Card for the State with most warehouses
#     st.metric(label="State with most warehouses", value=company_df.state.value_counts().index[0])
# with col4:
#     # Card for the State with the least warehouses
#     st.metric(label="State with least warehouses", value=company_df.state.value_counts().index[-1]) 
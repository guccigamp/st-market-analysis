import streamlit as st
import pandas as pd
from utils.graphs import filter_by_company_scattergeo
from streamlit_extras.chart_container import chart_container


df = pd.read_csv("datasets/companies_locations.csv")

# Set the page title and favicon
st.set_page_config(
    page_title="Filter by Company",
    layout="wide",
    page_icon="assets/ALTOR white.png"
)
#
col1, col2 = st.columns([1, 4], vertical_alignment="top", gap="large")


with col2:
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
        with chart_container(selected_df[["company", "location", 'latitude', 'longitude']]):
            st.plotly_chart(filter_by_company_scattergeo(companies))



with col1:
    st.header("Filter by Company")
    st.write("This Scatterplot plots warehouse locations of the selected companies")
    st.markdown("___")
    # Card for Number of Companies
    st.metric(label="Selected Companies", value=len(selected_df.company.unique()))
    # Card for Number of Warehouses
    st.metric(label="Warehouses", value=len(selected_df))
    # Card for Number of States
    st.metric(label="States", value=len(selected_df.state.unique()))
    st.markdown("___")

col5, col6, col7 = st.columns([2, 1, 1], vertical_alignment="top", gap="large")
with col5:
    # Card for the Company with most warehouses
    st.metric(label='Company with most warehouses', value=selected_df.company.value_counts().index[1])

with col6:
    # Card for the State with most warehouses
    st.metric(label="State with most warehouses", value=selected_df.state.value_counts().index[0])

with col7:
    # Card for the State with the least warehouses
    st.metric(label="State with least warehouses", value=selected_df.state.value_counts().index[-1])





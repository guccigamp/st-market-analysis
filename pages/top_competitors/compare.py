import streamlit as st
import pandas as pd
from utils.graphs import compare_scattergeo
from streamlit_extras.chart_container import chart_container


df = pd.read_csv("datasets/companies_locations.csv")

st.set_page_config(
    page_title="Compare Companies",
    layout="wide",
    page_icon="assets/ALTOR white.png"
)
col1, col2 = st.columns([1, 4], vertical_alignment="top", gap="large")

with col1:
    st.header("Compare Companies")
    st.write("This Scatterplot allows you to compare warehouse locations of different companies with that of Altor Solutions")
    st.markdown("___")

    # Drop Altor Solutions from the company list
    company_list = df.company.unique().tolist()
    company_list.remove("Altor Solutions")

    # Create a select box for the company
    company = st.selectbox(
        label="Select a company",
        options=company_list,
        placeholder="Choice an option"
    )
    st.markdown("___")
    company_df = df.query(f"company == '{company}'")

with col2:
    with chart_container(company_df[["company", "location", 'latitude', 'longitude']]):
        # Display the map
        st.plotly_chart(compare_scattergeo(company))

col3, col4 = st.columns(2, vertical_alignment="top", gap="large")
with col3:
    st.subheader("Altor Solutions")
    # Altor Solutions Card
    st.metric(label="Altor Solutions", value=len(df.query("company == 'Altor Solutions'")))
    st.metric(label="Altor Solutions Warehouses", value=len(df.query("company == 'Altor Solutions'").location.unique()))
    st.metric(label="Altor Solutions States", value=len(df.query("company == 'Altor Solutions'").state.unique()))

with col4:
    st.subheader(company)
    # Company Card
    st.metric(label=company, value=len(company_df))
    st.metric(label=f"{company} Warehouses", value=len(company_df.location.unique()))
    st.metric(label=f"{company} States", value=len(company_df.state.unique()))
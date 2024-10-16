import streamlit as st
import pandas as pd

st.header("View the Top Competitors Dataset")
st.write(
    "This dataset contains information about the top competitors in the industry, including their locations, states, "
    "and other relevant details.")
df = pd.read_csv("datasets/companies_locations.csv")
st.dataframe(df[["company", "location", "state", "latitude", "longitude"]])
st.download_button("Download Dataset", df.to_csv(index=False), "top_competitors.csv")

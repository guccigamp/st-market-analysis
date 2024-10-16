import streamlit as st

# Add your company logo to the sidebar
st.logo("assets/ALTOR white.png", size="large", icon_image="assets/ALTOR white.png")

pages = {
    "Market Analysis": [
        st.Page("pages/top_competitors/all_companies.py", title="All Companies"),
        st.Page("pages/top_competitors/filter.py", title="Filter by Company"),
        st.Page("pages/top_competitors/compare.py", title="Compare Companies"),
    ],
    "Datasets": [
        st.Page("pages/dataset.py", title="Top Competitors")
    ],
}

pg = st.navigation(pages)
pg.run()

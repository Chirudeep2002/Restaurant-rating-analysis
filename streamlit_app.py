import streamlit as st

from utils.data_loader import (
    load_data,
    load_models
)

from components.sidebar import render_sidebar
from components.analytics import render_analytics_tab
from components.recommendations import render_recommendations_tab
from components.sentiment import render_sentiment_tab
from components.geo import render_geo_tab
from components.advisor import render_advisor_tab


# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="AI Restaurant Intelligence Platform",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===================================================
# LOAD CSS
# ===================================================

def load_css():

    with open("styles/main.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# ===================================================
# LOAD DATA
# ===================================================

df, reviews_df = load_data()

model, label_encoders = load_models()


# ===================================================
# SIDEBAR
# ===================================================

filtered_df = render_sidebar(df)


# ===================================================
# HERO SECTION
# ===================================================

st.markdown("""
<h1 style='font-size:55px;'>
🍽️ AI-Powered Restaurant Intelligence Platform
</h1>
""", unsafe_allow_html=True)

st.markdown("""
Explore restaurant trends, customer sentiment,
geo-based cuisine intelligence, and AI-powered
restaurant recommendations using Yelp data.
""")


# ===================================================
# TABS
# ===================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analytics",
    "🤖 Recommendations",
    "😊 Sentiment",
    "🗺️ Geo Analytics",
    "🤖 AI Restaurant Advisor"
])


with tab1:

    render_analytics_tab(
        filtered_df,
        reviews_df
    )

with tab2:

    render_recommendations_tab(df)

with tab3:

    render_sentiment_tab(
        df,
        reviews_df
    )

with tab4:

    render_geo_tab(df)

with tab5:

    render_advisor_tab(df)
st.markdown("""
<hr>

<center>

AI Restaurant Intelligence Platform <br>
Built with Streamlit, NLP, Recommendation Systems,
Geo Intelligence, and Google Places API.

</center>
""", unsafe_allow_html=True)
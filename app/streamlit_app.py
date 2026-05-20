import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import joblib
from streamlit_extras.metric_cards import style_metric_cards


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Restaurant Intelligence Platform",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

/* =====================================================
MAIN APP
===================================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );
    color: #f8fafc;
}


/* =====================================================
TEXT FIXES
===================================================== */

html,
body,
[class*="css"]  {
    color: #f8fafc !important;
}


/* LABELS */
label {
    color: #f1f5f9 !important;
    font-weight: 600 !important;
}


/* HEADINGS */
h1, h2, h3, h4, h5 {
    color: #ffffff !important;
}


/* PARAGRAPHS */
p {
    color: #cbd5e1 !important;
}


/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617,
        #0f172a
    );
    border-right: 1px solid #1e293b;
}


/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}


/* METRIC CARDS */
div[data-testid="metric-container"] {

    background: rgba(255,255,255,0.92);

    border-left: 8px solid #67e8f9;

    padding: 25px;

    border-radius: 18px;

    box-shadow: 0 0 15px rgba(0,0,0,0.2);
}

/* METRIC LABEL */
div[data-testid="metric-container"] label {

    color: #64748b !important;

    font-size: 18px !important;

    font-weight: 700 !important;
}

/* METRIC VALUE */
div[data-testid="metric-container"] [data-testid="stMetricValue"] {

    color: #0f172a !important;

    font-size: 42px !important;

    font-weight: 800 !important;
}


/* METRIC TEXT */
div[data-testid="metric-container"] label {

    color: #cbd5e1 !important;
}

div[data-testid="metric-container"] div {

    color: white !important;
}


/* =====================================================
SELECTBOX
===================================================== */

.stSelectbox div[data-baseweb="select"] {

    background-color: #1e293b !important;

    border-radius: 12px;

    color: white !important;
}


/* SELECTED TEXT */
.stSelectbox * {

    color: white !important;
}


/* =====================================================
SLIDER
===================================================== */

.stSlider * {

    color: white !important;
}


/* =====================================================
BUTTONS
===================================================== */

.stButton>button {

    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );

    color: white;

    border: none;

    border-radius: 12px;

    padding: 12px 24px;

    font-weight: bold;

    transition: 0.3s;
}

.stButton>button:hover {

    transform: scale(1.03);

    box-shadow: 0 0 15px rgba(59,130,246,0.5);
}


/* =====================================================
DATAFRAMES
===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;
}


/* TABLE TEXT */
table {

    color: white !important;
}


/* =====================================================
TABS
===================================================== */

.stTabs [data-baseweb="tab"] {

    color: #cbd5e1;

    font-size: 18px;

    font-weight: 600;
}

.stTabs [aria-selected="true"] {

    color: #38bdf8 !important;
}


/* =====================================================
PLOTLY CHARTS
===================================================== */

.js-plotly-plot .plotly .main-svg {

    background: transparent !important;
}


/* =====================================================
ANIMATIONS
===================================================== */

.element-container {

    animation: fadeInUp 0.7s ease;
}

@keyframes fadeInUp {

    from {

        opacity: 0;

        transform: translateY(15px);
    }

    to {

        opacity: 1;

        transform: translateY(0px);
    }
}


/* =====================================================
SUCCESS BOX
===================================================== */

.stSuccess {

    background-color: rgba(16,185,129,0.15) !important;

    color: white !important;

    border-radius: 12px;
}


/* =====================================================
WARNING BOX
===================================================== */

.stWarning {

    background-color: rgba(245,158,11,0.15) !important;

    color: white !important;
}


/* =====================================================
FOOTER
===================================================== */

footer {

    visibility: hidden;
}


            /* SELECTBOX TEXT FIX */
.stSelectbox div[data-baseweb="select"] > div {
    color: black !important;
    font-weight: 600 !important;
}

/* DROPDOWN MENU */
div[role="listbox"] {
    background-color: #e2e8f0 !important;
    color: black !important;
}

/* DROPDOWN OPTIONS */
div[role="option"] {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/processed/final_restaurant_data.csv"
    )

    reviews_df = pd.read_csv(
        "data/processed/restaurant_reviews_sentiment.csv"
    )

    return df, reviews_df


df, reviews_df = load_data()


# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

model = joblib.load(
    "models/restaurant_rating_model.pkl"
)

label_encoders = joblib.load(
    "models/label_encoders.pkl"
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown("""
# 🍽️ Restaurant AI
### Intelligence Platform
""")

st.sidebar.markdown("---")

st.sidebar.header("Filters")

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All"] + sorted(df['city'].dropna().unique())
)

selected_cuisine = st.sidebar.selectbox(
    "Select Cuisine",
    ["All"] + sorted(df['main_category'].dropna().unique())
)

min_rating_filter = st.sidebar.slider(
    "Minimum Rating",
    1.0,
    5.0,
    3.5
)


# ---------------------------------------------------
# FILTERING
# ---------------------------------------------------

filtered_df = df.copy()

if selected_city != "All":

    filtered_df = filtered_df[
        filtered_df['city'] == selected_city
    ]

if selected_cuisine != "All":

    filtered_df = filtered_df[
        filtered_df['main_category'] == selected_cuisine
    ]

filtered_df = filtered_df[
    filtered_df['stars'] >= min_rating_filter
]

if filtered_df.empty:

    st.warning(
        "No restaurants match selected filters."
    )

    st.stop()


# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<h1 style='font-size:55px;'>
🍽️ AI-Powered Restaurant Intelligence Platform
</h1>
""", unsafe_allow_html=True)

st.markdown("""
Analyze restaurant performance, customer sentiment,
recommendation intelligence, and predictive analytics
using Yelp data.
""")


# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analytics",
    "🤖 Recommendations",
    "😊 Sentiment",
    "🗺️ Geo Analytics",
    "🔮 AI Prediction"
])


# ===================================================
# TAB 1 — ANALYTICS
# ===================================================

with tab1:

    st.header("Restaurant Analytics Dashboard")

    # KPIs

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Restaurants",
            len(filtered_df)
        )

    with col2:

        st.metric(
            "Average Rating",
            round(filtered_df['stars'].mean(), 2)
        )

    with col3:

        st.metric(
            "Average Reviews",
            int(filtered_df['review_count'].mean())
        )

    style_metric_cards()

    st.markdown("---")

    # Top Restaurants

    st.subheader("Top Rated Restaurants")

    top_restaurants = filtered_df.sort_values(
        by=['stars', 'review_count'],
        ascending=False
    ).head(10)

    st.dataframe(
        top_restaurants[
            [
                'name',
                'city',
                'main_category',
                'stars',
                'review_count'
            ]
        ],
        use_container_width=True
    )

    st.markdown("---")

    # Charts

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:

        top_cuisines = (
            filtered_df['main_category']
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_cuisines.columns = [
            'Cuisine',
            'Count'
        ]

        fig1 = px.bar(
            top_cuisines,
            x='Cuisine',
            y='Count',
            title='Top Cuisine Categories',
            color='Count'
        )

        fig1.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
        family="Arial",
        size=15,
        color="white"
    ),

    title_font=dict(
        size=28,
        color="white"
    ),

    legend=dict(
        font=dict(
            color="white",
            size=14
        )
    ),

    xaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    ),

    yaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    )
     )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col_chart2:

        fig2 = px.histogram(
            filtered_df,
            x='stars',
            nbins=10,
            title='Ratings Distribution',
            color_discrete_sequence=['#38bdf8']
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
        family="Arial",
        size=15,
        color="white"
    ),

    title_font=dict(
        size=28,
        color="white"
    ),

    legend=dict(
        font=dict(
            color="white",
            size=14
        )
    ),

    xaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    ),

    yaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    )

        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


# ===================================================
# TAB 2 — RECOMMENDATIONS
# ===================================================

with tab2:

    st.header("AI Recommendation Engine")

    # Recommendation Section

    st.subheader("Restaurant Recommendations")

    user_cuisine = st.selectbox(
        "Choose Cuisine",
        sorted(df['main_category'].dropna().unique())
    )

    min_rating = st.slider(
        "Minimum Rating",
        1.0,
        5.0,
        4.0
    )

    recommendations = df[
        (df['main_category'] == user_cuisine)
        &
        (df['stars'] >= min_rating)
    ]

    recommendations = recommendations.sort_values(
        by=['stars', 'review_count'],
        ascending=False
    ).head(10)

    st.dataframe(
        recommendations[
            [
                'name',
                'city',
                'stars',
                'review_count'
            ]
        ],
        use_container_width=True
    )

    st.markdown("---")

    # Similarity Engine

    st.subheader("Find Similar Restaurants")

    # Reset index
    similarity_df = df.reset_index(drop=True)

    similarity_df['combined_features'] = (
        similarity_df['main_category'].astype(str)
        + " "
        + similarity_df['city'].astype(str)
        + " "
        + similarity_df['delivery'].astype(str)
        + " "
        + similarity_df['wifi'].astype(str)
    )

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(
        similarity_df['combined_features']
    )

    cosine_sim = cosine_similarity(
        tfidf_matrix
    )

    def get_similar_restaurants(
        restaurant_name
    ):

        matches = similarity_df[
            similarity_df['name'].str.lower()
            == restaurant_name.lower()
        ]

        if matches.empty:

            return pd.DataFrame()

        idx = matches.index[0]

        similarity_scores = list(
            enumerate(cosine_sim[idx])
        )

        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        similarity_scores = similarity_scores[1:11]

        restaurant_indices = [
            i[0]
            for i in similarity_scores
        ]

        return similarity_df.iloc[
            restaurant_indices
        ][
            [
                'name',
                'main_category',
                'city',
                'stars',
                'review_count'
            ]
        ]

    restaurant_input = st.selectbox(
        "Choose Restaurant",
        sorted(
            similarity_df['name']
            .dropna()
            .unique()
        )
    )

    if st.button(
        "Find Similar Restaurants"
    ):

        similar_restaurants = (
            get_similar_restaurants(
                restaurant_input
            )
        )

        st.dataframe(
            similar_restaurants,
            use_container_width=True
        )


# ===================================================
# TAB 3 — SENTIMENT ANALYTICS
# ===================================================

with tab3:

    st.header("Customer Sentiment Analytics")

    # Sentiment Distribution

    sentiment_counts = (
        reviews_df['sentiment']
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        'Sentiment',
        'Count'
    ]

    fig_sentiment = px.pie(
        sentiment_counts,
        names='Sentiment',
        values='Count',
        title='Customer Review Sentiment'
    )

    fig_sentiment.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
        family="Arial",
        size=15,
        color="white"
    ),

    title_font=dict(
        size=28,
        color="white"
    ),

    legend=dict(
        font=dict(
            color="white",
            size=14
        )
    ),

    xaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    ),

    yaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    )

    )

    st.plotly_chart(
        fig_sentiment,
        use_container_width=True
    )

    st.markdown("---")

    # Positive Cuisine Chart

    positive_cuisine_counts = (
        reviews_df[
            reviews_df['sentiment'] == 'Positive'
        ]
        .groupby('main_category')
        .size()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    positive_cuisine_counts.columns = [
        'Cuisine',
        'Positive Reviews'
    ]

    fig_cuisine = px.bar(
        positive_cuisine_counts,
        x='Cuisine',
        y='Positive Reviews',
        title='Top Positive Cuisine Categories',
        color='Positive Reviews'
    )

    fig_cuisine.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
        family="Arial",
        size=15,
        color="white"
    ),

    title_font=dict(
        size=28,
        color="white"
    ),

    legend=dict(
        font=dict(
            color="white",
            size=14
        )
    ),

    xaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    ),

    yaxis=dict(
        title_font=dict(
            color="white",
            size=18
        ),
        tickfont=dict(
            color="white",
            size=14
        )
    )

    )

    st.plotly_chart(
        fig_cuisine,
        use_container_width=True
    )

    st.markdown("---")

    # Word Clouds

    col_wc1, col_wc2 = st.columns(2)

    with col_wc1:

        st.subheader(
            "Positive Word Cloud"
        )

        positive_words = " ".join(
            reviews_df[
                reviews_df['sentiment']
                == 'Positive'
            ]['cleaned_text']
            .astype(str)
        )

        positive_wordcloud = WordCloud(
            width=1000,
            height=500,
            background_color='white'
        ).generate(positive_words)

        fig_wc, ax = plt.subplots(
            figsize=(10,5)
        )

        ax.imshow(positive_wordcloud)

        ax.axis('off')

        st.pyplot(fig_wc)

    with col_wc2:

        st.subheader(
            "Negative Word Cloud"
        )

        negative_words = " ".join(
            reviews_df[
                reviews_df['sentiment']
                == 'Negative'
            ]['cleaned_text']
            .astype(str)
        )

        negative_wordcloud = WordCloud(
            width=1000,
            height=500,
            background_color='black'
        ).generate(negative_words)

        fig_wc2, ax2 = plt.subplots(
            figsize=(10,5)
        )

        ax2.imshow(negative_wordcloud)

        ax2.axis('off')

        st.pyplot(fig_wc2)


# ===================================================
# TAB 4 — GEO ANALYTICS
# ===================================================

with tab4:

    st.header("Restaurant Geo Analytics")

    map_df = filtered_df.dropna(
        subset=['latitude', 'longitude']
    )

    restaurant_map = folium.Map(
        location=[
            map_df['latitude'].mean(),
            map_df['longitude'].mean()
        ],
        zoom_start=4
    )

    for _, row in map_df.head(200).iterrows():

        popup_text = (
            f"""
            <b>{row['name']}</b><br>
            Cuisine: {row['main_category']}<br>
            Rating: {row['stars']}<br>
            Reviews: {row['review_count']}
            """
        )

        folium.Marker(
            location=[
                row['latitude'],
                row['longitude']
            ],
            popup=popup_text
        ).add_to(restaurant_map)

    st_folium(
        restaurant_map,
        width=1200,
        height=600
    )


# ===================================================
# TAB 5 — AI PREDICTION
# ===================================================

with tab5:

    st.header("Restaurant Rating Prediction")

    pred_cuisine = st.selectbox(
        "Cuisine Type",
        sorted(df['main_category'].dropna().unique())
    )

    pred_city = st.selectbox(
        "City",
        sorted(df['city'].dropna().unique())
    )

    pred_review_count = st.slider(
        "Review Count",
        0,
        5000,
        100
    )

    pred_delivery = st.selectbox(
        "Delivery Available",
        ['True', 'False']
    )

    pred_outdoor = st.selectbox(
        "Outdoor Seating",
        ['True', 'False']
    )

    pred_reservation = st.selectbox(
        "Reservations Available",
        ['True', 'False']
    )

    input_data = pd.DataFrame({

        'main_category': [pred_cuisine],

        'city': [pred_city],

        'review_count': [pred_review_count],

        'delivery': [pred_delivery],

        'outdoor_seating': [pred_outdoor],

        'reservations': [pred_reservation]
    })

    for col in [

        'main_category',
        'city',
        'delivery',
        'outdoor_seating',
        'reservations'
    ]:

        input_data[col] = (
            label_encoders[col]
            .transform(input_data[col])
        )

    if st.button(
        "Predict Restaurant Rating"
    ):

        with st.spinner(
            "Generating AI Prediction..."
        ):

            prediction = model.predict(
                input_data
            )

        st.markdown(
            f"""
            <div style="
                padding:25px;
                border-radius:20px;
                background:linear-gradient(
                    90deg,
                    #0ea5e9,
                    #2563eb
                );
                color:white;
                font-size:28px;
                font-weight:bold;
                text-align:center;
            ">
            Predicted Restaurant Rating:
            {prediction[0]:.2f} ⭐
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown("""
<center>

### 🚀 Built with:
Python • Streamlit • Plotly • Scikit-learn • NLP • Folium

AI-Powered Restaurant Intelligence Platform

</center>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def render_recommendations_tab(df):

    st.header("🤖 AI Dining Discovery")

    st.markdown("""
    Discover highly-rated restaurants using cuisine intelligence,
    customer satisfaction analytics, and recommendation AI.
    """)

    st.markdown("---")

    # ==================================================
    # SMART RECOMMENDATIONS
    # ==================================================

    st.subheader("🍽️ Smart Restaurant Recommendations")

    col1, col2 = st.columns(2)

    with col1:

        user_cuisine = st.selectbox(
            "Choose Cuisine",
            sorted(
                df['main_category']
                .dropna()
                .unique()
            )
        )

    with col2:

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
    ).head(8)

    st.markdown("---")

    for _, row in recommendations.iterrows():

        st.markdown(f"""
        <div class="restaurant-card">

        <div class="restaurant-title">
        🍴 {row['name']}
        </div>

        <div class="badge-container">

        <div class="rating-badge">
        ⭐ {row['stars']}
        </div>

        <div class="review-badge">
        📝 {row['review_count']} Reviews
        </div>

        <div class="location-badge">
        📍 {row['city']}
        </div>

        <div class="cuisine-badge">
        🍽️ {row['main_category']}
        </div>

        </div>

        <div class="ai-insight">

        AI Insight:
        Customers highly rate this restaurant
        for food quality, dining experience,
        and customer satisfaction.

        </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # SIMILAR RESTAURANTS
    # ==================================================

    st.subheader("🔍 Discover Similar Restaurants")

    similarity_df = df.reset_index(drop=True)
    # ==================================================
# SAFE FEATURE ENGINEERING
# ==================================================

    similarity_df['main_category'] = (
    similarity_df['main_category']
    .fillna("Unknown")
    .astype(str)
    )

    similarity_df['city'] = (
    similarity_df['city']
    .fillna("Unknown")
    .astype(str)
    )

    # Optional columns safety

    if 'delivery' not in similarity_df.columns:

        similarity_df['delivery'] = "Unknown"

    if 'wifi' not in similarity_df.columns:

        similarity_df['wifi'] = "Unknown"

    similarity_df['delivery'] = (
    similarity_df['delivery']
    .fillna("Unknown")
    .astype(str)
    )

    similarity_df['wifi'] = (
    similarity_df['wifi']
    .fillna("Unknown")
    .astype(str)
    )

    # FINAL COMBINED FEATURES

    similarity_df['combined_features'] = (

    similarity_df['main_category']
    + " "
    + similarity_df['city']
    + " "
    + similarity_df['delivery']
    + " "
    + similarity_df['wifi']

    )   

    # FINAL SAFETY

    similarity_df = similarity_df.dropna(
    subset=['combined_features']
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

        similarity_scores = similarity_scores[1:7]

        restaurant_indices = [
            i[0]
            for i in similarity_scores
        ]

        return similarity_df.iloc[
            restaurant_indices
        ]

    restaurant_input = st.selectbox(
        "Choose Restaurant",
        sorted(
            similarity_df['name']
            .dropna()
            .unique()
        )
    )

    if st.button("Find Similar Restaurants"):

        similar_restaurants = (
            get_similar_restaurants(
                restaurant_input
            )
        )

        st.markdown("---")

        for _, row in similar_restaurants.iterrows():

            st.markdown(f"""
            <div class="restaurant-card">

            <div class="restaurant-title">
            🍴 {row['name']}
            </div>

            <div class="badge-container">

            <div class="rating-badge">
            ⭐ {row['stars']}
            </div>

            <div class="review-badge">
            📝 {row['review_count']} Reviews
            </div>

            <div class="location-badge">
            📍 {row['city']}
            </div>

            <div class="cuisine-badge">
            🍽️ {row['main_category']}
            </div>

            </div>

            <div class="ai-insight">

            Similar customer preferences,
            cuisine patterns, and dining attributes
            make this restaurant a strong match.

            </div>

            </div>
            """, unsafe_allow_html=True)
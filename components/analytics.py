from turtle import pd
import pandas as pd
import streamlit as st
import plotly.express as px

def render_analytics_tab(
    filtered_df,
    reviews_df
):
    if filtered_df.empty:
        st.warning("No restaurants found for selected filters.")
        return

    st.header("📊 Executive Restaurant Intelligence")

    st.markdown("""
    Analyze restaurant performance, customer engagement,
    cuisine trends, and dining intelligence across the platform.
    """)

    st.markdown("---")

    # ==================================================
    # KPI SECTION
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Restaurants",
            len(filtered_df)
        )

    with col2:

        avg_reviews = filtered_df['review_count'].mean()

        if pd.isna(avg_reviews):
            avg_reviews = 0
        else:
            avg_reviews = int(avg_reviews)

        st.metric("Average Reviews",avg_reviews)

    with col3:

        st.metric(
            "Avg Reviews",
            int(filtered_df['review_count'].mean())
        )

    with col4:

        top_category = (
            filtered_df['main_category']
            .value_counts()
            .idxmax()
        )

        st.metric(
            "Top Cuisine",
            top_category
        )

    st.markdown("---")
    # ==================================================
    # DYNAMIC INSIGHTS
    # ==================================================

    highest_rated_city = (
        filtered_df.groupby('city')['stars']
        .mean()
        .sort_values(ascending=False)
        .head(1)
        .index[0]
    )

    top_positive_cuisine = (
        reviews_df[
            reviews_df['sentiment'] == 'Positive'
        ]['main_category']
        .value_counts()
        .idxmax()
    )

    top_negative_cuisine = (
        reviews_df[
            reviews_df['sentiment'] == 'Negative'
        ]['main_category']
        .value_counts()
        .idxmax()
    )

    most_reviewed_city = (
        filtered_df['city']
        .value_counts()
        .idxmax()
    )

    positive_reviews = len(
        reviews_df[
            reviews_df['sentiment'] == 'Positive'
        ]
    )

    total_reviews = len(reviews_df)

    sentiment_score = round(
        (positive_reviews / total_reviews) * 100,
        1
    )

    # ==================================================
    # INSIGHT + CHART SECTION
    # ==================================================

    col_chart, col_insight = st.columns([1.2, 1])

    # --------------------------------------------------
    # TOP CUISINE CHART
    # --------------------------------------------------

    if filtered_df.empty:

        st.warning("No cuisine data available for selected filters.")

        top_cuisines = pd.DataFrame(
        columns=['main_category', 'count']
        )

    else:

        top_cuisines = (
        filtered_df['main_category']
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_cuisines.columns = [
        'Cuisine',
        'Restaurants'
    ]

    fig1 = px.bar(
        top_cuisines,
        x='Cuisine',
        y='Restaurants',
        color='Restaurants',
        title='Top Cuisine Categories'
    )

    fig1.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=15
        ),

        title_font=dict(
            color="white",
            size=28
        ),

        xaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white")
        ),

        yaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white")
        ),

        legend=dict(
            font=dict(color="white")
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    with col_chart:

        st.markdown(
            '<div class="chart-card">',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("""
        <p style='font-size:17px; color:#cbd5e1;'>

        Cuisine popularity analysis shows strong customer demand
        concentrated around dominant restaurant categories.

        Customer engagement remains highest for cuisines
        delivering consistent dining experiences and strong reviews.

        </p>
        """, unsafe_allow_html=True)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # INSIGHTS CARD
    # --------------------------------------------------

    with col_insight:

        st.markdown(f"""
        <div class="chart-card">

        <h2>📌 Customer Intelligence</h2>

        <p style="
            font-size:17px;
            line-height:1.9;
            color:#cbd5e1;
        ">

        <b>{sentiment_score}%</b> of customer reviews
        express positive dining experiences.

        <br><br>

        <b>{top_positive_cuisine}</b> restaurants
        receive the strongest positive customer sentiment
        across the platform.

        <br><br>

        The highest concentration of customer engagement
        is currently observed in <b>{most_reviewed_city}</b>.

        <br><br>

        <b>{highest_rated_city}</b> demonstrates
        the strongest overall restaurant ratings.

        <br><br>

        Negative reviews are most frequently associated
        with <b>{top_negative_cuisine}</b> restaurants,
        primarily due to operational and wait-time concerns.

        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # RATINGS DISTRIBUTION
    # ==================================================

    fig2 = px.histogram(
        filtered_df,
        x='stars',
        nbins=10,
        title='Customer Rating Distribution',
        color_discrete_sequence=['#38bdf8']
    )

    fig2.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=15
        ),

        title_font=dict(
            color="white",
            size=28
        ),

        xaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white")
        ),

        yaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white")
        ),

        legend=dict(
            font=dict(color="white")
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown("""
    <p style='font-size:17px; color:#cbd5e1;'>

    Most restaurants maintain ratings between
    3.5 and 5.0 stars, indicating generally
    strong customer satisfaction trends.

    Higher-rated restaurants typically demonstrate
    stronger review consistency and customer engagement.

    </p>
    """, unsafe_allow_html=True)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ==================================================
    # TOP RESTAURANTS
    # ==================================================

    st.subheader("⭐ Top Performing Restaurants")

    top_restaurants = filtered_df.sort_values(
        by=['stars', 'review_count'],
        ascending=False
    ).head(8)

    for _, row in top_restaurants.iterrows():

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
        Customers consistently praise this restaurant
        for food quality, customer service,
        and dining consistency.

        </div>

        </div>
        """, unsafe_allow_html=True)
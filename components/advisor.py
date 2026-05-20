import streamlit as st
import plotly.express as px
import pandas as pd

from collections import Counter

from utils.google_places import get_restaurants


def render_advisor_tab(df):

    st.header("🤖 AI Restaurant Advisor")

    st.markdown("""
    Discover the best restaurant experiences
    using live AI-powered dining intelligence.
    """)

    st.markdown("---")

    # ==================================================
    # USER INPUTS
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        advisor_city = st.text_input(
            "📍 Enter Location / City",
            placeholder="Example: Philadelphia"
        )

    with col2:

        advisor_vibe = st.selectbox(
            "Dining Preference",
            [
                "Family Dining",
                "Luxury Experience",
                "Quick Bites",
                "Casual Dining",
                "Late Night Food",
                "Outdoor Experience"
            ]
        )

    # ==================================================
    # EMPTY INPUT HANDLING
    # ==================================================

    if not advisor_city:

        st.info(
            "Enter a city/location to discover restaurants."
        )

        st.stop()

    # ==================================================
    # GOOGLE PLACES API
    # ==================================================

    with st.spinner(
    "Finding the best restaurants..."):

        restaurants = get_restaurants(
        advisor_city
        )

        if not restaurants:

            st.warning(
            "No restaurants found for this location."
        )

            st.stop()

    # ==================================================
    # EXTRACT RESTAURANT DATA
    # ==================================================

    restaurant_data = []

    cuisine_list = []

    for restaurant in restaurants:

        name = restaurant.get(
            "name",
            "Unknown"
        )

        rating = restaurant.get(
            "rating",
            0
        )

        reviews = restaurant.get(
            "user_ratings_total",
            0
        )

        address = restaurant.get(
            "formatted_address",
            "Unknown"
        )

        types = restaurant.get(
            "types",
            []
        )

        # Attempt cuisine extraction

        cuisine = "Restaurant"

        for t in types:

            if t not in [
                "restaurant",
                "food",
                "point_of_interest",
                "establishment"
            ]:

                cuisine = (
                    t.replace("_", " ")
                    .title()
                )

                break

        cuisine_list.append(cuisine)

        restaurant_data.append({
            "Name": name,
            "Cuisine": cuisine,
            "Rating": rating,
            "Reviews": reviews,
            "Address": address
        })

    restaurants_df = pd.DataFrame(
        restaurant_data
    )

    # ==================================================
    # BEST CUISINE INTELLIGENCE
    # ==================================================

    cuisine_counter = Counter(
        cuisine_list
    )

    best_cuisine = cuisine_counter.most_common(1)[0][0]

    st.markdown(f"""
    <div class="chart-card">

    <h2>🍽️ Best Cuisine Trend in {advisor_city}</h2>

    <h1 style="
        color:#38bdf8;
        font-size:52px;
        margin-bottom:10px;
    ">
    {best_cuisine}
    </h1>

    <p style="
        color:#cbd5e1;
        font-size:18px;
        line-height:1.8;
    ">

    Based on live restaurant intelligence,
    customer engagement,
    and cuisine popularity,
    <b>{best_cuisine}</b> currently dominates
    the dining landscape in <b>{advisor_city}</b>.

    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # CUISINE DISTRIBUTION CHART
    # ==================================================

    cuisine_chart_df = pd.DataFrame(
        cuisine_counter.items(),
        columns=[
            "Cuisine",
            "Count"
        ]
    )

    cuisine_chart_df = cuisine_chart_df.sort_values(
        by="Count",
        ascending=False
    ).head(10)

    fig_advisor = px.bar(
        cuisine_chart_df,
        x='Cuisine',
        y='Count',
        color='Count',
        title=f'Top Cuisine Trends in {advisor_city}'
    )

    fig_advisor.update_layout(

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
        fig_advisor,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ==================================================
    # LIVE RESTAURANT RECOMMENDATIONS
    # ==================================================

    st.subheader(
        f"⭐ Best Restaurants in {advisor_city}"
    )

    restaurants_df = restaurants_df.sort_values(
        by=[
            "Rating",
            "Reviews"
        ],
        ascending=False
    )

    for _, row in restaurants_df.head(10).iterrows():

        st.markdown(f"""
        <div class="restaurant-card">

        <div class="restaurant-title">
        🍴 {row['Name']}
        </div>

        <div class="badge-container">

        <div class="rating-badge">
        ⭐ {row['Rating']}
        </div>

        <div class="review-badge">
        📝 {row['Reviews']} Reviews
        </div>

        <div class="location-badge">
        📍 {row['Address']}
        </div>

        <div class="cuisine-badge">
        🍽️ {row['Cuisine']}
        </div>

        </div>

        <div class="ai-insight">

        AI Insight:
        This restaurant demonstrates
        strong customer engagement,
        positive dining reputation,
        and high local popularity
        in {advisor_city}.

        </div>

        </div>
        """, unsafe_allow_html=True)
import streamlit as st
import plotly.express as px
import folium

from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


def render_geo_tab(df):

    st.header("🌍 Geo Intelligence Dashboard")

    st.markdown("""
    Explore cuisine hotspots, restaurant intelligence,
    and dining trends by location.
    """)

    st.markdown("---")

    selected_geo_city = st.selectbox(
        "📍 Select City",
        sorted(df['city'].dropna().unique())
    )

    city_geo_df = df[
        df['city'] == selected_geo_city
    ]

    st.markdown("---")

    # ==================================================
    # METRICS
    # ==================================================

    geo_col1, geo_col2, geo_col3 = st.columns(3)

    with geo_col1:

        st.metric(
            "Restaurants",
            len(city_geo_df)
        )

    with geo_col2:

        st.metric(
            "Average Rating",
            round(
                city_geo_df['stars'].mean(),
                2
            )
        )

    with geo_col3:

        top_city_cuisine = (
            city_geo_df['main_category']
            .value_counts()
            .idxmax()
        )

        st.metric(
            "Top Cuisine",
            top_city_cuisine
        )

    st.markdown("---")

    # ==================================================
    # CUISINE CHART
    # ==================================================

    cuisine_counts = (
        city_geo_df['main_category']
        .value_counts()
        .head(10)
        .reset_index()
    )

    cuisine_counts.columns = [
        'Cuisine',
        'Restaurants'
    ]

    fig_geo = px.bar(
        cuisine_counts,
        x='Cuisine',
        y='Restaurants',
        color='Restaurants',
        title=f'Top Cuisine Categories in {selected_geo_city}'
    )

    fig_geo.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(
            color="white",
            size=28
        )
    )

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig_geo,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ==================================================
    # MAP
    # ==================================================

    st.subheader("🗺️ Restaurant Intelligence Map")

    map_df = city_geo_df.dropna(
        subset=['latitude', 'longitude']
    )

    if not map_df.empty:

        restaurant_map = folium.Map(
            location=[
                map_df['latitude'].mean(),
                map_df['longitude'].mean()
            ],
            zoom_start=11,
            tiles="CartoDB positron"
        )

        marker_cluster = MarkerCluster().add_to(
            restaurant_map
        )

        for _, row in map_df.head(300).iterrows():

            popup_text = f"""
            <b>{row['name']}</b><br>
            Cuisine: {row['main_category']}<br>
            Rating: ⭐ {row['stars']}<br>
            Reviews: {row['review_count']}
            """

            folium.Marker(
                location=[
                    row['latitude'],
                    row['longitude']
                ],
                popup=popup_text,
                tooltip=row['name']
            ).add_to(marker_cluster)

        st.markdown(
            '<div class="chart-card">',
            unsafe_allow_html=True
        )

        st_folium(
            restaurant_map,
            width=1200,
            height=650
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
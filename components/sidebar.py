import streamlit as st


def render_sidebar(df):

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

    return filtered_df
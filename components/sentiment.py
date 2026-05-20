import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def render_sentiment_tab(
    df,
    reviews_df
):

    st.header("😊 Customer Sentiment Intelligence")

    st.markdown("""
    Analyze customer emotions, dining experiences,
    review behavior, and restaurant satisfaction trends.
    """)

    st.markdown("---")

    # ==================================================
    # KPIs
    # ==================================================

    positive_reviews = len(
        reviews_df[
            reviews_df['sentiment'] == 'Positive'
        ]
    )

    negative_reviews = len(
        reviews_df[
            reviews_df['sentiment'] == 'Negative'
        ]
    )

    neutral_reviews = len(
        reviews_df[
            reviews_df['sentiment'] == 'Neutral'
        ]
    )

    total_reviews = len(reviews_df)

    sentiment_score = round(
        (positive_reviews / total_reviews) * 100,
        1
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Reviews",
            f"{total_reviews:,}"
        )

    with col2:

        st.metric(
            "Positive Reviews",
            f"{positive_reviews:,}"
        )

    with col3:

        st.metric(
            "Negative Reviews",
            f"{negative_reviews:,}"
        )

    with col4:

        st.metric(
            "Customer Satisfaction",
            f"{sentiment_score}%"
        )

    st.markdown("---")

    # ==================================================
    # PIE CHART
    # ==================================================

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
        title='Customer Review Sentiment Distribution',
        hole=0.45,
        color='Sentiment',
        color_discrete_map={
            'Positive': '#10b981',
            'Negative': '#ef4444',
            'Neutral': '#f59e0b'
        }
    )

    fig_sentiment.update_layout(

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

    col_chart, col_insight = st.columns([1.2, 1])

    with col_chart:

        st.markdown(
            '<div class="chart-card">',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig_sentiment,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # ==================================================
    # DYNAMIC INSIGHTS
    # ==================================================

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
        df['city']
        .value_counts()
        .idxmax()
    )

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
        receive the strongest positive customer sentiment.

        <br><br>

        Highest customer engagement is currently observed
        in <b>{most_reviewed_city}</b>.

        <br><br>

        Negative reviews are frequently associated with
        <b>{top_negative_cuisine}</b> restaurants.

        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # POSITIVE CUISINES
    # ==================================================

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
        color='Positive Reviews',
        title='Top Positively Reviewed Cuisine Categories'
    )

    fig_cuisine.update_layout(

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
        fig_cuisine,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# ==================================================
# POSITIVE WORD CLOUD
# ==================================================

    st.subheader("💚 Positive Customer Language")

    positive_words = " ".join(
        reviews_df[
        reviews_df['sentiment'] == 'Positive'
    ]['cleaned_text']
    .astype(str)
    )

    positive_wordcloud = WordCloud(
    width=1600,
    height=700,
    background_color='white',
    colormap='viridis'
    ).generate(positive_words)

    fig_wc1, ax1 = plt.subplots(
    figsize=(16,7)
    )

    ax1.imshow(positive_wordcloud)

    ax1.axis('off')

    st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
    )

    st.pyplot(fig_wc1)

    st.markdown("""

### 🌟 Key Positive Themes

- Customers highly value food quality and freshness.
- Friendly staff and service strongly impact ratings.
- Restaurant atmosphere contributes to customer satisfaction.
- Fast delivery and consistency improve engagement.

""")

    st.markdown(
    '</div>',
    unsafe_allow_html=True
    )

    st.markdown("---")

# ==================================================
# NEGATIVE WORD CLOUD
# ==================================================

    st.subheader("💔 Negative Customer Language")

    negative_words = " ".join(
        reviews_df[
        reviews_df['sentiment'] == 'Negative'
    ]['cleaned_text']
    .astype(str)
    )

    negative_wordcloud = WordCloud(
    width=1600,
    height=700,
    background_color='black',
    colormap='Reds'
    ).generate(negative_words)

    fig_wc2, ax2 = plt.subplots(
    figsize=(16,7)
    )

    ax2.imshow(negative_wordcloud)

    ax2.axis('off')

    st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
    )

    st.pyplot(fig_wc2)

    st.markdown("""

    ### ⚠️ Common Customer Complaints

- Slow service and long wait times reduce satisfaction.
- Incorrect orders negatively impact customer trust.
- Price sensitivity affects perceived dining value.
- Operational delays create poor customer experiences.

""")

    st.markdown(
    '</div>',
    unsafe_allow_html=True
    )
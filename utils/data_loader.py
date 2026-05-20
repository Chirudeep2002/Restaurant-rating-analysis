import pandas as pd
import joblib
import streamlit as st


@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/processed/final_restaurant_data.csv"
    )

    reviews_df = pd.read_csv(
        "data/processed/restaurant_reviews_sentiment.csv"
    )

    return df, reviews_df


@st.cache_resource
def load_models():

    model = joblib.load(
        "models/restaurant_rating_model.pkl"
    )

    label_encoders = joblib.load(
        "models/label_encoders.pkl"
    )

    return model, label_encoders
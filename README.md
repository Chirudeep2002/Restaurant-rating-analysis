# 🍽️ AI Restaurant Intelligence Platform

> **NLP-powered restaurant analytics and discovery** — sentiment analysis, smart recommendations, geo intelligence, and live Google Places integration built on the Yelp Open Dataset.

🌐 **Live Demo:** [restaurant-rating.streamlit.app](https://restaurant-rating.streamlit.app/)
&nbsp;&nbsp;|&nbsp;&nbsp;
📁 **GitHub:** [Restaurant-rating-analysis](https://github.com/Chirudeep2002/Restaurant-rating-analysis)

---

## 📊 Project Stats

| Metric | Value |
|---|---|
| 🍴 Restaurants | **1,762** across 308 cities |
| 📝 Reviews Analyzed | **5,000** Yelp reviews |
| 🗺️ Geographic Coverage | **14 states** · 308 cities |
| 🍜 Cuisine Categories | **171** unique categories |
| 🎯 Sentiment Accuracy | **93%** (TF-IDF + Gradient Boosting) |
| 🔗 Live API | Google Places API (real-time discovery) |
| 📦 Dataset Source | [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/) |

---

## 🧠 What It Does

A full-stack restaurant intelligence platform that goes beyond simple ratings. It analyzes what customers *actually say* (not just stars), surfaces similar restaurants, maps cuisine hotspots geographically, and provides live restaurant discovery via the Google Places API — even for restaurants outside the local dataset.

---

## 🚀 Features

### 📊 Executive Analytics Dashboard
- Restaurant performance analytics across 171 cuisines
- Dynamic KPI cards: average rating (3.51★), review volume, category distribution
- Cuisine trend analysis and customer engagement insights
- Interactive Plotly visualizations

### 😊 Customer Sentiment Intelligence (93% Accuracy)
- NLP sentiment classification (Positive / Negative / Neutral)
- Model: TF-IDF vectorization (bigrams) + Gradient Boosting classifier
- Trained on 5,000 labeled Yelp reviews
- WordCloud visualization by sentiment class
- Positive/negative keyword extraction

**Sentiment breakdown in dataset:**
| Sentiment | Count | Share |
|---|---|---|
| Positive | 4,587 | 91.7% |
| Negative | 388 | 7.8% |
| Neutral | 25 | 0.5% |

### 🤖 AI Dining Discovery (Recommendation Engine)
- TF-IDF + Cosine Similarity across 1,762 restaurants
- Similar restaurant finder by cuisine profile
- AI-generated dining insights per recommendation
- Premium restaurant cards with feature highlights

### 🌍 Geo Intelligence Dashboard
- Interactive Folium maps with restaurant clustering
- Cuisine hotspot analytics by city/state
- Location-based restaurant density visualization
- Heatmap-ready architecture for 308 cities

### 🤖 AI Restaurant Advisor (Live)
- Real-time restaurant discovery via Google Places API
- Works beyond the local Yelp dataset (any city, any cuisine)
- AI-generated dining recommendations with context
- Dynamic location + cuisine filtering

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **NLP / ML** | Scikit-learn · TF-IDF Vectorizer · Gradient Boosting · Cosine Similarity |
| **Visualization** | Plotly · Folium · WordCloud |
| **Backend** | Python · Pandas · NumPy · Joblib |
| **APIs** | Google Places API |
| **Frontend** | Streamlit · Custom CSS |
| **Deployment** | Streamlit Community Cloud |

---

## 🔬 NLP Pipeline

```
Raw Yelp Review Text
        │
        ▼
┌──────────────────────────┐
│    Text Preprocessing    │  ← Lowercasing, stopword removal, lemmatization
└────────────┬─────────────┘
             │
    ┌────────▼────────┐
    │ TF-IDF (bigram) │  ← 5,000 features, (1,2)-gram range
    └────────┬────────┘
             │
    ┌────────▼──────────────────┐
    │  Gradient Boosting        │  ← 93% accuracy on held-out test set
    │  Sentiment Classifier     │
    └────────┬──────────────────┘
             │
    Positive / Negative / Neutral  +  Confidence Score
```

---

## 📂 Project Structure

```
restaurant-rating-analysis/
│
├── streamlit_app.py            # Main entrypoint
│
├── components/
│   ├── analytics.py            # Dashboard analytics
│   ├── recommendations.py      # TF-IDF recommendation engine
│   ├── sentiment.py            # NLP sentiment pipeline
│   ├── geo.py                  # Folium geo maps
│   ├── advisor.py              # Google Places advisor
│   └── sidebar.py              # UI navigation
│
├── utils/
│   ├── data_loader.py          # Dataset loading & caching
│   └── google_places.py        # Places API wrapper
│
├── styles/
│   └── main.css
│
├── data/processed/             # Processed Yelp data
├── models/                     # Serialized ML models
├── notebooks/                  # EDA notebooks
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/Chirudeep2002/Restaurant-rating-analysis.git
cd Restaurant-rating-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the Yelp Dataset
# Visit: https://business.yelp.com/data/resources/open-dataset/
# Place the files in data/processed/

# 4. Add Google Places API key
# Create .streamlit/secrets.toml:
# GOOGLE_PLACES_API_KEY = "YOUR_KEY"

# 5. Run
streamlit run streamlit_app.py
```

---

## 🔮 Roadmap

- [ ] BERT-based sentiment model (upgrade from TF-IDF)
- [ ] Real-time Yelp API integration
- [ ] User preference learning (personalized recommendations)
- [ ] PostgreSQL for production-scale storage
- [ ] Restaurant trend forecasting module

---

## 👨‍💻 Author

**Bandapalli Chirudeep**
MS Computer Science · UNC Charlotte · AI & Data Engineering

[![LinkedIn](https://img.shields.io/badge/LinkedIn-chirudeepbandapalli-blue?style=flat&logo=linkedin)](https://linkedin.com/in/chirudeepbandapalli)
[![GitHub](https://img.shields.io/badge/GitHub-Chirudeep2002-black?style=flat&logo=github)](https://github.com/Chirudeep2002)
[![Portfolio](https://img.shields.io/badge/Portfolio-chirudeep--portfolio.vercel.app-green?style=flat)](https://chirudeep-portfolio.vercel.app)

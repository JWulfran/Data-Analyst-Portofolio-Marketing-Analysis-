import pandas as pd
import pyodbc
import sqlalchemy
from sqlalchemy import create_engine, text
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')


def fetch_data_from_sql():
   # Replace driver if needed: ODBC Driver 18 for SQL Server is common on Windows now
    engine = create_engine(
    "mssql+pyodbc://@JWULFRAN\\SQLEXPRESS/PortfolioProject_MarketingAnalytics"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )

    query = text("""
    SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText
    FROM dbo.customer_reviews
    """)  # change schema if not dbo

    df= pd.read_sql(query, engine)
    return df

customer_reviews_df = fetch_data_from_sql()
SIA = SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    sentiment = SIA.polarity_scores(review)
    return sentiment['compound']

def categorize_sentiment(score, rating):
    if score > 0.05:
        if rating >= 4:
            return 'Positif'
        elif rating == 3:
            return 'Mix Positif'
        else: 
            return "Mix Negatif"
    elif score < -0.05:
        if rating <= 2:
            return "Negatif"
        elif rating == 3:
            return "Mix Negatif"
        else:
            return "Mix Positif"
    else:
        if rating >=4:
            return "Positif"
        elif rating <= 2:
            return "Negatif"
        else:
            return "Neutre"
        
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'
    else: 
        return '-1.0 to -0.5'
    
customer_reviews_df['sentiment_score'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

customer_reviews_df['sentiment_category'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['sentiment_score'], row['Rating']), axis=1)

customer_reviews_df['sentiment_bucket'] = customer_reviews_df['sentiment_score'].apply(sentiment_bucket)

print(customer_reviews_df.head())

customer_reviews_df.to_csv('customer_reviews_enriched.csv', index=False)




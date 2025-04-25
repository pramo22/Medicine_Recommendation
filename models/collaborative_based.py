# %%
import pandas as pd
import os
import joblib
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

# %%
# File Paths
MODEL_PATH = "models/svd_model.pkl"
COLLAB_CSV_PATH = "data\\collaborative_scores.csv"
CONTENT_CSV_PATH = "data\\content_scores.csv"
HYBRID_CSV_PATH = "data/hybrid_scores.csv"
DRUG_REVIEWS_PATH = "data\\drug_reviews_with_sentiment.csv"

# %%
# Load data
df = pd.read_csv(DRUG_REVIEWS_PATH)
df = df.dropna(subset=['drugName', 'rating']).reset_index(drop=True)  # Drop missing ratings
# Convert 'condition' column to lowercase for case-insensitive comparison
df['condition'] = df['condition'].str.lower()

# %%
# Select necessary columns
df_cf = df[['patient_id', 'drugName', 'rating']]

# %%
# Prepare the Surprise dataset
reader = Reader(rating_scale=(1, 10))  # Adjust rating scale if needed
data = Dataset.load_from_df(df_cf[['patient_id', 'drugName', 'rating']], reader)
trainset = data.build_full_trainset()

# %%
# Check if the model exists, otherwise train and save it
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
else:
    model = SVD()
    cross_validate(model, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    model.fit(trainset)
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved!")

# %%
# Get all drugs and users
all_drugs = df_cf['drugName'].unique()
all_users = df_cf['patient_id'].unique()

def recommend_svd(user_id, user_condition, review_text=None, top_n=5):
    # Convert the user-provided condition to lowercase
    user_condition = user_condition.lower()

    # Step 1: Get all drugs used for this condition
    drugs_for_condition = df[df['condition'] == user_condition]['drugName'].unique()
    
    # Step 2: Filter out drugs the user has already rated
    rated = df_cf[df_cf['patient_id'] == user_id]['drugName'].tolist()
    unrated = [drug for drug in drugs_for_condition if drug not in rated]

    if not unrated:
        return pd.DataFrame([{
            'drugName': 'No new drugs to recommend',
            'collab_score': 0,
            'condition': user_condition,
            'predicted_sentiment': 'N/A',
            'patient_id': user_id
        }])
    
    # Step 3: Predict ratings for unrated drugs
    predictions = [(drug, model.predict(user_id, drug).est) for drug in unrated]

    # Step 4: Predict ratings
    top_recs = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]
    recs_df = pd.DataFrame(top_recs, columns=["drugName", "collab_score"])

    # Step 5: Add positive review explanations
    explanation_df = df[(df['predicted_sentiment'] == 'Positive') & (df['condition'] == user_condition)].drop_duplicates(subset='drugName')

    enriched_recs = recs_df.merge(
        explanation_df[['drugName', 'condition', 'review', 'predicted_sentiment']],
        on='drugName',
        how='left'
    )

    # Fill missing explanation fields
    enriched_recs['condition'] = enriched_recs['condition'].fillna(user_condition)
    enriched_recs['review'] = enriched_recs['review'].fillna(review_text if review_text else "No review available")
    enriched_recs['predicted_sentiment'] = enriched_recs['predicted_sentiment'].fillna("N/A")
    
    # Add user ID column
    enriched_recs['patient_id'] = user_id

    # Save collaborative scores to a separate CSV
    if os.path.exists(COLLAB_CSV_PATH):
        enriched_recs[['patient_id', 'drugName', 'condition', 'collab_score', 'review', 'predicted_sentiment']].to_csv(COLLAB_CSV_PATH, mode='a', header=False, index=False)

    else:
        enriched_recs[['patient_id', 'drugName', 'condition', 'collab_score', 'review', 'predicted_sentiment']].to_csv(COLLAB_CSV_PATH, index=False)

    return enriched_recs

# %%
def hybrid_model_recommendation(patient_id, condition, top_n=5):
    import pandas as pd

    condition = condition.lower()
    patient_id = str(patient_id)  # Ensure input is string

    # Load all with patient_id as string
    collab_df = pd.read_csv(COLLAB_CSV_PATH, dtype={'patient_id': str})
    content_df = pd.read_csv(CONTENT_CSV_PATH, dtype={'patient_id': str})
    sentiment_df = pd.read_csv(DRUG_REVIEWS_PATH, dtype={'patient_id': str})

    # Normalize condition to lowercase
    collab_df['condition'] = collab_df['condition'].str.lower()
    content_df['condition'] = content_df['condition'].str.lower()
    sentiment_df['condition'] = sentiment_df['condition'].str.lower()

    # Merge content + sentiment
    content_with_sentiment = pd.merge(
        content_df, sentiment_df,
        on=["patient_id", "drugName",'review', "condition","predicted_sentiment"],
        how="left"
    )

    # Merge content+sentiment with collaborative
    hybrid_df = pd.merge(
        collab_df, content_with_sentiment,
        on=["patient_id", "drugName",'review', "condition","predicted_sentiment"],
        how="outer"
    )

    # Clean up
    hybrid_df = hybrid_df.drop(columns=['Unnamed: 0'], errors='ignore')
    hybrid_df = hybrid_df.dropna(subset=['collab_score', 'content_score'], how='all')

    # Fill NaNs and scale
    hybrid_df['collab_score'] = hybrid_df['collab_score'].fillna(hybrid_df['collab_score'].mean())
    hybrid_df['content_score'] = hybrid_df['content_score'].fillna(hybrid_df['content_score'].mean())
    hybrid_df['content_score'] *= 10

    # Final filtering
    df = hybrid_df[
        (hybrid_df['patient_id'] == patient_id) &
        (hybrid_df['condition'] == condition)
    ]

    if df.empty:
        print("⚠️ No matching records found.")
        return pd.DataFrame()

    df = df.drop_duplicates(subset=['drugName'])

    df['hybrid_score'] = 0.7 * df['collab_score'] + 0.3 * df['content_score']

    return df.sort_values('hybrid_score', ascending=False)[
        ['drugName', 'hybrid_score', 'review','condition', 'predicted_sentiment', 'collab_score', 'content_score']
    ].head(top_n).reset_index(drop=True)


# %%




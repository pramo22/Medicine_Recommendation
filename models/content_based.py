# %%
import pickle
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# %%
# Load models
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')


# %%
# Load preprocessed data (includes sentiment!)
with open("models/content_data.pkl", "rb") as f:
    data = pickle.load(f)
    df = data["df"]
    review_embeddings = data["embeddings"]

# %%
def recommend_with_positive_sentiment(condition, review_text, patient_id, top_n=5):
    user_sentiment = 'Positive' if "not" not in review_text.lower() else 'Negative'  # basic fallback if needed
    user_input = f"{condition} {review_text} {user_sentiment} 10"

    user_embedding = sbert_model.encode([user_input])[0]
    cosine_scores = cosine_similarity([user_embedding], review_embeddings).flatten()
    df['content_score'] = cosine_scores

    filtered = df[
        (df['condition'].str.lower() == condition.lower()) &
        (df['predicted_sentiment'] == 'Positive')
    ].copy()

    top_results = filtered.sort_values(by='content_score', ascending=False).head(top_n)
    top_results['patient_id'] = str(patient_id)
    path="data\\content_scores.csv"
    if os.path.exists(path):
        top_results[['patient_id', 'drugName', 'condition', 'content_score','review','predicted_sentiment']].to_csv(path, mode='a', header=False, index=False)
    else:
        top_results[['patient_id', 'drugName', 'condition', 'content_score','review','predicted_sentiment']].to_csv(path, index=False)
    return top_results[['patient_id', 'drugName', 'condition', 'review', 'rating', 'content_score','predicted_sentiment',]]

# %%



# %%

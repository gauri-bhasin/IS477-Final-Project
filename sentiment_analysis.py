import os
import re
import numpy as np
import pandas as pd
from textblob import TextBlob

# ---------- CONFIG / PATHS ----------

INPUT_CSV = "spotify_with_lyrics.csv"
TRACK_OUTPUT_CSV = "spotify_with_lyrics_and_sentiment.csv"
SUMMARY_OUTPUT_CSV = "artist_year_sentiment_summary.csv"

# ---------- LOAD MERGED DATA ----------

if not os.path.exists(INPUT_CSV):
    raise FileNotFoundError(
        f"{INPUT_CSV} not found. Run collect_and_clean_dataset.py first "
        "to create spotify_with_lyrics.csv."
    )

print(f"Loading merged Spotify + lyrics data from {INPUT_CSV} ...")
merged = pd.read_csv(INPUT_CSV)
print("Merged shape:", merged.shape)

# ---------- LYRICS CLEANING ----------

def clean_lyrics(text):
    """
    Basic cleaning like handling NaNs remove line breaks and extra spaces.
    No aggressive cleaning here because sentiment models
    like to see natural language.
    """
    if pd.isna(text):
        return ""
    text = str(text)
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

print("Cleaning lyrics (creating lyrics_clean column)...")
merged["lyrics_clean"] = merged["lyrics"].apply(clean_lyrics)

# ---------- SENTIMENT ANALYSIS (TEXTBLOB) ----------

def get_sentiment(text):
    """
    Use TextBlob to compute sentiment.
    - polarity: -1.0 (negative) to +1.0 (positive)
    - subjectivity: 0.0 (objective) to 1.0 (subjective)
    """
    if not text or text.strip() == "":
        return pd.Series({
            "sent_polarity": np.nan,
            "sent_subjectivity": np.nan
        })
    blob = TextBlob(text)
    return pd.Series({
        "sent_polarity": blob.sentiment.polarity,
        "sent_subjectivity": blob.sentiment.subjectivity
    })

print("Computing sentiment scores (this may take a bit)...")
sent_scores = merged["lyrics_clean"].apply(get_sentiment)
merged = pd.concat([merged, sent_scores], axis=1)

# ---------- LABEL SENTIMENT (POS / NEG / NEUTRAL) ----------

def label_sentiment(polarity, pos_thresh=0.05, neg_thresh=-0.05):
    """
    Convert continuous polarity score to a simple label.
    Thresholds are small so that slightly positive/negative songs
    get counted as positive/negative.
    """
    if pd.isna(polarity):
        return "unknown"
    if polarity >= pos_thresh:
        return "positive"
    if polarity <= neg_thresh:
        return "negative"
    return "neutral"

print("Assigning sentiment labels...")
merged["sent_label"] = merged["sent_polarity"].apply(label_sentiment)

# ---------- RELEASE YEAR EXTRACTION ----------

def extract_year(date_str):
    """
    Spotify release_date can be 'YYYY' 'YYYY-MM' or 'YYYY-MM-DD'
    We just take the first 4 chars if possible
    """
    try:
        return int(str(date_str)[:4])
    except Exception:
        return np.nan

print("Extracting release_year from release_date...")
merged["release_year"] = merged["release_date"].apply(extract_year)

# ---------- SAVE TRACK-LEVEL DATA WITH SENTIMENT ----------

print(f"Saving track-level sentiment data to {TRACK_OUTPUT_CSV} ...")
merged.to_csv(TRACK_OUTPUT_CSV, index=False)

# ---------- ARTIST-YEAR SENTIMENT SUMMARY ----------

print("Aggregating sentiment by artist_name and release_year...")

artist_year_sent = (
    merged
    .groupby(["artist_name", "release_year"])
    .agg(
        mean_polarity=("sent_polarity", "mean"),
        mean_subjectivity=("sent_subjectivity", "mean"),
        pos_share=("sent_label", lambda x: (x == "positive").mean()),
        neg_share=("sent_label", lambda x: (x == "negative").mean()),
        neu_share=("sent_label", lambda x: (x == "neutral").mean()),
        n_tracks=("track_id", "nunique")
    )
    .reset_index()
)

print(f"Saving artist-year sentiment summary to {SUMMARY_OUTPUT_CSV} ...")
artist_year_sent.to_csv(SUMMARY_OUTPUT_CSV, index=False)

print("Done with sentiment analysis!")

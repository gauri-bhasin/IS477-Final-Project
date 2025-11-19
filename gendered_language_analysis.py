import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt

INPUT_CSV = "spotify_with_lyrics_and_sentiment.csv"
OUTPUT_TRACK_CSV = "tracks_with_gendered_counts.csv"
OUTPUT_SUMMARY_CSV = "artist_year_gendered_summary.csv"
#First we load the data

if not os.path.exists(INPUT_CSV):
    raise FileNotFoundError("spotify_with_lyrics_and_sentiment.csv not found")

print("Loading dataset...")
df = pd.read_csv(INPUT_CSV)

print("Shape:", df.shape)

# Make sure lyrics column exists
if "lyrics_clean" not in df.columns:
    df["lyrics_clean"] = df["lyrics"].fillna("")

#Next we define the gendered terms into two lists

feminine_terms = [
    "she", "her", "hers", "girl", "girls", "woman", "women", 
    "lady", "ladies", "queen", "girlfriend", "mom", "mother"
]

masculine_terms = [
    "he", "him", "his", "boy", "boys", "man", "men",
    "guy", "guys", "king", "boyfriend", "dad", "father"
]

# compile regex for speed
fem_regex = re.compile(r"\b(" + "|".join(feminine_terms) + r")\b", re.IGNORECASE)
masc_regex = re.compile(r"\b(" + "|".join(masculine_terms) + r")\b", re.IGNORECASE)

#add a function to count terms

def count_terms(text):
    if pd.isna(text):
        text = ""
    text = str(text).lower()

    fem_count = len(fem_regex.findall(text))
    masc_count = len(masc_regex.findall(text))

    total_words = len(text.split())

    if total_words == 0:
        total_words = np.nan

    return pd.Series({
        "feminine_count": fem_count,
        "masculine_count": masc_count,
        "total_words": total_words,
        "feminine_norm": fem_count / total_words * 1000 if total_words else np.nan,
        "masculine_norm": masc_count / total_words * 1000 if total_words else np.nan
    })

# the numbers of terms counted are matched to the song 

print("Counting gendered terms (this may take a few seconds)...")
term_counts = df["lyrics_clean"].apply(count_terms)
df = pd.concat([df, term_counts], axis=1)


print("Aggregating by artist, year, and genre...")

grouped = (
    df.groupby(["artist_name", "release_year", "tag"])
    .agg(
        mean_feminine_norm=("feminine_norm", "mean"),
        mean_masculine_norm=("masculine_norm", "mean"),
        total_tracks=("track_id", "nunique")
    )
    .reset_index()
)


print("Saving track-level file:", OUTPUT_TRACK_CSV)
df.to_csv(OUTPUT_TRACK_CSV, index=False)

print("Saving artist-year summary:", OUTPUT_SUMMARY_CSV)
grouped.to_csv(OUTPUT_SUMMARY_CSV, index=False)

#Visualizations

print("Creating plots...")

for artist in grouped["artist_name"].unique():
    artist_df = grouped[grouped["artist_name"] == artist].sort_values("release_year")

    plt.figure(figsize=(10, 5))
    plt.plot(artist_df["release_year"], artist_df["mean_feminine_norm"], label="Feminine terms", marker="o")
    plt.plot(artist_df["release_year"], artist_df["mean_masculine_norm"], label="Masculine terms", marker="o")

    plt.title(f"Gendered Term Trends Over Time — {artist}")
    plt.xlabel("Year")
    plt.ylabel("Terms per 1000 Words")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filename = f"{artist}_gendered_trend.png".replace(" ", "_")
    plt.savefig(filename)
    plt.close()

    print(f"Saved plot: {filename}")

print("Analysis complete!")

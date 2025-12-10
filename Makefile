# End-to-end workflow: collection → sentiment → gendered language

.PHONY: all collect sentiment gendered clean

# Run the full pipeline
all: collect sentiment gendered

# 1. Collect & integrate Spotify + lyrics data
collect:
	python collect_and_clean_dataset.py

# 2. Run sentiment analysis
sentiment:
	python sentiment_analysis.py

# 3. Run gendered language analysis + plots
gendered:
	python gendered_language_analysis.py

# Optional: clean derived outputs (for fresh reruns)
clean:
	rm -f spotify_with_lyrics.csv \
	      spotify_with_lyrics_and_sentiment.csv \
	      artist_year_sentiment_summary.csv \
	      tracks_with_gendered_counts.csv \
	      artist_year_gendered_summary.csv \
	      Ariana_Grande_gendered_trend.png \
	      Drake_gendered_trend.png \
	      Ed_Sheeran_gendered_trend.png \
	      Taylor_Swift_gendered_trend.png

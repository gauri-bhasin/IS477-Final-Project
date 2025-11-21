# Status Report – Gender Representation in Music Lyrics Over Time

**Course:** IS 477  
**Team:** Gauri Bhasin & Krishna Damania  

## 1. Progress on Planned Tasks

This section follows the tasks and weeks from our original project plan.

### Week 1 – Collect Spotify and Genius datasets (Gauri)  
**Status:** Completed  

**What we did:**  
- Set up Spotify API authentication and collected track-level metadata (track ID, title, album, artist, release date, popularity) for four focal artists: **Taylor Swift, Drake, Ariana Grande, and Ed Sheeran**.  
- Downloaded the Genius + Kaggle lyrics dataset and identified the subset relevant for our artists.  

**Repository artifacts:**  
- `collect_and_clean_dataset.py` – script that pulls Spotify metadata and reads the lyrics dataset.  
- `spotify_tracks.csv` – exported Spotify track metadata.  
- `song_lyrics.csv` – external lyrics dataset referenced by the script (kept local / not fully committed because of copyright).


### Week 2 – Clean & preprocess text (Gauri)  
**Status:**  Completed  

**What we did:**  
- Normalized track titles and artist names (lowercasing, removing parentheses and extra punctuation) so that Spotify titles match Genius titles more reliably.  
- Filtered the lyrics dataset to:
  - English-language songs only, and  
  - Selected genre tags (pop / rap) to keep the focus consistent with our artists.  
- Chose a single “best” lyrics entry per song using view counts to avoid duplicates and remixes.

**Repository artifacts:**  
- `collect_and_clean_dataset.py` – normalization and filtering logic.  
- Intermediate processed lyrics stored in memory within the script; final merged result saved as `spotify_with_lyrics.csv` (see below).

---

### Week 3 – Integrate datasets (Gauri)  
**Status:** Completed  

**What we did:**  
- Joined Spotify metadata with the cleaned Genius lyrics using standardized artist and title fields.  
- Produced a combined dataset that includes, for each track, both:
  - Spotify information (release date, popularity, etc.), and  
  - Lyrics and basic Genius metadata (year, tag, views, song ID).  

**Repository artifacts:**  
- `collect_and_clean_dataset.py` – merge step.  
- `spotify_with_lyrics.csv` – integrated Spotify + lyrics dataset.

---

### Week 4 – Sentiment analysis (Krishna)  
**Status:**  Completed  

**What we did:**  
- Created a separate script to perform sentiment analysis on the cleaned lyrics text.  
- Used **TextBlob** to assign, for each song:
  - A polarity score (negative to positive sentiment) and  
  - A subjectivity score (objective to subjective language).  
- Converted continuous polarity into simple categories: **positive**, **negative**, **neutral**, and **unknown** when lyrics are missing.  
- Extracted an explicit `release_year` field from the Spotify release date to support time-based analysis.  
- Created a summary table that aggregates sentiment by artist and year (average polarity and share of positive/negative/neutral songs).  

**Repository artifacts:**  
- `sentiment_analysis.py` – script for sentiment scoring and aggregation.  
- `spotify_with_lyrics_and_sentiment.csv` – track-level dataset with sentiment fields added.  
- `artist_year_sentiment_summary.csv` – artist–year level sentiment summary for visualizations.

---

### Week 5 – Gendered term frequencies & trends (Krishna)  
**Status:** Completed

**What we did:**  
- Analyzing gendered term frequencies and trends using the merged lyrics dataset:
  - Defined two dictionaries of gendered terms:
    - Feminine terms (e.g., “she”, “her”, “woman”, “girl”, etc.)
    - Masculine terms (e.g., “he”, “him”, “man”, “boy”, etc.)
  - Cleaned each song’s lyrics and computed:
    - Total word count
    - Count of feminine terms
    - Count of masculine terms
    - Normalized frequencies (e.g., feminine-terms-per-1000-words).
  - Aggregated gendered-language usage by:
    - Artist
    - Year
    - Genre
  - Generated time-series plots showing how masculine vs feminine term usage changed over time for major artists (Taylor Swift, Drake, Ariana Grande, Ed Sheeran).
**Repository artifacts:**  
- `gendered_language_analysis.py` – full script that performs gendered-term counting, normalization, aggregation, and plotting
- `tracks_with_gendered_counts.csv` – track-level dataset including feminine/masculine term counts and normalized rates
- `artist_year_gendered_summary.csv` – aggregated artist-year dataset summarizing gendered language frequencies
- `Ariana_Grande_gendered_trend.png`, `Drake_gendered_trend.png`, `Taylor_Swift_gendered_trend.png`, `Ed_Sheeran_gendered_trend.png`– visual trendlines showing masculine vs feminine language use over time.

---

### Week 6 – Automated reproducible workflow (Krishna)  
**Status:** Not started, should complete by 29th november

**Planned work:**  
- Organize scripts into a clear pipeline (data collection → cleaning → integration → sentiment → gendered language).  
- Add a simple workflow tool (Makefile or shell script) so the entire analysis can be reproduced end-to-end.  
- Add a `requirements.txt` describing Python dependencies.

---

### Week 7 – Final report and visualizations (Gauri & Krishna)  
**Status:** Not started: final week

**Planned work:**  
- Use the sentiment and gendered-language summaries to produce:
  - Time-series plots of sentiment over 2000–2025 by artist and later by artist gender.  
  - Visualizations of gendered term frequencies over time.  
- Draft the final written report (Markdown) describing:
  - Data lifecycle,
  - Methods,
  - Ethical considerations, and
  - Key findings.

---

### Week 8 – GitHub release and submission (Gauri)  
**Status:** Not started (future work)  

**Planned work:**  
- Clean up the repository structure, add documentation, and ensure no copyrighted full lyrics are exposed.  
- Provide clear instructions in the README for reproducing the analysis from scratch.  
- Prepare the final version of the repo for submission.

---

## 2. Updated Timeline and Task Status

| Week | Task                                                                                   | Responsible | Status        | Expected Completion |
|------|----------------------------------------------------------------------------------------|-------------|---------------|---------------------|
| 1    | Collect Spotify metadata and lyrics dataset                                            | Gauri       | **Done**      | Completed           |
| 2    | Clean & preprocess metadata and lyrics                                                 | Gauri       | **Done**      | Completed           |
| 3    | Integrate Spotify and lyrics datasets                                                  | Gauri       | **Done**      | Completed           |
| 4    | Run sentiment analysis and create sentiment summaries                                  | Krishna     | **Done**      | Completed           |
| 5    | Analyze gendered term frequencies and trends                                           | Krishna     | **Done**      |
| Completed         |
| 6    | Build automated, reproducible workflow                                                 | Krishna     | Not started   | Target: Nov 25      |
| 7    | Final visualizations + written report                                                  | Both        | Not started   | Target: Dec 5       |
| 8    | Final GitHub cleanup and project submission                                            | Gauri       | Not started   | Target: Dec 10      |

---

## 3. Changes to Project Plan

Since Milestone 2, we have made a few adjustments and clarifications to keep the project feasible and focused:

1. **Scope of artists and songs**  
   - Instead of trying to capture a very broad slice of Spotify, we restricted our analysis to four high-profile artists (Taylor Swift, Drake, Ariana Grande, Ed Sheeran).  
   - This keeps API calls and lyrics integration manageable while still giving us a meaningful comparison between male and female artists.

2. **Sentiment method choice**  
   - The original plan mentioned using TextBlob *or* a BERT-based model.  
   - After considering complexity and runtime, we decided to standardize on **TextBlob** as our primary sentiment engine for this project, and to treat model comparison as potential future work rather than a requirement.

3. **Lyrics sourcing**  
   - Instead of scraping the Genius API directly, we are primarily relying on the Kaggle Genius dataset as our lyrics source. This simplifies data collection and rate-limiting issues, and we continue to follow fair-use guidelines by only using lyrics text for analysis (no full re-publication in the report).

4. **Gender identification**  
   - We have not yet implemented an automated artist gender inference step. For this milestone the sentiment work is artist-agnostic; the gender dimension will be layered on in Week 5 and may combine manual labeling for our limited artist set with external reference sources.

Overall the core research question and analytical goals remain the same, but we have narrowed the technical scope to ensure we can finish the workflow and interpret the results in depth.

---

## 4. Individual Contributions (Milestone 3)

### Gauri Bhasin – Contribution Summary  
- Set up the Spotify API connection and collected track metadata for the selected artists.  
- Cleaned and normalized song titles and artist names.  
- Filtered and deduplicated the Genius lyrics dataset, and integrated it with Spotify metadata to create the combined `spotify_with_lyrics.csv` dataset.  
- Helped refine the project scope and plan based on earlier milestones.
- Provided feedback on sentiment analysis approach and results interpretation and helped with the gendered-language and timeline analyses.

### Krishna Damania – Contribution Summary  
- Implemented the sentiment analysis stage using the merged Spotify + lyrics dataset.  
- Designed and ran the TextBlob-based pipeline to generate track-level sentiment scores and categorical labels.  
- Produced the `spotify_with_lyrics_and_sentiment.csv` dataset and the `artist_year_sentiment_summary.csv` summary file for later visualization.  
- Completed the sentiment analysis results into gendered-language and timeline analyses.



# Gender Representation in Music Lyrics Over Time

## Contributors
- **Gauri Bhasin** (gaurib2)  
- **Krishna Damania** (kd21)  

Course: **IS 477 – Data Management, Curation & Reproducibility**

---

## Summary  *(Project Overview – ~500–1000 words)*

Popular music is one of the main ways people encounter stories about love, identity, power, and gender.  
This project investigates **how gender and sentiment are represented in song lyrics over time**, focusing on four highly visible artists between roughly **2010 and 2025**.

Our **primary research question** is:

> **Do songs by male and female artists differ in sentiment polarity and gender-related language over the past two decades?**

To answer this, we combine two main data sources:

- The **Spotify Web API** – to obtain track-level metadata such as track IDs, titles, artists, albums, release dates, and popularity scores.  
- A **Genius / Kaggle lyrics dataset** – to obtain full song lyrics and additional metadata such as genre tags, year, and page views.

We limit the scope to four popular artists who differ by gender and style:

- **Taylor Swift** (female; pop / country / pop-rock)  
- **Ariana Grande** (female; pop / R&B)  
- **Drake** (male; rap / pop-rap)  
- **Ed Sheeran** (male; pop / singer–songwriter)

This focused set keeps API calls and integration manageable while still enabling meaningful comparisons between male and female artists.

Our workflow has several stages:

1. **Data acquisition (Spotify + Genius).**  
   We authenticate with the Spotify Web API and collect track metadata for the four artists. We also download a large Genius-based lyrics dataset from Kaggle, which contains titles, artists, tags, views, language labels, and full lyrics.

2. **Cleaning, filtering, and integration.**  
   We normalize song titles and artist names (lowercasing, stripping parentheses, removing “- remix” style suffixes) and filter the lyrics dataset to English-language songs in relevant music genres (primarily pop and rap).  
   We then **merge** the Spotify and Genius data using standardized artist and title fields, selecting the highest-view lyrics entry per song to reduce duplicates and remixes.

3. **Sentiment analysis.**  
   Using **TextBlob**, we compute sentiment scores for each track’s lyrics, capturing  
   - **polarity** (−1 = very negative, +1 = very positive), and  
   - **subjectivity** (0 = objective, 1 = subjective).  
   We then convert polarity into discrete labels (**positive**, **negative**, **neutral**, **unknown**) and aggregate sentiment statistics by **artist** and **release year**.

4. **Gendered language analysis.**  
   We build dictionaries of explicitly gendered terms (for example, “she”, “her”, “girl”, “woman” versus “he”, “him”, “boy”, “man”) and count their occurrences in each song’s lyrics.  
   Term counts are **normalized by total word count** (occurrences per 1,000 words) so that long and short songs can be compared fairly.  
   We then aggregate these measures by **artist**, **year**, and **genre**, producing time-series views of how masculine vs. feminine language usage changes over time.

5. **Visualization and interpretation.**  
   Using the aggregated sentiment and gendered-language data, we generate:  
   - artist-level trend plots of mean sentiment polarity over time, and  
   - artist-level plots comparing feminine vs masculine word usage per year.  
   The gendered-language plots used in the report are saved as:
   - `Ariana_Grande_gendered_trend.png`  
   - `Drake_gendered_trend.png`  
   - `Ed_Sheeran_gendered_trend.png`  
   - `Taylor_Swift_gendered_trend.png`

Our end goal is a **reproducible, curated workflow** that documents each step—from data acquisition through cleaning, analysis, and visualization—so that others (including course staff) can re-run our pipeline and re-create the results using the same inputs.


## Data Profile  *(~500–1000 words)*

Our project uses two primary data sources plus several derived datasets.

### 1. Spotify Web API – Track Metadata

- **Source:** Spotify Web API  
- **Access method:** Authenticated calls using the `spotipy` Python library.  
- **Unit of observation:** Individual tracks for a given artist.  
- **Key fields used:**
  - `track_id` – unique identifier for each track  
  - `track_name`  
  - `album_name`  
  - `artist_name`  
  - `release_date` (year or full date)  
  - `popularity` (0–100 score)

- **Coverage:**  
  All tracks returned by Spotify for Taylor Swift, Ariana Grande, Drake, and Ed Sheeran, including albums and singles.

**Ethical / legal constraints:**  
Spotify’s API terms allow retrieval of metadata for research / educational purposes but do **not** allow redistribution of full audio or proprietary content. We only store and redistribute track **metadata**, not audio files, and our code respects authentication and rate-limit requirements.

### 2. Genius / Kaggle Lyrics Dataset

- **Source:** Genius lyrics compiled into a Kaggle dataset, stored locally as `song_lyrics.csv`.  
- **Access method:** Downloaded manually from Kaggle and stored in a **private Box folder**.  
- **Key fields used:**
  - `title`  
  - `artist`  
  - `tag` (genre, e.g., pop, rap)  
  - `year`  
  - `views` (page views)  
  - `lyrics` (full text)  
  - `language_cld3` (auto-detected language)  
  - `id` (song identifier)

**Ethical / legal constraints:**  
Full song lyrics are copyrighted. To comply with fair use and dataset terms:

- We **do not** publish full lyrics in the GitHub repository or report.  
- `song_lyrics.csv` is kept **outside** the repo in a private Box folder and is **not** committed to GitHub.  
- Downstream datasets only expose **derived features** (for example, term counts, sentiment scores, and normalized frequencies), not the original text.  

The Box folder holding `song_lyrics.csv` (and any large input data) is:

> `IS477-Final_data` – shared via:  
> **https://uofi.box.com/s/hkiubh09uycy102t19n5b5q3aj05953b**

Users should download `song_lyrics.csv` from this folder and place it in the project root (or the path described in the Reproducing section).

### 3. Integrated and Derived Datasets

We generate several intermediate and final datasets:

1. **`spotify_tracks.csv`**  
   - Output of the Spotify metadata collection step.  
   - Contains `track_id`, `track_name`, `album_name`, `artist_name`, `release_date`, and `popularity` for all tracks by the four focal artists.

2. **`spotify_with_lyrics.csv`**  
   - Integrated dataset produced by `collect_and_clean_dataset.py`.  
   - Includes, for each track, merged Spotify metadata and Genius fields (`lyrics`, `tag`, `year`, `views`, `id`), along with normalized `artist_norm` and `title_norm` keys used for joining.

3. **`spotify_with_lyrics_and_sentiment.csv`**  
   - Track-level dataset with added sentiment fields:  
     - `lyrics_clean` (lightly cleaned lyrics)  
     - `sent_polarity` (TextBlob polarity)  
     - `sent_subjectivity` (TextBlob subjectivity)  
     - `sent_label` (`positive`, `neutral`, `negative`, `unknown`)  
     - `release_year` (parsed from `release_date`)

4. **`tracks_with_gendered_counts.csv`**  
   - Track-level dataset with:  
     - total word counts  
     - feminine term counts and frequencies  
     - masculine term counts and frequencies  

5. **`artist_year_sentiment_summary.csv`**  
   - Aggregated by `artist_name` and `release_year`:  
     - mean polarity and subjectivity  
     - share of positive / negative / neutral songs  
     - `n_tracks` (number of tracks contributing to that year for that artist)

6. **`artist_year_gendered_summary.csv`**  
   - Aggregated by `artist_name` and `release_year`:  
     - feminine terms per 1,000 words  
     - masculine terms per 1,000 words  
     - `n_tracks` (number of tracks contributing)

These derived datasets are small enough to be included in the GitHub repository and are the main inputs for our visualizations.


## Data Quality  *(~500–1000 words)*

Our data quality work focuses on ensuring that:

1. We have the correct tracks for each artist.  
2. Merged records truly refer to the **same song** across Spotify and Genius.  
3. Analytical fields (sentiment and gendered-term counts) are computed from appropriately cleaned text.

### 1. Quality Checks on Spotify Metadata

- We verified each focal artist’s Spotify identity by manually inspecting a sample of returned albums and tracks.  
- We limited album types to `album` and `single` to reduce duplicates from compilations.  
- We de-duplicated track entries using Spotify’s unique `track_id`.  
- Basic sanity checks (for example, distribution of release years and popularity values) confirmed expected coverage of each artist’s discography.

### 2. Quality Checks on Lyrics Dataset

- We restricted lyrics to **English** using `language_cld3 == "en"`.  
- We filtered to `tag` in `{"pop", "rap"}` so that the lyrics correspond to the popular-music context of our selected artists.  
- For each `(artist_norm, title_norm)` pair we sorted by `views` in descending order and kept only the **most viewed** entry, treating it as the canonical version of that song’s lyrics. This step removes many near-duplicates, remixes, and alternate versions.

### 3. Normalization and Integration

To make Spotify and Genius compatible, we apply consistent normalization:

- **Title normalization (`normalize_title`):**  
  - lower-case  
  - remove anything inside parentheses (e.g., “(feat. X)”)  
  - remove trailing descriptors after a dash (e.g., “– Acoustic Version”)  
  - collapse multiple spaces and strip leading/trailing spaces

- **Artist normalization:**  
  - lower-case  
  - strip leading/trailing spaces

The merge is performed on `artist_norm` and `title_norm`. We manually inspected a sample of merged rows to ensure that the majority of matches represent the same song, and we accept that a small number of mismatches may remain (e.g., completely different songs sharing a generic title).

### 4. Text Cleaning for Analysis

For sentiment and gendered-term counting we apply **light text cleaning**:

- Replace line breaks with spaces.  
- Collapse sequences of whitespace into a single space.  
- Do **not** remove stopwords or apply stemming/lemmatization so that pronouns and functional words are preserved for analysis.

Gendered-term counting is done on simple tokenization (splitting on whitespace and basic punctuation), and counts are later normalized by total word count to allow cross-song comparison.

### 5. Known Limitations

- Some Spotify tracks have **no matching lyrics** in the Genius dataset, leading to missing lyrics (`NaN`) and `sent_label = "unknown"`. These tracks also contribute zero gendered-term counts.  
- The Genius dataset may not cover every track or may contain transcription errors; we do not manually correct lyrics.  
- Features / collaborations can blur artist attribution. In this project we focus on tracks where the focal artist appears as the main `artist_name`.  
- Sentiment models like TextBlob are sensitive to slang, irony, and figurative language, which are common in music lyrics. Sentiment results should therefore be interpreted as approximate indicators rather than exact psychological scores.

We document these limitations in comments and in this README so that downstream users interpret results cautiously and transparently.


## Findings  *(~500 words)*

This project produced two main analytical outputs:  
(1) **sentiment polarity patterns over time**, and  
(2) **gendered language usage** measured through normalized feminine and masculine term frequencies.  

The visualizations `Ariana_Grande_gendered_trend.png`, `Drake_gendered_trend.png`, `Ed_Sheeran_gendered_trend.png`, and `Taylor_Swift_gendered_trend.png` summarize gendered-language trends for each artist. Combined with the sentiment summaries in `artist_year_sentiment_summary.csv`, they reveal stylistic and thematic differences between these four artists.

### 1. Gendered Language Usage Over Time

#### Ariana Grande

Ariana Grande’s lyrics display **consistently higher masculine-term usage than feminine-term usage**, especially in the mid-2010s.  

- Masculine terms peak around **2016** at roughly **19 terms per 1,000 words**, followed by a noticeable decline.  
- Feminine terms stay low and stable across years, generally **below 4 terms per 1,000 words**.

**Interpretation:** Ariana’s lyricism often centers on **male subjects** (partners, crushes, exes), while explicitly feminine self-references are rarer and more stable over time.

#### Ed Sheeran

Ed Sheeran shows the **most variability** among the four artists.

- Feminine-term usage rises sharply after 2015, peaking **above ~17 terms per 1,000 words in 2019**.  
- Masculine-term usage forms a complementary pattern, with peaks around **2014** and **2024** and relatively lower values during 2019–2021.

**Interpretation:** Sheeran’s lyrics oscillate between different narrative perspectives. Later albums feature more frequent references to women and relationships framed from an emotionally expressive, often self-reflective standpoint.

#### Taylor Swift

Taylor Swift exhibits **clear, structured patterns** in gendered language.

- Masculine terms dominate early and mid-career years, with strong peaks around **2012** (roughly **21 terms per 1,000 words**) and **2018–2021** (≈15 per 1,000).  
- Feminine terms remain present but lower; they gradually increase again around **2024**.

**Interpretation:** Swift’s lyrics consistently foreground male subjects—consistent with relationship-centric storytelling—but the modest rise in feminine self-referencing in more recent work suggests increased focus on self-definition, reflection, and empowerment.

#### Drake

Drake’s gendered language frequencies are the **highest overall**.

- Feminine-term usage often **exceeds masculine-term usage**, with substantial surges in the **late 2000s / early 2010s** and again around **2021**.  
- Masculine terms show episodic spikes, but not as consistently high as feminine terms.

**Interpretation:** Drake frequently references women—sometimes as romantic interests, sometimes as broader archetypes—consistent with conventions in rap and R&B where women are central to narrative and status-oriented storytelling.

### 2. Comparative Patterns Across Artists

Across all four artists, several cross-cutting patterns emerge:

- **Feminine terms** are most prevalent in **Drake** and **Ed Sheeran**, and lowest and most stable in **Ariana Grande**. This suggests stylistic and genre-driven differences: male artists in pop/rap tend to reference women frequently, while female artists reference themselves explicitly somewhat less often.
- **Masculine terms** dominate in **Taylor Swift** and **Ariana Grande**, reflecting narratives oriented around male partners or love interests. Ed Sheeran shows alternating peaks, while Drake uses masculine references less frequently than feminine ones.
- All artists exhibit **non-linear, episodic changes** rather than gradual monotonic trends. Peaks in term frequencies loosely align with **album cycles**, suggesting that thematic emphasis is driven more by project-level creative direction than by slow, year-over-year drift.

### 3. Overall Interpretation

Overall, gendered language patterns reveal a strong relationship between **artist identity, genre conventions, and narrative perspective**:

- Male artists tend to **reference women heavily and variably**,  
- Female artists more consistently **reference men**, and  
- Feminine self-referencing among female artists remains relatively low but increases slightly in recent years, hinting at a shift toward autonomy and empowerment.

These findings complement the sentiment analysis: the polarity scores provide a background measure of emotional tone, while gendered term frequencies highlight **who** is being talked about and **how often**, offering a multidimensional view of gender in modern popular music.


## Future Work  *(~500–1000 words)*

Several extensions could deepen and generalize this project:

1. **Expand artist and genre coverage.**  
   Our analysis focuses on four very popular artists. Future work could:  
   - include a larger sample of male, female, and non-binary artists across pop, rap, R&B, and other genres;  
   - stratify artists by decade or popularity level to reduce selection bias.

2. **Richer modeling of gendered language.**  
   Our current dictionaries are pronoun- and noun-based (he/she, girl/boy, man/woman). Future work could:  
   - incorporate adjectives and phrases associated with gender roles or stereotypes;  
   - use word embeddings or contextual language models to identify words that are gender-coded even when they are not explicit pronouns.

3. **More advanced sentiment and emotion analysis.**  
   TextBlob is simple and interpretable but limited. Future work might:  
   - compare lexicon-based sentiment with transformer-based models (e.g., fine-tuned BERT);  
   - move beyond polarity to multi-label emotion analysis (anger, joy, sadness, desire, etc.).

4. **Contextual and demographic enrichment.**  
   We currently treat gender as a binary based on public artist identity. Future work could:  
   - incorporate non-binary or gender-fluid artists where appropriately documented;  
   - connect lyric trends to external events (album eras, public narratives, chart performance).

5. **Interactive dashboards and teaching tools.**  
   The derived datasets could power:  
   - a simple web dashboard where users select an artist and see sentiment and gendered-language trends;  
   - classroom examples for demonstrating responsible NLP in cultural analytics.

6. **Reproducible packaging and archival.**  
   Future versions could:  
   - provide a Dockerfile or similar environment container;  
   - publish the final code and derived datasets to an archival repository (e.g., Zenodo) with a DOI to create a pseudo-persistent research object.


## Reproducing the Analysis  *(Step-by-step workflow)*

This section explains how to reproduce our results using the code and data in this repository.

### 0. Prerequisites

- Python 3.10+  
- `git`  
- A command-line environment (PowerShell, bash, etc.)  
- (Optional for re-collecting metadata) Spotify developer credentials

Clone the repository:
- git clone https://github.com/gauri-bhasin/IS477-Final-Project.git
- cd IS477-Final-Project
Create and activate a virtual environment, then install dependencies:

##### bash
##### Copy code
- python -m venv venv

##### Windows PowerShell
venv\Scripts\Activate.ps1

##### macOS / Linux (if applicable)
##### source venv/bin/activate

- pip install -r requirements.txt
### 1. Obtain Input Data from Box
- From the Box folder IS477-Final_data (https://uofi.box.com/s/hkiubh09uycy102t19n5b5q3aj05953b):

- Download at least the following files:

- song_lyrics.csv (large, copyrighted lyrics dataset)

- spotify_tracks.csv (Spotify metadata collected once by the team)

- Place them in the project root (same directory as collect_and_clean_dataset.py).
Alternatively, you may also download the intermediate CSVs for inspection, but they will be recreated by the scripts.

##### Note: You do not need your own Spotify credentials. The script is configured to reuse the provided spotify_tracks.csv rather than calling the API again.

### 2. Collect, Clean, and Integrate Data
- Run:

##### bash
##### Copy code
- python collect_and_clean_dataset.py
This will:

- Load spotify_tracks.csv and song_lyrics.csv.

- Filter the lyrics dataset to English and relevant genres.

- Normalize artist and title fields.

- Deduplicate lyrics by (artist_norm, title_norm) using highest views.

- Merge Spotify + Genius data.

##### Output:

spotify_with_lyrics.csv

###### (If USE_SPOTIFY_API inside the script remains set to False, it will not call the Spotify API or require config.py.)

### 3. Sentiment Analysis
Run:

##### bash
##### Copy code
python sentiment_analysis.py

This will:

- Read spotify_with_lyrics.csv.

- Clean lyrics into lyrics_clean.

- Compute TextBlob sentiment scores and subjectivity.

- Assign a categorical sentiment label (sent_label).

- Extract release_year from release_date.

Outputs:

- spotify_with_lyrics_and_sentiment.csv

- artist_year_sentiment_summary.csv

### 4. Gendered Language Analysis
Run:

##### bash
##### Copy code
python gendered_language_analysis.py
This will:

- Load spotify_with_lyrics_and_sentiment.csv.

- Count feminine vs. masculine term occurrences and normalize by word count.

- Aggregate counts by artist and year.

- Generate visualizations.

- Outputs:

- tracks_with_gendered_counts.csv

- artist_year_gendered_summary.csv

- Ariana_Grande_gendered_trend.png

- Drake_gendered_trend.png

- Ed_Sheeran_gendered_trend.png

- Taylor_Swift_gendered_trend.png

### 5. Optional: Single-Command Workflow
For convenience, we also provide:

run_all.py – a small orchestration script that sequentially runs the three core steps.

Usage:

##### bash
##### Copy code
python run_all.py
Assuming the CSVs from Box are in place and dependencies are installed, this will recreate all processed datasets and plots end-to-end.

##### (An optional Makefile is included for users who have make installed, but it is not required for grading.)

## Environment & Dependencies
Programming language: Python 3.11

##### Key libraries:

- pandas – data manipulation

- numpy – numerical operations

- textblob – sentiment analysis

- matplotlib – visualization

- spotipy – Spotify Web API client (used only for original data collection)

All dependencies are listed in requirements.txt.
The project was developed and tested on Windows using a local virtual environment.

## License and Data Use
##### Code (Python scripts, run_all.py, Makefile):
Intended to be released under the MIT License (per course guidelines and team preference).

##### Derived datasets and plots (spotify_with_lyrics_and_sentiment.csv, tracks_with_gendered_counts.csv, *_gendered_trend.png, etc.):
Shared for educational and research purposes only within the scope of IS 477.

##### Lyrics data (song_lyrics.csv) and any text fields containing full lyrics:
Remain copyrighted by the original rights holders and by Genius.
These files are kept outside GitHub and shared privately via Box only with course staff.

## References (APA 7 style)
##### Note: Exact dataset titles may vary slightly; citations reflect the sources actually used.

- Kaggle. (n.d.). Genius song lyrics dataset [Data set]. Kaggle. https://www.kaggle.com/

- Loria, S. (n.d.). TextBlob: Simplified text processing for Python [Computer software]. https://textblob.readthedocs.io/

- Spotify. (n.d.). Spotify for Developers: Web API [Web API documentation]. https://developer.spotify.com/documentation/web-api

##### Additional course readings and lecture materials on data curation, reproducibility, and NLP informed the design of this project.

## Contribution Statement
##### Gauri Bhasin

- Set up the Spotify API connection and collected track metadata for the selected artists.

- Cleaned and normalized song titles and artist names.

- Filtered and deduplicated the Genius lyrics dataset, and integrated it with Spotify metadata to create spotify_with_lyrics.csv.

- Helped refine the project scope and project plan.

- Contributed to interpretation of sentiment and gendered-language results and to report writing.
- Helped design the automated workflow (run_all.py, Makefile) and contributed to report writing and interpretation.

##### Krishna Damania

- Implemented the sentiment analysis stage using TextBlob on the merged dataset.
- Produced spotify_with_lyrics_and_sentiment.csv and artist_year_sentiment_summary.csv.
- Implemented the gendered language analysis, producing tracks_with_gendered_counts.csv, artist_year_gendered_summary.csv, and the gendered trend plots.


##### Both team members collaborated on the overall research design, framing of research questions, and final documentation of methods, ethics, limitations, and findings.

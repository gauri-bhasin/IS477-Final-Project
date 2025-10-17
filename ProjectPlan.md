# Gender Representation in Music Lyrics Over Time

### Question: Do songs by male and female artists differ in sentiment polarity and gender-related language over the past two decades?
 #### Datasets:
Spotify API (track metadata, artists, release year)
Lyrics dataset (Kaggle “Lyrics Genius” or Genius API)
 #### Integration: 
 Album track + artist name
 #### Enrichment: 
 NLP sentiment/gendered pronoun analysis
 #### Ethics: 
 Copyright/licensing for lyrics datasets
### Compare male vs. female artists using sentiment and gendered word frequency.

### Overview
This project studies the representation of sentiment and gender in popular music between 2000 and 2025. Through an integration of song metadata collected from the Spotify API with lyrical data taken from the Genius Lyrics dataset, this research endeavors to analyze the intersection of gender and sentiment in modern music. Employing the branch of natural language processing (NLP) methods, this project will determine emotional tone-related trends, gendered language trends, and artist demographics during the relevant timeframe. Aims to have a clear and reproducible workflow that emphasizes linguistic and cultural shifts in how male and female artists exhibit their identities and depict gender in lyrics.

## Research Question(s)
### Primary Question:
Do songs by male and female artists differ in sentiment polarity and gender-related language over the past two decades?
#### Sub-questions:
How has lyrical sentiment (positive, negative, neutral) evolved for male vs. female artists between 2000–2025?
Which gendered terms (e.g., “he,” “she”) appear most frequently by artist gender and year?
Is there a noticeable shift toward more empowering or emotional expression across decades?
### Team
#### Role for Gauri Bhasin: 
Responsible for 2 stages of the data lifecycle, including acquisition, integration, and documentation.


#### Role for Krishna Damania: 
Responsible for 2 stages of the data lifecycle, including analysis and documentation.


### Responsibilities:


- Collect datasets via Spotify API and Genius Lyrics dataset
- Conduct NLP-based sentiment and gender term analysis
- Manage GitHub repository, version control, and workflow automation
- Prepare Markdown reports, visualizations, and final project documentation
### Datasets
## Spotify API
- Access Method: Using https://developer.spotify.com/documentation/web-api
- Attributes: Song title, artist name, release year, popularity, genre, artist gender (derived from Spotify metadata)
Purpose: Provides structured metadata for linking and temporal analysis


## Genius Lyrics Dataset (Kaggle or LyricsGenius API)
- Access Method: Kaggle download or LyricsGenius API
- Attributes: Song title, artist name, lyrics text

### Purpose: 
Provides unstructured text data for NLP analysis
- Integration:
 - The datasets will be merged on album track + artist name using fuzzy matching to handle slight naming variations.
- Format Difference:
 - Spotify → JSON (API)
 - Genius → CSV or scraped text (structured post-processing
 

### Timeline
##Phase(Done By) | Task | Module Alignment | Target Date
- Week 1(Gauri) : Collect Spotify and Genius datasets | In Modules 3–4 by  Oct 17- Oct 20

- Week 2(Gauri) : Clean & preprocess text (remove punctuation, normalize casing, etc.)| Module 10 by Oct 25
- Week 3(Gauri) : Integrate datasets (title + artist matching) | Modules 7–8 by Nov 5
- Week 4(Krishna) : Conduct sentiment analysis (TextBlob or BERT model) | Module 6 by Nov 10
- Week 5(Krishna) : Analyze gendered term frequencies and trends | Modules 9–10 by Nov 20
- Week 6(Krishna) : Build automated reproducible workflow (Jupyter + Makefile/Script) | Modules 11–12 by Nov 25
- Week 7(Gauri and Krishna) : Prepare final report and visualizations | Modules 13–15 by Dec 5
- Week 8(Gauri) : GitHub release and project submission | Final by Dec 10           


### Constraints
- Licensing: Genius lyrics are subject to copyright laws and only permitted to have limited quotes or modified content released (like word frequency).
- APIs: Spotify API rate limiting may slow down data collection.
- Gender identification: Not all genders of artists are represented in metadata; may require sources in second step.
- Sentiment accuracy: NLP sentiment models may misinterpret sarcasm, slang, or figurative lyrics.

### Gaps
- Need to determine the best artist gender inference algorithm (possibly via an ancillary dataset).
- The definition of "gendered language" will require fine-tuning, such as pronoun usage frequency compared to overall thematic terms.
- Some older songs may not appear on Spotify or Genius APIs, a sampling strategy will be required.


### Ethical Considerations
- Copyright: All lyrics given here shall adhere to fair-use clauses and no full lyrics will be republished.
- Representation: No analysis will indulge in stereotypes, results will highlight linguistic patterns and not personality traits.
- Transparency: All code and documentation should be transparent and reproducible on GitHub.

### Anticipated Outcomes
- A visual dashboard showing sentiment and gendered language trends (2000–2025).
- Markdown-based final report describing lifecycle stages, methods, and ethical review.
- Fully reproducible GitHub repository with scripts for data collection, integration, and analysis.


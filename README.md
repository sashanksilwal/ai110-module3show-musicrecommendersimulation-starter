# Music Recommender Simulation

A Python-based music recommender that scores and ranks songs from a 20-song catalog based on user taste profiles. It supports multiple scoring strategies, a diversity penalty, and transparent explanations for every recommendation.

---

## How The System Works

### Song Features
Each song has: genre, mood, energy (0-1), tempo, valence (positivity), danceability, acousticness, popularity (0-100), decade, and a detailed mood tag (e.g., "euphoric", "nostalgic").

### User Profile
A user profile stores: favorite genre, favorite mood, target energy level, acoustic preference, preferred decade, and preferred mood tag.

### Algorithm Recipe
The recommender scores every song in the catalog against the user profile:

- **Genre match**: +3.0 points (exact match)
- **Mood match**: +2.0 points (exact match)
- **Energy similarity**: up to +1.0 point (proportional to closeness)
- **Acoustic preference**: up to +1.0 point (high acousticness if user likes acoustic, low if not)
- **Valence**: +0.5 * valence score
- **Danceability**: +0.5 * danceability score
- **Popularity bonus**: +0.3 * (popularity / 100)
- **Decade match**: +1.0 point
- **Mood tag match**: +1.5 points

Songs are sorted by score, highest first. A **diversity penalty** reduces scores for songs whose artist or genre already appears in the top results.

### Scoring Modes
Four strategies with different weight distributions:
- **Balanced** (default) — even weighting across all features
- **Genre-First** — genre match worth 5.0, other features reduced
- **Mood-First** — mood match worth 5.0, mood tag worth 3.0
- **Energy-Focused** — energy similarity worth 5.0, danceability boosted

### Data Flow
```
User Profile → Score every song → Sort by score → Apply diversity penalty → Return top K
```

### Potential Biases
- The system might over-prioritize genre since it has the highest base weight
- Exact string matching means "indie pop" ≠ "pop", missing related genres
- Small catalog size limits recommendation quality

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Experiments Tried

### Scoring Mode Comparison
Ran the "High-Energy Pop Fan" profile across all four scoring modes:
- **Balanced**: Sunrise City #1, Gym Hero #2 — both pop songs ranked highest
- **Genre-First**: Same top 2 but much larger gap to non-pop songs (8.03 vs 3.62)
- **Mood-First**: Fuego Eterno (latin/happy) jumped to #1 because mood weight dominated genre
- **Energy-Focused**: Songs clustered tightly in score since most high-energy songs scored similarly

### Diversity Penalty Test
Compared results with and without the diversity penalty. In the lofi profile, LoRoom appeared twice — the penalty correctly reduced the second song's ranking to promote variety.

### Edge Case: Conflicting Preferences
A profile with high energy (0.95) but chill mood produced a mixed list — the system balanced both signals rather than crashing or ignoring one, showing graceful degradation.

---

## Limitations and Risks

- Only works on a 20-song catalog — too small for real use
- Does not understand lyrics, language, or cultural context
- Exact genre matching misses related genres (indie pop ≠ pop)
- Popularity bonus creates a feedback loop favoring already-popular tracks
- Single energy/mood values can't capture how taste changes by context (morning vs. workout)
- Dataset skews toward Western, English-language music from 2010s-2020s

---

## Reflection

[**Model Card**](model_card.md)

Building this recommender showed how sensitive outputs are to weight choices. A small change — like doubling the mood weight — completely reshuffles the ranking. This means the people who set the weights have enormous power over what users discover.

The project also highlighted how data composition creates implicit bias. With only 1 classical song and 3 pop songs, the system structurally favors pop listeners. Real-world recommenders face the same problem at scale — genres with less training data get worse recommendations, creating a cycle where underrepresented music stays underrepresented. Human oversight in data curation and weight design remains essential even when the algorithm itself is "fair."

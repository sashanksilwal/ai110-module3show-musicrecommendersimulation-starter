# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system suggests 3-5 songs from a small catalog based on a user's preferred genre, mood, energy level, acoustic preference, decade, and mood tag. It supports multiple scoring strategies (balanced, genre-first, mood-first, energy-focused) and includes a diversity penalty to avoid repetitive recommendations. It is designed for classroom exploration only, not for real users.

---

## 3. How the Model Works

The recommender compares each song in the catalog to a user's taste profile. It checks whether the song's genre and mood match the user's favorites, how close the song's energy level is to the user's target, and whether the song has acoustic qualities the user prefers. It also considers popularity, decade, and detailed mood tags.

Each matching feature earns points according to configurable weights. For example, in "balanced" mode a genre match is worth 3 points and a mood match is worth 2 points. The energy score is proportional to how close the song's energy is to the target — a perfect match earns the full weight, and a large gap earns close to zero.

After scoring, all songs are ranked from highest to lowest. A diversity penalty reduces the score of songs whose artist or genre already appears in the top results, preventing the list from being dominated by one sound.

---

## 4. Data

The catalog contains 20 songs in `data/songs.csv`. The original 10 songs covered pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Ten additional songs were added to cover hip-hop, R&B, classical, electronic/EDM, country, metal, latin, funk, soul, and reggae.

Each song has numerical features (energy, tempo, valence, danceability, acousticness), categorical features (genre, mood), and extended features (popularity 0-100, decade, and a detailed mood tag like "euphoric" or "nostalgic").

The dataset mostly reflects mainstream Western music tastes. Genres like K-pop, Afrobeats, and Bollywood are absent. The catalog is too small to represent the diversity of any single genre.

---

## 5. Strengths

- For users with clear preferences (e.g., "chill lofi" or "intense rock"), the top results feel accurate and intuitive.
- The explanation system makes the scoring transparent — users can see exactly why each song was recommended and how many points each feature contributed.
- Multiple scoring modes let users explore different ranking philosophies without changing the data.
- The diversity penalty prevents the same artist from flooding the top results.

---

## 6. Limitations and Bias

- With only 20 songs, many user profiles will see the same songs repeatedly. A real system needs thousands of tracks.
- The scoring treats genre as an exact string match. A user who likes "indie pop" gets no credit for "pop" songs, even though the genres are closely related.
- The system does not understand lyrics, language, or cultural context. It cannot distinguish between a happy English pop song and a happy Spanish pop song beyond the genre label.
- Popularity is used as a bonus, which biases the system toward well-known tracks and could create a "filter bubble" where popular songs get recommended more, becoming even more popular.
- Energy and mood preferences are single values. Real listeners' tastes vary by time of day, activity, and emotional state.
- The dataset over-represents 2010s and 2020s music, so users who prefer older music get fewer matches.

---

## 7. Evaluation

Five user profiles were tested:
1. **High-Energy Pop Fan** — correctly ranked "Sunrise City" and "Gym Hero" at the top.
2. **Chill Lofi Listener** — correctly ranked lofi tracks highest, with acoustic songs also scoring well.
3. **Intense Rock Lover** — "Storm Runner" ranked first with a high score (10.14), as expected.
4. **Mellow Jazz & Soul** — "Coffee Shop Stories" ranked first. Other relaxed/acoustic songs followed logically.
5. **Edge Case (High Energy + Chill Mood)** — produced mixed results, showing the system can handle conflicting preferences by balancing both signals rather than failing.

A scoring mode comparison showed that switching from "balanced" to "mood-first" caused "Fuego Eterno" (a happy latin song) to jump to #1, ahead of the pop songs. This confirmed that the weights meaningfully change rankings.

The diversity penalty was tested by running with and without it — in this catalog the effect was modest since few artists have multiple songs, but it correctly penalized LoRoom's second appearance in the lofi profile results.

---

## 8. Future Work

- Add support for multi-genre preferences (e.g., a user who likes both jazz and lofi).
- Implement collaborative filtering — "users who liked X also liked Y."
- Add a diversity slider so users can control how varied vs. focused their recommendations are.
- Support time-of-day context (morning = low energy, workout = high energy).
- Expand the catalog to 100+ songs to make the diversity penalty more impactful.
- Add fuzzy genre matching so "indie pop" partially matches "pop."

---

## 9. Personal Reflection

Building this recommender revealed how much a simple scoring system's behavior depends on the weights assigned to each feature. Doubling the genre weight makes the system feel like a genre filter; doubling the mood weight makes it feel like a playlist curator. Neither is objectively "right" — the choice reflects a design value about what matters most.

The most surprising finding was how much the small dataset size affects perceived quality. With only 20 songs, even a well-tuned algorithm produces lists where 3 out of 5 songs feel like compromises. This highlights why real recommender systems need massive catalogs.

This exercise also made clear how easily bias creeps in through data composition. If the catalog has 3 pop songs and 1 classical song, the system will appear to "prefer" pop simply because there are more candidates to match. Human judgment is still essential for curating training data, setting weights, and deciding when algorithmic recommendations should be overridden.

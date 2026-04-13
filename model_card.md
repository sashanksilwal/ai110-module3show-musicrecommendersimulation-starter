# Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

## 2. Intended Use

This is a toy recommender I built for a class assignment. You feed it a little user profile (favorite genre, favorite mood, target energy, whether you like acoustic stuff, and optionally a decade and mood tag) and it picks 5 songs from a 20-song catalog. It also tells you why it picked each one, which is honestly the whole point of the exercise. It's meant for classroom exploration and is definitely not something you'd ship to real users.

## 3. How the Model Works

For every song in the catalog, the recommender checks how well it lines up with your profile and hands out points. If the genre matches your favorite it gets a big chunk of points. Same for mood. Then it looks at how close the song's energy is to your target and gives partial credit depending on how close. If you said you like acoustic music, acoustic songs get a boost. If you didn't, non-acoustic songs get a boost instead. Smaller points come from valence (how positive the song sounds), danceability, popularity, decade, and a more specific mood tag.

Every song ends up with a total score. The songs get sorted highest to lowest, and the top 5 come out the other end. There's also a little diversity step that docks points from songs when the same artist or genre has already appeared, so one artist can't take over the whole list.

There are four different "modes" you can pick from, and they just change the weights. Balanced spreads things out. Genre-first makes the genre match worth way more than anything else. Mood-first does the same for mood. Energy-focused leans heavily on matching the energy level. Same data, different priorities.

## 4. Data

The catalog lives in `data/songs.csv` and has 20 songs. The starter came with 10, and I added 10 more to get a wider mix. The 20 now cover pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, R&B, classical, electronic, country, metal, latin, funk, soul, and reggae.

Each song has numerical features like energy, tempo, valence, danceability, and acousticness, plus categorical ones like genre and mood. I also added three more fields: a popularity score from 0 to 100, a decade, and a detailed mood tag like "euphoric" or "nostalgic".

The dataset leans pretty heavily toward mainstream Western music. There's no K-pop, no Afrobeats, no Bollywood, nothing in languages I don't listen to. And with only 20 songs, even the genres that are represented only get one or two tracks, so the catalog is really just a tiny slice.

## 5. Strengths

When the user profile is clear and unambiguous, the top results actually feel right. The chill lofi listener gets lofi songs. The intense rock lover gets Storm Runner at the top. The jazz and soul profile gets Coffee Shop Stories. That part works.

The explanations are probably the best feature. You can see exactly why each song was picked and how many points came from each feature. There's no mystery to any of it, which is nice for a classroom project where the whole idea is understanding how recommenders make decisions.

Having four scoring modes also makes it easy to see how the weights shape the output, without having to touch any code.

## 6. Limitations and Bias

The catalog is way too small. With only 20 songs, most profiles will keep seeing the same handful of tracks. A real recommender needs thousands or millions.

Genre matching is exact string comparison, which feels wrong. Someone who likes "indie pop" gets zero points for a regular "pop" song, even though those two things are obviously related. In reality genres should have some kind of similarity score, not a yes or no answer.

The model has no idea what lyrics are, what language a song is in, or what culture it comes from. A happy pop song in English and a happy pop song in Spanish look identical to it except for the genre label.

The popularity bonus is a bit of a trap. Already-popular songs get a tiny edge, and in a real system that kind of thing creates feedback loops where popular stuff keeps getting recommended and everything else gets buried.

Energy and mood are single numbers, but real taste isn't like that. What you want in the morning is different from what you want at the gym or what you want when you're falling asleep. None of that is captured.

And the dataset is skewed toward music from the 2010s and 2020s, so anyone who mostly listens to older stuff is going to get worse recommendations than someone whose taste happens to match what I put in the CSV.

## 7. Evaluation

I didn't calculate any fancy metrics, I just tried a bunch of user profiles and looked at whether the results made sense.

I tested five profiles: a high-energy pop fan, a chill lofi listener, an intense rock lover, a mellow jazz and soul listener, and a weird edge case that asked for high energy and a chill mood at the same time. The first four all produced top results that I thought looked right. The edge case was interesting because it's a contradictory profile and the system didn't crash, it just gave a mixed list that split the difference between the two signals.

I also ran the pop fan profile through all four scoring modes to see what changed. In balanced mode, two pop songs took the top spots. In mood-first mode, a latin song jumped to #1 because the mood match was weighted heavily enough to beat the genre mismatch. That was a good sanity check that the weights actually do what I thought they did.

Finally I ran the lofi profile with and without the diversity penalty to see if repeat artists got pushed down. They did, so the penalty works, even if the effect is small in such a tiny catalog.

## 8. Future Work

There's a lot I'd want to try if I had more time. Fuzzy genre matching is probably the first thing so that "indie pop" and "pop" share some similarity. Multi-genre user preferences would be good too, because nobody only listens to one genre.

Collaborative filtering would be a huge step up, where instead of comparing songs to profiles, the system learns from what similar users liked. A diversity slider so users can choose between "give me exactly what I asked for" and "surprise me a little" would be nice. Time-of-day context, where the system knows that morning you and workout you want different things, would make it feel much more alive.

And honestly just a bigger catalog. A lot of the current limitations go away once there are a few hundred songs instead of twenty.

## 9. Personal Reflection

The thing I didn't expect is how much the output depends on the weights. Same songs, same user, nudge one number, and the top 5 is completely different. That's kind of unsettling. Whoever picks the weights has a huge amount of control over what people end up listening to, and there's no objectively correct answer. It's a design choice that looks like a technical one.

The other thing that stuck with me is how bias creeps in through the data before the algorithm even runs. I have three pop songs and one classical song, so of course pop listeners get better recommendations. That's not the algorithm being unfair, it's the data being unbalanced. Scale that up to a real service and you can see how entire genres or communities get underrepresented and just stay that way.

It changed how I think about recommender apps. When Spotify or YouTube suggests something, there's a human somewhere who decided which features to use, what weights to give them, what data to train on, and what counts as a "good" recommendation. Those decisions are invisible but they shape everything. That feels like a place where human judgment still really matters, even when the model looks smart.

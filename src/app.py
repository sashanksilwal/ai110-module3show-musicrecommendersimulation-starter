"""
Streamlit UI for the Music Recommender Simulation.

Run with:
    streamlit run src/app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from src.recommender import load_songs, recommend_songs, SCORING_MODES


st.set_page_config(
    page_title="VibeFinder 1.0",
    page_icon="🎵",
    layout="wide",
)


@st.cache_data
def get_songs():
    return load_songs("data/songs.csv")


def main():
    songs = get_songs()

    st.title("🎵 VibeFinder 1.0")
    st.caption(
        "A tiny music recommender that picks songs from a 20-song catalog "
        "based on your taste profile, and tells you why it picked each one."
    )

    # ---- Sidebar: user profile ----
    st.sidebar.header("Your Taste Profile")

    all_genres = sorted({s["genre"] for s in songs})
    all_moods = sorted({s["mood"] for s in songs})
    all_decades = sorted({s["decade"] for s in songs})
    all_mood_tags = sorted({s["mood_tag"] for s in songs if s.get("mood_tag")})

    genre = st.sidebar.selectbox("Favorite genre", all_genres, index=all_genres.index("pop") if "pop" in all_genres else 0)
    mood = st.sidebar.selectbox("Favorite mood", all_moods, index=all_moods.index("happy") if "happy" in all_moods else 0)
    energy = st.sidebar.slider("Target energy level", 0.0, 1.0, 0.8, 0.05)
    likes_acoustic = st.sidebar.checkbox("I like acoustic sounds", value=False)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Optional preferences")
    decade = st.sidebar.selectbox("Preferred decade", ["(any)"] + all_decades)
    mood_tag = st.sidebar.selectbox("Preferred mood tag", ["(any)"] + all_mood_tags)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Settings")
    mode = st.sidebar.selectbox("Scoring mode", list(SCORING_MODES.keys()))
    k = st.sidebar.slider("Number of recommendations", 1, 10, 5)
    diverse = st.sidebar.checkbox("Apply diversity penalty", value=True)

    # ---- Build profile dict ----
    prefs = {
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "likes_acoustic": likes_acoustic,
        "decade": decade if decade != "(any)" else "",
        "mood_tag": mood_tag if mood_tag != "(any)" else "",
    }

    # ---- Get recommendations ----
    recs = recommend_songs(prefs, songs, k=k, mode=mode, diverse=diverse)

    # ---- Main display ----
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Top {k} Recommendations")
        st.caption(f"Using **{mode}** scoring mode" + (" with diversity penalty" if diverse else ""))

        if not recs:
            st.warning("No recommendations found.")
        else:
            for i, (song, score, explanation) in enumerate(recs, 1):
                with st.container():
                    left, right = st.columns([4, 1])
                    with left:
                        st.markdown(f"### {i}. {song['title']}")
                        st.markdown(
                            f"**{song['artist']}**  •  "
                            f"{song['genre']}  •  "
                            f"{song['mood']}  •  "
                            f"{song['decade']}"
                        )
                    with right:
                        st.metric("Score", f"{score:.2f}")

                    st.markdown("**Why this song:**")
                    for reason in explanation.split("; "):
                        st.markdown(f"- {reason}")

                    with st.expander("See song details"):
                        st.json({
                            "energy": song["energy"],
                            "tempo_bpm": song["tempo_bpm"],
                            "valence": song["valence"],
                            "danceability": song["danceability"],
                            "acousticness": song["acousticness"],
                            "popularity": song["popularity"],
                            "mood_tag": song.get("mood_tag", ""),
                        })
                    st.divider()

    with col2:
        st.subheader("Your profile")
        st.markdown(f"**Genre:** {genre}")
        st.markdown(f"**Mood:** {mood}")
        st.markdown(f"**Energy:** {energy:.2f}")
        st.markdown(f"**Acoustic:** {'yes' if likes_acoustic else 'no'}")
        if decade != "(any)":
            st.markdown(f"**Decade:** {decade}")
        if mood_tag != "(any)":
            st.markdown(f"**Mood tag:** {mood_tag}")

        st.markdown("---")
        st.subheader("Scoring weights")
        weights = SCORING_MODES[mode]
        for feature, weight in weights.items():
            st.markdown(f"- **{feature}**: {weight}")

        st.markdown("---")
        st.subheader("Catalog")
        st.markdown(f"**{len(songs)}** songs loaded")
        st.markdown(f"**{len(all_genres)}** unique genres")


if __name__ == "__main__":
    main()

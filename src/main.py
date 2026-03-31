"""
Command line runner for the Music Recommender Simulation.

Runs multiple user profiles across different scoring modes
and displays results in a formatted table.
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles for testing
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop", "mood": "happy", "energy": 0.85,
        "likes_acoustic": False, "decade": "2020s", "mood_tag": "euphoric",
    },
    "Chill Lofi Listener": {
        "genre": "lofi", "mood": "chill", "energy": 0.35,
        "likes_acoustic": True, "decade": "2020s", "mood_tag": "peaceful",
    },
    "Intense Rock Lover": {
        "genre": "rock", "mood": "intense", "energy": 0.92,
        "likes_acoustic": False, "decade": "2010s", "mood_tag": "aggressive",
    },
    "Mellow Jazz & Soul": {
        "genre": "jazz", "mood": "relaxed", "energy": 0.40,
        "likes_acoustic": True, "decade": "2010s", "mood_tag": "romantic",
    },
    "Edge Case: High Energy + Sad Mood": {
        "genre": "pop", "mood": "chill", "energy": 0.95,
        "likes_acoustic": False, "mood_tag": "melancholic",
    },
}


def print_table(recommendations, profile_name: str, mode: str) -> None:
    """Print recommendations as a formatted card layout with reasons on separate lines."""
    print()
    print("+" + "=" * 68 + "+")
    print(f"|  {'Profile:':<10} {profile_name:<55} |")
    print(f"|  {'Mode:':<10} {mode:<55} |")
    print("+" + "=" * 68 + "+")

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        title = song["title"]
        artist = song["artist"]
        genre = song["genre"]
        energy = song["energy"]
        mood = song["mood"]

        print(f"|                                                                    |")
        print(f"|  #{i}  {title:<40} Score: {score:>6.2f}  |")
        print(f"|       Artist: {artist:<25} Genre: {genre:<15} |")
        print(f"|       Mood: {mood:<12}  Energy: {energy:<5.2f}                      |")
        print(f"|       Reasons:                                                     |")
        reasons = explanation.split("; ")
        for reason in reasons:
            print(f"|         - {reason:<57} |")
        print(f"|  {'':·<66}  |")

    print("+" + "=" * 68 + "+")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")

    # --- Run each profile with the balanced mode ---
    for name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5, mode="balanced", diverse=True)
        print_table(recs, name, "balanced")

    # --- Scoring mode comparison for the first profile ---
    first_name = list(PROFILES.keys())[0]
    first_prefs = PROFILES[first_name]
    print("\n\n" + "#" * 80)
    print("  SCORING MODE COMPARISON")
    print("#" * 80)
    for mode in ["balanced", "genre-first", "mood-first", "energy-focused"]:
        recs = recommend_songs(first_prefs, songs, k=5, mode=mode, diverse=True)
        print_table(recs, first_name, mode)

    # --- Experiment: weight shift (genre halved, energy doubled) ---
    print("\n\n" + "#" * 80)
    print("  EXPERIMENT: What happens without diversity penalty?")
    print("#" * 80)
    recs_no_div = recommend_songs(first_prefs, songs, k=5, mode="balanced", diverse=False)
    print_table(recs_no_div, first_name, "balanced (no diversity)")


if __name__ == "__main__":
    main()

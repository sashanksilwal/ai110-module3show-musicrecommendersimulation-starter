import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    decade: str = "2020s"
    mood_tag: str = ""


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    preferred_decade: str = ""
    preferred_mood_tag: str = ""


# ---------------------------------------------------------------------------
# Scoring modes (Strategy pattern)
# ---------------------------------------------------------------------------

SCORING_MODES = {
    "balanced": {
        "genre": 3.0, "mood": 2.0, "energy": 1.0,
        "acoustic": 1.0, "valence": 0.5, "danceability": 0.5,
        "popularity": 0.3, "decade": 1.0, "mood_tag": 1.5,
    },
    "genre-first": {
        "genre": 5.0, "mood": 1.0, "energy": 0.5,
        "acoustic": 0.5, "valence": 0.3, "danceability": 0.3,
        "popularity": 0.2, "decade": 0.5, "mood_tag": 0.5,
    },
    "mood-first": {
        "genre": 1.0, "mood": 5.0, "energy": 1.0,
        "acoustic": 0.5, "valence": 0.8, "danceability": 0.3,
        "popularity": 0.2, "decade": 0.5, "mood_tag": 3.0,
    },
    "energy-focused": {
        "genre": 1.0, "mood": 1.0, "energy": 5.0,
        "acoustic": 0.5, "valence": 0.5, "danceability": 1.5,
        "popularity": 0.2, "decade": 0.0, "mood_tag": 0.5,
    },
}


def _score_song_for_user(
    user: UserProfile, song: Song, mode: str = "balanced"
) -> Tuple[float, List[str]]:
    """Score a song for a user and return (score, list_of_reasons)."""
    w = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if song.genre.lower() == user.favorite_genre.lower():
        score += w["genre"]
        reasons.append(f"genre match: {song.genre} (+{w['genre']:.1f})")

    # Mood match
    if song.mood.lower() == user.favorite_mood.lower():
        score += w["mood"]
        reasons.append(f"mood match: {song.mood} (+{w['mood']:.1f})")

    # Energy similarity (0 to weight)
    energy_diff = abs(song.energy - user.target_energy)
    energy_pts = max(0, w["energy"] * (1.0 - energy_diff))
    score += energy_pts
    if energy_diff <= 0.2:
        reasons.append(f"energy close to target (+{energy_pts:.1f})")

    # Acoustic preference
    if user.likes_acoustic:
        acoustic_pts = song.acousticness * w["acoustic"]
        score += acoustic_pts
        if song.acousticness > 0.6:
            reasons.append(f"acoustic sound (+{acoustic_pts:.1f})")
    else:
        acoustic_pts = (1.0 - song.acousticness) * w["acoustic"]
        score += acoustic_pts

    # Valence and danceability
    score += song.valence * w["valence"]
    score += song.danceability * w["danceability"]

    # Popularity bonus (normalized 0-1)
    pop_pts = (song.popularity / 100.0) * w["popularity"]
    score += pop_pts

    # Decade match
    if user.preferred_decade and song.decade == user.preferred_decade:
        score += w["decade"]
        reasons.append(f"decade match: {song.decade} (+{w['decade']:.1f})")

    # Mood tag match
    if user.preferred_mood_tag and song.mood_tag.lower() == user.preferred_mood_tag.lower():
        score += w["mood_tag"]
        reasons.append(f"mood tag match: {song.mood_tag} (+{w['mood_tag']:.1f})")

    if not reasons:
        reasons.append("general blend of qualities")

    return round(score, 2), reasons


# ---------------------------------------------------------------------------
# Diversity penalty helper
# ---------------------------------------------------------------------------

def _apply_diversity_penalty(
    scored_list: list, top_k: int
) -> list:
    """Re-rank results so no single artist or genre dominates the top-k."""
    selected = []
    artist_count: Dict[str, int] = {}
    genre_count: Dict[str, int] = {}

    for item in scored_list:
        if len(selected) >= top_k:
            break
        song = item[0]  # Song or dict
        artist = song.artist if isinstance(song, Song) else song["artist"]
        genre = song.genre if isinstance(song, Song) else song["genre"]

        penalty = 0.0
        if artist_count.get(artist, 0) >= 1:
            penalty += 1.5  # penalize repeat artist
        if genre_count.get(genre, 0) >= 2:
            penalty += 1.0  # penalize >2 songs of same genre

        adjusted_score = item[1] - penalty
        artist_count[artist] = artist_count.get(artist, 0) + 1
        genre_count[genre] = genre_count.get(genre, 0) + 1
        selected.append((item[0], adjusted_score, item[2]))

    selected.sort(key=lambda x: x[1], reverse=True)
    return selected


# ---------------------------------------------------------------------------
# OOP Recommender (used by tests)
# ---------------------------------------------------------------------------

class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(
        self, user: UserProfile, k: int = 5, mode: str = "balanced", diverse: bool = False
    ) -> List[Song]:
        scored = []
        for s in self.songs:
            sc, reasons = _score_song_for_user(user, s, mode)
            scored.append((s, sc, reasons))
        scored.sort(key=lambda x: x[1], reverse=True)

        if diverse:
            scored = _apply_diversity_penalty(scored, k)

        return [item[0] for item in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song, mode: str = "balanced") -> str:
        _, reasons = _score_song_for_user(user, song, mode)
        return "Recommended because: " + "; ".join(reasons) + "."


# ---------------------------------------------------------------------------
# Functional helpers (used by main.py)
# ---------------------------------------------------------------------------

def _dict_to_song(s: Dict) -> Song:
    """Convert a song dictionary to a Song dataclass."""
    return Song(
        id=s["id"], title=s["title"], artist=s["artist"],
        genre=s["genre"], mood=s["mood"], energy=s["energy"],
        tempo_bpm=s["tempo_bpm"], valence=s["valence"],
        danceability=s["danceability"], acousticness=s["acousticness"],
        popularity=s.get("popularity", 50),
        decade=s.get("decade", "2020s"),
        mood_tag=s.get("mood_tag", ""),
    )


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"] = int(row.get("popularity", 50))
            songs.append(row)
    return songs


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5,
    mode: str = "balanced", diverse: bool = True
) -> List[Tuple[Dict, float, str]]:
    """Score, rank, and return top-k songs with explanations."""
    user = UserProfile(
        favorite_genre=user_prefs.get("genre", ""),
        favorite_mood=user_prefs.get("mood", ""),
        target_energy=user_prefs.get("energy", 0.5),
        likes_acoustic=user_prefs.get("likes_acoustic", False),
        preferred_decade=user_prefs.get("decade", ""),
        preferred_mood_tag=user_prefs.get("mood_tag", ""),
    )

    scored = []
    for s in songs:
        song = _dict_to_song(s)
        sc, reasons = _score_song_for_user(user, song, mode)
        explanation = "; ".join(reasons)
        scored.append((s, sc, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    if diverse:
        scored = _apply_diversity_penalty(scored, k)

    return scored[:k]

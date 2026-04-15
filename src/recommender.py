from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of dictionaries."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = {
                'id': int(row['vaid']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': int(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences using weighted matching rules."""
    score = 0.0
    reasons = []

    # --- Genre match (+3.0) ---
    preferred_genres = user_prefs.get("preferred_genres", [])
    if song["genre"] in preferred_genres:
        score += 3.0
        reasons.append(f"genre match ({song['genre']}) (+3.0)")

    # --- Mood match (+2.0) ---
    preferred_moods = user_prefs.get("preferred_moods", [])
    if song["mood"] in preferred_moods:
        score += 2.0
        reasons.append(f"mood match ({song['mood']}) (+2.0)")

    # --- Energy within tolerance (0.0–2.0, linear decay) ---
    energy_target = user_prefs.get("energy_target", 0.5)
    energy_tolerance = user_prefs.get("energy_tolerance", 0.2)
    energy_diff = abs(song["energy"] - energy_target)
    if energy_diff <= energy_tolerance:
        energy_score = (1 - energy_diff / energy_tolerance) * 2.0
        score += energy_score
        reasons.append(
            f"energy match ({song['energy']:.2f} within {energy_target:.2f} ± {energy_tolerance:.2f}) (+{energy_score:.2f})"
        )

    # --- Valence similarity (0.0–1.5, optional) ---
    if "target_valence" in user_prefs:
        target_valence = user_prefs["target_valence"]
        valence_diff = abs(song["valence"] - target_valence)
        valence_score = max(0.0, (1 - valence_diff) * 1.5)
        score += valence_score
        reasons.append(
            f"valence match ({song['valence']:.2f} vs target {target_valence:.2f}) (+{valence_score:.2f})"
        )

    return score, reasons

#FIXME
def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top k recommendations with explanations."""
    # Score all songs and build (song, score, explanation) tuples
    scored_songs = [
        (song, score, " ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    
    # Sort by score (descending) and return top k results
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]

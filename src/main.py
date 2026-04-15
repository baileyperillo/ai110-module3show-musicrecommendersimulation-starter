"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")


    # User preference profiles
    profiles = {
        "High-Energy Pop": {
            "preferred_genres": ["pop"],
            "preferred_moods": ["happy", "energetic"],
            "energy_target": 0.9,
            "energy_tolerance": 0.15,
            "target_valence": 0.85,
        },
        "Chill Lofi": {
            "preferred_genres": ["lofi", "hip-hop"],
            "preferred_moods": ["calm", "melancholic"],
            "energy_target": 0.25,
            "energy_tolerance": 0.2,
            "target_valence": 0.4,
        },
        "Deep Intense Rock": {
            "preferred_genres": ["rock", "metal"],
            "preferred_moods": ["angry", "intense"],
            "energy_target": 0.95,
            "energy_tolerance": 0.1,
            "target_valence": 0.3,
        },
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 70)
        print(f"🎵 TOP RECOMMENDATIONS — {profile_name} 🎵".center(70))
        print("=" * 70 + "\n")

        for i, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"#{i} {song['title']}")
            print(f"   Artist: {song['artist']} | Genre: {song['genre']}")
            print(f"   Score: {score:.2f}/10.0")
            print(f"   Why: {explanation}")
            print("-" * 70 + "\n")


if __name__ == "__main__":
    main()

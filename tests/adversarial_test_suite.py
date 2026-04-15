"""
Adversarial & Edge Case Test Suite for Music Recommender
Tests the robustness of scoring logic against tricky inputs.
"""

from src.recommender import load_songs, recommend_songs


def test_all_profiles():
    """Run all adversarial test cases and report findings."""
    songs = load_songs("data/songs.csv")
    print(f"\n{'='*80}")
    print("🔬 ADVERSARIAL TEST SUITE - MUSIC RECOMMENDER EVALUATION")
    print(f"{'='*80}\n")
    print(f"Testing against {len(songs)} songs\n")
    
    test_cases = get_all_test_profiles()
    
    for category, profiles in test_cases.items():
        print(f"\n{'─'*80}")
        print(f"📊 CATEGORY: {category}")
        print(f"{'─'*80}\n")
        
        for test_name, user_prefs in profiles.items():
            run_single_test(test_name, user_prefs, songs)


def run_single_test(test_name, user_prefs, songs):
    """Execute a single test and display results."""
    print(f"🧪 Test: {test_name}")
    print(f"   Params: {format_params(user_prefs)}")
    
    try:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        
        if not recommendations:
            print(f"   ⚠️  NO RECOMMENDATIONS RETURNED")
        else:
            scores = [score for _, score, _ in recommendations]
            print(f"   ✓ Returned {len(recommendations)} songs")
            print(f"   Score range: {min(scores):.2f} - {max(scores):.2f}")
            print(f"   Top recommendation: {recommendations[0][0]['title']} ({recommendations[0][1]:.2f} pts)")
            
            # Detect ties
            if len(set(scores)) < len(scores):
                tied_count = len(scores) - len(set(scores))
                print(f"   ⚠️  WARNING: {tied_count} tied scores (determinism risk!)")
        
        print()
    except Exception as e:
        print(f"   ❌ ERROR: {type(e).__name__}: {e}\n")


def format_params(prefs):
    """Pretty-print user preferences."""
    parts = []
    if "preferred_genres" in prefs:
        parts.append(f"genres={prefs['preferred_genres']}")
    if "preferred_moods" in prefs:
        parts.append(f"moods={prefs['preferred_moods']}")
    if "energy_target" in prefs:
        parts.append(f"energy={prefs.get('energy_target', '?'):.2f}±{prefs.get('energy_tolerance', 0):.2f}")
    if "target_valence" in prefs:
        parts.append(f"valence={prefs['target_valence']:.2f}")
    return ", ".join(parts)


def get_all_test_profiles():
    """Return all adversarial test profiles organized by category."""
    
    return {
        "1️⃣  CONFLICTING SEMANTICS": {
            "High Energy + Sad": {
                "preferred_genres": ["blues", "folk", "lofi"],
                "preferred_moods": ["sad", "melancholic"],
                "energy_target": 0.95,
                "energy_tolerance": 0.05,
                "target_valence": 0.15,
            },
            "Low Energy + Angry": {
                "preferred_genres": ["metal", "rock", "hip-hop"],
                "preferred_moods": ["angry", "intense"],
                "energy_target": 0.15,
                "energy_tolerance": 0.15,
                "target_valence": 0.85,
            },
            "Three Contradictory Moods": {
                "preferred_genres": ["r&b", "jazz", "rock"],
                "preferred_moods": ["romantic", "angry", "calm"],
                "energy_target": 0.5,
                "energy_tolerance": 0.5,
                "target_valence": 0.75,
            },
        },
        
        "2️⃣  EXTREME PARAMETERS": {
            "Zero Tolerance (Perfect Match Only)": {
                "preferred_genres": ["pop", "indie pop"],
                "preferred_moods": ["happy"],
                "energy_target": 0.8,
                "energy_tolerance": 0.0,
            },
            "Impossible Energy Target": {
                "preferred_genres": ["jazz", "classical"],
                "preferred_moods": ["transcendent"],
                "energy_target": 1.5,
                "energy_tolerance": 0.1,
            },
            "Negative Parameters": {
                "preferred_genres": ["pop"],
                "preferred_moods": ["happy"],
                "energy_target": -0.5,
                "energy_tolerance": -0.1,
            },
        },
        
        "3️⃣  EMPTY PREFERENCES": {
            "No Genres": {
                "preferred_genres": [],
                "preferred_moods": ["happy"],
                "energy_target": 0.75,
                "energy_tolerance": 0.2,
            },
            "No Moods": {
                "preferred_genres": ["lofi", "jazz"],
                "preferred_moods": [],
                "energy_target": 0.5,
                "energy_tolerance": 0.3,
            },
            "Energy Only": {
                "energy_target": 0.6,
                "energy_tolerance": 0.15,
            },
        },
        
        "4️⃣  ALL SONGS SCORE EQUAL": {
            "All Zero Score": {
                "preferred_genres": ["polka", "zydeco"],
                "preferred_moods": ["existential"],
                "energy_target": 0.0,
                "energy_tolerance": 0.01,
                "target_valence": 0.9999,
            },
            "Maximum Tolerance": {
                "preferred_genres": [],
                "preferred_moods": [],
                "energy_target": 0.5,
                "energy_tolerance": 0.5,
            },
        },
        
        "5️⃣  DATA MISMATCH": {
            "Classical + Metal Speed": {
                "preferred_genres": ["classical"],
                "preferred_moods": ["peaceful"],
                "energy_target": 0.97,
                "energy_tolerance": 0.05,
            },
            "Synthetic Mood": {
                "preferred_genres": ["pop"],
                "preferred_moods": ["nostalgic", "euphoric", "vibe"],
                "energy_target": 0.8,
                "energy_tolerance": 0.15,
            },
            "Case Sensitivity (mixed case)": {
                "preferred_genres": ["Pop", "POP"],
                "preferred_moods": ["Happy"],
                "energy_target": 0.8,
                "energy_tolerance": 0.15,
            },
        },
        
        "6️⃣  NUMERICAL BOUNDARIES": {
            "Float Precision Hell": {
                "preferred_genres": ["pop"],
                "preferred_moods": ["happy"],
                "energy_target": 0.3333333333,
                "energy_tolerance": 0.0000000001,
            },
            "Valence Out of Range (1.5)": {
                "preferred_genres": ["pop"],
                "preferred_moods": ["happy"],
                "energy_target": 0.8,
                "energy_tolerance": 0.2,
                "target_valence": 1.5,
            },
            "Negative Valence": {
                "preferred_genres": ["pop"],
                "preferred_moods": ["happy"],
                "energy_target": 0.8,
                "energy_tolerance": 0.2,
                "target_valence": -0.5,
            },
        },
        
        "7️⃣  CONTROL CASES": {
            "Perfect Match (Golden Song)": {
                "preferred_genres": ["pop"],
                "preferred_moods": ["happy"],
                "energy_target": 0.82,
                "energy_tolerance": 0.01,
                "target_valence": 0.84,
            },
            "Intentional Best Fit": {
                "preferred_genres": ["folk", "classical", "jazz"],
                "preferred_moods": ["peaceful", "sad", "melancholic"],
                "energy_target": 0.25,
                "energy_tolerance": 0.1,
                "target_valence": 0.3,
            },
        },
    }


if __name__ == "__main__":
    test_all_profiles()

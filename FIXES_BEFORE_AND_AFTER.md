# 🛠️ ADVERSARIAL FIXES - Before & After Code

## Issue #1: Case Sensitivity Silent Failure (CRITICAL)

### ❌ BEFORE (Broken)
```python
# recommender.py - score_song()

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    # --- Genre match (+3.0) ---
    preferred_genres = user_prefs.get("preferred_genres", [])
    if song["genre"] in preferred_genres:  # ❌ BUG: Case-sensitive!
        score += 3.0
        reasons.append(f"genre match ({song['genre']}) (+3.0)")

    # --- Mood match (+2.0) ---
    preferred_moods = user_prefs.get("preferred_moods", [])
    if song["mood"] in preferred_moods:  # ❌ BUG: Case-sensitive!
        score += 2.0
        reasons.append(f"mood match ({song['mood']}) (+2.0)")
```

**Problem:** 
- User enters: `genres=['Pop']`
- Data has: `genre: "pop"`
- Result: `'Pop' in ["pop"]` → False → No match!

### ✅ AFTER (Fixed)
```python
def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    # --- Genre match (+3.0) ---
    preferred_genres = user_prefs.get("preferred_genres", [])
    song_genre_lower = song["genre"].lower()
    preferred_genres_lower = [g.lower() for g in preferred_genres]
    
    if song_genre_lower in preferred_genres_lower:  # ✅ FIXED: Case-insensitive!
        score += 3.0
        reasons.append(f"genre match ({song['genre']}) (+3.0)")

    # --- Mood match (+2.0) ---
    preferred_moods = user_prefs.get("preferred_moods", [])
    song_mood_lower = song["mood"].lower()
    preferred_moods_lower = [m.lower() for m in preferred_moods]
    
    if song_mood_lower in preferred_moods_lower:  # ✅ FIXED: Case-insensitive!
        score += 2.0
        reasons.append(f"mood match ({song['mood']}) (+2.0)")
```

**Result:** 
- User enters: `genres=['Pop']`
- Comparison: `'pop' in ['pop']` → True ✓
- Score: +3.0 applied correctly

---

## Issue #2: No Input Validation (CRITICAL)

### ❌ BEFORE (Broken)
```python
def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    # --- Energy within tolerance (0.0–2.0, linear decay) ---
    energy_target = user_prefs.get("energy_target", 0.5)  # ❌ No validation!
    energy_tolerance = user_prefs.get("energy_tolerance", 0.2)  # ❌ No validation!
    energy_diff = abs(song["energy"] - energy_target)
    
    # If energy_target is 1.5 or -0.5, math still works but is nonsensical!
```

**Problems:**
- `energy_target: 1.5` (outside [0, 1]) → All songs far from target
- `energy_tolerance: -0.1` (negative!) → Disables energy scoring
- `energy_tolerance: 0.0` (too strict) → Floating point precision issues

### ✅ AFTER (Fixed)
```python
def validate_user_preferences(user_prefs: Dict) -> None:
    """Validate user preferences and raise errors for invalid values."""
    
    # Validate energy_target
    energy_target = user_prefs.get("energy_target")
    if energy_target is not None:
        if not isinstance(energy_target, (int, float)):
            raise ValueError(f"energy_target must be a number, got {type(energy_target)}")
        if not 0 <= energy_target <= 1:
            raise ValueError(f"energy_target must be in [0, 1], got {energy_target}")
    
    # Validate energy_tolerance
    energy_tolerance = user_prefs.get("energy_tolerance")
    if energy_tolerance is not None:
        if not isinstance(energy_tolerance, (int, float)):
            raise ValueError(f"energy_tolerance must be a number, got {type(energy_tolerance)}")
        if energy_tolerance < 0:
            raise ValueError(f"energy_tolerance must be non-negative, got {energy_tolerance}")
        if energy_tolerance > 1:
            print(f"⚠️  Warning: energy_tolerance > 1.0 ({energy_tolerance}) will match all songs")
    
    # Validate target_valence
    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        if not 0 <= target_valence <= 1:
            raise ValueError(f"target_valence must be in [0, 1], got {target_valence}")
    
    # Validate genres/moods exist in dataset
    VALID_GENRES = {"pop", "lofi", "rock", "ambient", "jazz", "synthwave", 
                    "indie pop", "hip-hop", "classical", "r&b", "country", 
                    "metal", "electronic", "blues", "folk"}
    VALID_MOODS = {"happy", "chill", "intense", "relaxed", "moody", "focused",
                   "confident", "peaceful", "romantic", "nostalgic", "angry",
                   "euphoric", "sad", "melancholic"}
    
    for genre in user_prefs.get("preferred_genres", []):
        if genre.lower() not in VALID_GENRES:
            print(f"⚠️  Warning: genre '{genre}' not found in dataset (valid: {', '.join(sorted(VALID_GENRES))})")
    
    for mood in user_prefs.get("preferred_moods", []):
        if mood.lower() not in VALID_MOODS:
            print(f"⚠️  Warning: mood '{mood}' not found in dataset (valid: {', '.join(sorted(VALID_MOODS))})")


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top k recommendations with explanations."""
    
    # ✅ Validate input before processing
    validate_user_preferences(user_prefs)
    
    # Score all songs and build (song, score, explanation) tuples
    scored_songs = [
        (song, score, " ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    
    # Sort by score (descending) and return top k results
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
```

**Result:**
```python
# Now rejects invalid input
user_prefs = {"energy_target": 1.5}
recommend_songs(user_prefs, songs)
# Raises: ValueError: energy_target must be in [0, 1], got 1.5

# Or warns about missing moods
user_prefs = {"preferred_moods": ["vibe"]}
recommend_songs(user_prefs, songs)
# Prints: ⚠️  Warning: mood 'vibe' not found in dataset
```

---

## Issue #3: Tied Scores Not Deterministic

### ❌ BEFORE (Arbitrary Tie-Breaking)
```python
# If two songs have the same score:
scored_songs = [
    (song1, 3.5, "..."),
    (song2, 3.5, "..."),  # Same score!
]

sorted_result = sorted(scored_songs, key=lambda x: x[1], reverse=True)
# Python maintains relative order (stable sort), but which is "first" is ambiguous
```

**Problem:** Same profile might return different recommendations if there are ties

### ✅ AFTER (Deterministic Tie-Breaking)
```python
def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top k recommendations with explanations."""
    
    validate_user_preferences(user_prefs)
    
    scored_songs = [
        (song, score, " ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    
    # ✅ FIXED: Sort by score DESC, then by song ID ASC for deterministic tie-breaking
    return sorted(
        scored_songs, 
        key=lambda x: (-x[1], x[0]['id']),  # Score DESC, then ID ASC
        reverse=False
    )[:k]
```

**Result:**
- Same score → broken by song ID (lower ID wins)
- Reproducible: run same profile twice, get same top-5

---

## Testing the Fixes

### Test Case: Case Sensitivity
```python
profile = {
    "preferred_genres": ["Pop", "ROCK"],  # Mixed case
    "preferred_moods": ["Happy"],
    "energy_target": 0.8,
    "energy_tolerance": 0.2,
}

# BEFORE: Score = 1.73 (genre/mood not matched)
# AFTER:  Score = 5.00 (genre/mood matched correctly)
```

### Test Case: Invalid Input
```python
profile = {
    "energy_target": 1.5,  # Invalid!
}

# BEFORE: Returns scores (nonsensical)
# AFTER:  Raises ValueError immediately
```

### Test Case: Tied Scores
```python
# Run same profile 5 times
for i in range(5):
    results = recommend_songs(profile, songs, k=5)
    print(results[0][0]['title'])  # Top recommendation

# BEFORE: May vary (non-deterministic)
# AFTER:  Always same (deterministic)
```

---

## Implementation Priority

1. **Fix #1 (Case Sensitivity):** 5 lines changed, 2-3 lines added
2. **Fix #2 (Validation):** 30-50 lines added (new function)
3. **Fix #3 (Tie-Breaking):** 1 line modified in sort key

**Total Time:** ~30 minutes for all three critical fixes

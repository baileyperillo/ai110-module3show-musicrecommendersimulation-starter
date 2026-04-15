# 🎯 Adversarial & Edge Case Test Profiles
## Music Recommender System Evaluation

---

## Category 1: Conflicting Semantic Preferences
These profiles have contradictory mood-energy combinations that violate typical musical semantics.

### 1.1: High Energy + Sad Mood
```python
"Contradictory Melancholy": {
    "preferred_genres": ["blues", "folk", "lofi"],
    "preferred_moods": ["sad", "melancholic"],
    "energy_target": 0.95,           # CONTRADICTION: high energy
    "energy_tolerance": 0.05,        # Very strict
    "target_valence": 0.15,          # Low positivity (sad)
}
```
**What it tests:**
- Energy=0.95 with sad mood is unnatural (e.g., "Storm Runner" is 0.91 energy but "intense", not sad)
- Algorithm may rank songs poorly because sad/melancholic songs rarely have high energy
- **Expected result:** Likely returns very few/no matches, or misaligned recommendations
- **Question:** Does the system gracefully handle zero matches?

### 1.2: Low Energy + Angry Mood
```python
"Lazy Aggression": {
    "preferred_genres": ["metal", "rock", "hip-hop"],
    "preferred_moods": ["angry", "intense"],
    "energy_target": 0.15,           # CONTRADICTION: very low energy
    "energy_tolerance": 0.15,        # Allows 0.0-0.3
    "target_valence": 0.85,          # Upbeat? Contradicts angry
}
```
**What it tests:**
- Angry songs typically have high energy (e.g., "Shatter the Glass" = 0.97)
- Low energy contradicts the genre expectations
- Mixed signals: low energy + high valence + angry mood

### 1.3: Romantic + Angry + Calm Mood
```python
"Emotional Chaos": {
    "preferred_genres": ["r&b", "jazz", "rock"],
    "preferred_moods": ["romantic", "angry", "calm"],  # All three together
    "energy_target": 0.5,
    "energy_tolerance": 0.5,         # Very loose (0.0-1.0)
    "target_valence": 0.75,          # Upbeat
}
```
**What it tests:**
- Can the system prioritize when everything is preferred?
- Without genre/mood weighting, maybe all high-scoring songs tie
- Fuzzy preferences indicate a confused user

---

## Category 2: Extreme Parameter Values

### 2.1: Zero Energy Tolerance
```python
"Perfectionistic": {
    "preferred_genres": ["pop", "indie pop"],
    "preferred_moods": ["happy"],
    "energy_target": 0.8,
    "energy_tolerance": 0.0,         # ONLY energy=0.8 exactly
}
```
**What it tests:**
- Will any song be exactly 0.8 energy? (CSV shows discrete values)
- Edge case: `energy_diff <= energy_tolerance` becomes `energy_diff <= 0.0`
- If no exact match exists, should return 0 points for energy

### 2.2: Impossible Range
```python
"The Unicorn": {
    "preferred_genres": ["jazz", "classical"],  # Genres not in dataset?
    "preferred_moods": ["transcendent"],        # Not a real mood?
    "energy_target": 1.5,            # Outside normalized range [0, 1]!
    "energy_tolerance": 0.1,
}
```
**What it tests:**
- Dataset only has moods: happy, chill, intense, relaxed, moody, focused, confident, peaceful, romantic, nostalgic, angry, euphoric, sad, melancholic
- If energy_target > 1.0, all songs will have `energy_diff` huge
- **Bug potential:** No validation on input ranges

### 2.3: Negative/Invalid Parameters
```python
"Broken Input": {
    "preferred_genres": ["pop"],
    "preferred_moods": ["happy"],
    "energy_target": -0.5,           # Negative!
    "energy_tolerance": -0.1,        # Negative tolerance!
}
```
**What it tests:**
- Are inputs validated?
- Will `abs(song["energy"] - (-0.5))` math work correctly?
- `-0.1` tolerance: will `energy_diff <= -0.1` ever be true?

---

## Category 3: Empty/No Preference Profiles

### 3.1: Empty Genre Preferences
```python
"Genre Agnostic": {
    "preferred_genres": [],          # No genres!
    "preferred_moods": ["happy"],
    "energy_target": 0.75,
    "energy_tolerance": 0.2,
}
```
**What it tests:**
- Empty list check: `if song["genre"] in []` always False
- All songs skip genre scoring
- Recommendations based only on mood + energy

### 3.2: No Mood Preferences
```python
"Mood Flexible": {
    "preferred_genres": ["lofi", "jazz"],
    "preferred_moods": [],           # No moods!
    "energy_target": 0.5,
    "energy_tolerance": 0.3,
}
```
**What it tests:**
- Similar to 3.1, mood scoring skipped for all songs

### 3.3: Minimal Preferences (only energy)
```python
"Energy Only": {
    # Missing preferred_genres, preferred_moods
    "energy_target": 0.6,
    "energy_tolerance": 0.15,
}
```
**What it tests:**
- `user_prefs.get("preferred_genres", [])` returns empty list
- Does `.get()` fallback work correctly?
- What's the minimum viable preference profile?

---

## Category 4: Extreme/Degenerate Cases

### 4.1: All Songs Score Zero
```python
"No Match": {
    "preferred_genres": ["polka", "zydeco"],   # Genres not in data
    "preferred_moods": ["existential"],        # Mood not in data
    "energy_target": 0.0,
    "energy_tolerance": 0.01,          # Only [0.0 - 0.01] range
    "target_valence": 0.9999,          # Almost no song matches
}
```
**What it tests:**
- Ties: if all scores are identical, sort is arbitrary
- How does tie-breaking work? By original order? Random?
- SQL OFFSET/LIMIT style: if all N songs tie at 0.0, returning top 5 is arbitrary
- User experience: "No recommendations found" vs random songs

### 4.2: All Songs Score Equal (Intentional Tie)
```python
"Everyone's Equal": {
    "preferred_genres": ["*WILDCARD*"],  # Matches nothing deliberately
    "preferred_moods": ["*WILDCARD*"],
    "energy_target": 0.5,               # Likely matches some songs equally
    "energy_tolerance": 0.5,            # Huge tolerance
}
```
**What it tests:**
- Determinism: is sorting stable? Do ties use stable sort?
- If two songs have same score, which appears first?
- Reproducibility: run twice, get same order?

### 4.3: Very Large k (k > total songs)
```python
# When calling: recommend_songs(user_prefs, songs, k=1000)
# Dataset has ~18 songs
```
**What it tests:**
- `return sorted(...)[:k]` when k > len(songs)
- Python slicing handles this gracefully (`x[:999]` on 18-item list works)
- But does the UI expect exactly k results?

### 4.4: Very Small k (k=0 or k=1)
```python
# When calling: recommend_songs(user_prefs, songs, k=0)
# Or: recommend_songs(user_prefs, songs, k=1)
```
**What it tests:**
- k=0: returns empty list (valid? or error?)
- k=1: edge case for UI handling

---

## Category 5: Adversarial Data Mismatches

### 5.1: Genre Doesn't Match Energy/Mood
```python
"Classical at Metal Levels": {
    "preferred_genres": ["classical"],  # Classical typically low energy
    "preferred_moods": ["peaceful"],
    "energy_target": 0.97,              # Metal/aggressive levels
    "energy_tolerance": 0.05,
}
```
**Why this matters:**
- Dataset: "Still Water Suite" = classical, 0.22 energy
- Asking for classical + 0.97 energy = likely no match
- Reveals algorithm doesn't understand genre-energy correlation

### 5.2: Synthetic Mood (Not in Dataset)
```python
"Spotify Algorithm": {
    "preferred_genres": ["pop"],
    "preferred_moods": ["nostalgic", "euphoric", "vibe"],  # Last one invented
    "energy_target": 0.8,
    "energy_tolerance": 0.15,
}
```
**What it tests:**
- Case sensitivity: is "Happy" ≠ "happy"?
- Typo resilience: "euporic" vs "euphoric"
- Does system validate mood against known moods?

### 5.3: Genre Typo / Case Sensitivity
```python
"Case Sensitive Fail": {
    "preferred_genres": ["Pop", "POP", "pop!"],  # Different cases + special char
    "preferred_moods": ["Happy"],                # Capital H
    "energy_target": 0.8,
    "energy_tolerance": 0.15,
}
```
**What it tests:**
- CSV has `"pop"` (lowercase)
- Does `"Pop" in ["pop", "lofi", ...]` fail silently?
- No robust matching = silent failure for user input

---

## Category 6: Numerical Boundary Conditions

### 6.1: Float Precision Edge Case
```python
"Floating Point Hell": {
    "preferred_genres": ["pop"],
    "preferred_moods": ["happy"],
    "energy_target": 0.3333333333,     # Repeating decimal
    "energy_tolerance": 0.0000000001,  # Extremely tight
}
```
**What it tests:**
- `abs(0.82 - 0.3333333333) = 0.4866...` >> tolerance
- Floating point arithmetic: `0.1 + 0.2 != 0.3` in IEEE 754
- Does scoring handle precision correctly?

### 6.2: Valence Exceeding [0, 1]
```python
"Valence Overload": {
    "preferred_genres": ["pop"],
    "preferred_moods": ["happy"],
    "energy_target": 0.8,
    "energy_tolerance": 0.2,
    "target_valence": 1.5,             # Outside [0, 1] normalization!
}
```
**What it tests:**
- `valence_diff = abs(0.84 - 1.5) = 0.66`
- `valence_score = max(0.0, (1 - 0.66) * 1.5) = 0.34 * 1.5 = 0.51`
- Math still works, but semantically broken

### 6.3: Target Valence Outside [0, 1]
```python
"Negative Vibes": {
    "target_valence": -0.5,            # Negative (impossible)
}
```
**What it tests:**
- `valence_diff = abs(0.84 - (-0.5)) = 1.34`
- `(1 - 1.34) = -0.34`, then `max(0.0, -0.34 * 1.5) = 0.0`
- Math clips to 0, but invalid input accepted

---

## Category 7: Special Test Case Combinations

### 7.1: Deliberate Perfect Match
```python
"The Golden Song": {
    "preferred_genres": ["pop"],
    "preferred_moods": ["happy"],
    "energy_target": 0.82,             # Exactly "Sunrise City"
    "energy_tolerance": 0.01,
    "target_valence": 0.84,            # Exactly "Sunrise City"
}
```
**What it tests:**
- Maximum score: 3.0 + 2.0 + 2.0 + 1.5 = 8.5
- Does algorithm identify this?
- Reproducibility: always returns "Sunrise City" first?

### 7.2: Intentional Worst Case
```python
"Anti-Pop": {
    "preferred_genres": ["folk", "classical", "jazz"],
    "preferred_moods": ["peaceful", "sad", "melancholic"],
    "energy_target": 0.25,
    "energy_tolerance": 0.1,           # Only [0.15 - 0.35]
    "target_valence": 0.3,
}
```
**What it tests:**
- Manually designed to exclude "Sunrise City", "Gym Hero", "Shatter the Glass"
- Verifies algorithm correctly filters

### 7.3: Maximum Tolerance (No Filtering)
```python
"Acceptance": {
    "preferred_genres": ["*"],         # Invalid, but...
    "preferred_moods": ["*"],          # ...tests robustness
    "energy_target": 0.5,
    "energy_tolerance": 0.5,           # Allows [0.0 - 1.0]
}
```
**What it tests:**
- Tolerance of 0.5 captures almost all songs
- All songs likely score ≥2.0 (from energy alone)
- Ranking becomes arbitrary

---

## Recommended Test Execution Order

1. **Start Simple:** 7.1 (Golden Song) - verify baseline works
2. **Empty Cases:** 3.1, 3.2, 3.3 - test graceful degradation
3. **Contradictions:** 1.1, 1.2 - find ranking logic issues
4. **Boundaries:** 2.1, 2.2, 6.1 - numerical robustness
5. **Tie-Breaking:** 4.1, 4.2 - determinism
6. **Data Mismatches:** 5.2, 5.3 - validation failures
7. **Extreme Values:** 2.3, 6.2, 6.3 - input validation

---

## Expected System Behaviors to Investigate

- [ ] **Validation:** Does input reject/warn on invalid values?
- [ ] **Graceful Degradation:** Empty preferences → partial recommendations?
- [ ] **Tie-Breaking:** Are ties deterministic? Stable sort?
- [ ] **Edge Cases:** k=0, k>total, empty results?
- [ ] **Case Sensitivity:** Genre/mood matching case-insensitive?
- [ ] **Numerical Precision:** Float comparison edge cases?
- [ ] **Range Checking:** Clamp values to [0, 1]?
- [ ] **Error Messages:** User-friendly explanations?

---

## Scoring Impact Analysis

For each test case, measure:
1. **Total recommendations returned:** < k? = k? > k?
2. **Score distribution:** Min/max/avg scores
3. **Top-ranked song:** Which song wins?
4. **Reproducibility:** Same result on repeat?
5. **Explanation quality:** Do reasons make sense?

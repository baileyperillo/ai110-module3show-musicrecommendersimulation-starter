# Quick Reference: Running Adversarial Tests

## Execute the Full Test Suite
```bash
python -m pytest tests/adversarial_test_suite.py -v
# OR
python tests/adversarial_test_suite.py
```

## Key Vulnerabilities Found

### 🔴 **Critical Issues to Investigate**

1. **Tie-Breaking Undefined** (Category 4)
   - When all songs score 0 or equal values, ranking is arbitrary
   - Example: "All Zero Score" profile → no genres/moods match
   - Risk: Recommendations appear random

2. **No Input Validation** (Category 2 & 6)
   - System accepts energy_target = 1.5 (outside [0, 1])
   - System accepts energy_tolerance = -0.1 (negative!)
   - No clipping or warning messages

3. **Case Sensitivity Silently Fails** (Category 5)
   - "Pop" ≠ "pop" → zero matches, no error
   - User input from UI likely has different casing
   - Silent failure = confused users

4. **Contradictory Requirements Undetected** (Category 1)
   - "sad mood + 0.95 energy" is musically impossible
   - Algorithm dutifully returns bad recommendations
   - No semantic understanding of domain

### 🟡 **Medium Priority Issues**

5. **Empty Preference Lists** (Category 3)
   - Gracefully handled but reduces recommendation quality
   - All songs skip that dimension (genre/mood)

6. **Extreme Tolerances** (Category 2)
   - k > total songs (asks for 1000, has 18) → no error
   - energy_tolerance = 0.5 means "accept everything"

7. **Floating Point Edge Cases** (Category 6)
   - Tolerance = 0.0000000001 likely hits precision issues
   - No guidance on reasonable tolerance values

---

## What Each Test Category Reveals

| Category | Risk Type | Example | Expected Behavior |
|----------|-----------|---------|-------------------|
| 1: Conflicting Semantics | Domain Logic | sad + 0.95 energy | Detect/warn about contradiction |
| 2: Extreme Parameters | Input Validation | energy=-0.5 | Reject or clamp to [0, 1] |
| 3: Empty Preferences | Graceful Degradation | genres=[] | Return partial results |
| 4: Tied Scores | Tie-Breaking | all score 0.0 | Deterministic, stable sort |
| 5: Data Mismatch | Robustness | mood="vibe" (not in data) | Fail gracefully with message |
| 6: Numerical Boundaries | Math Correctness | valence=1.5 | Handle out-of-range sensibly |
| 7: Control Cases | Verify Baseline | perfect match | Should rank #1 consistently |

---

## Test Execution Checklist

Run tests and document findings for each:

- [ ] **Do invalid inputs get rejected or produce warnings?**
  - Tests: 2.2, 2.3, 5.3, 6.2
  
- [ ] **Are tied scores handled deterministically?**
  - Tests: 4.1, 4.2, 7 (compare Control cases multiple times)
  
- [ ] **Do empty preferences gracefully skip scoring?**
  - Tests: 3.1, 3.2, 3.3
  
- [ ] **Is case-sensitive matching a silent failure?**
  - Tests: 5.3 (compare with lowercase genres in main.py)
  
- [ ] **Are contradictory requirements detected?**
  - Tests: 1.1, 1.2, 1.3
  
- [ ] **Does perfect match always rank first?**
  - Tests: 7 (Golden Song)

---

## Sample Output Analysis

Expected output when running test:
```
🧪 Test: High Energy + Sad
   Params: genres=['blues', 'folk', 'lofi'], moods=['sad', 'melancholic'], energy=0.95±0.05
   ✓ Returned 5 songs
   Score range: 0.00 - 2.05
   Top recommendation: ??? 
   ⚠️  WARNING: Many tied scores (determinism risk!)
```

**Analysis:**
- If top song is random each run → tie-breaking issue
- If score range is 0.0-2.05 → only energy scored (genre/mood didn't match expected sad high-energy combo)
- This is expected: sad songs rarely have 0.95 energy

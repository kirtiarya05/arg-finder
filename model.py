def resistance_score(matches, gc):
    score = len(matches) * 20 + (gc / 10)
    return min(score, 100)
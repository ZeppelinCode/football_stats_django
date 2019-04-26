from matches_cache import matches

print([match['Team1'] for match in matches if not match['Team1']])
print([match['Team2'] for match in matches if not match['Team2']])

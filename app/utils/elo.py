def calculate_elo(winner_elo, loser_elo, k=32):
    # Calculate expected scores
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

    # Update ratings
    new_winner_elo = winner_elo + k * (1 - expected_winner)  # Winner gets 1 point
    new_loser_elo = loser_elo + k * (0 - expected_loser)

    return int(new_winner_elo), int(new_loser_elo)
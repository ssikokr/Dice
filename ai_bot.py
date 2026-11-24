"""Dynamic Bot AI logic and difficulty models for Dice Arcade (Pig).

Provides 4 distinct strategic AI personalities:
1. Cautious (Easy): Banks early (threshold 10), minimizing risk.
2. Balanced (Medium): The classic V3 strategy (banks at 15, or earlier when ahead).
3. Aggressive (Hard): Pushes for big turns (22+ pts), aggressive when trailing.
4. Adaptive (Master): Dynamically scales risk based on live game state, score delta,
   and proximity to target.
"""

AI_DIFFICULTIES = {
    "cautious": {
        "name": "Cautious",
        "description": "Easy — Banks early at 10 pts, avoids risking Pig Out.",
        "badge": "Easy",
    },
    "balanced": {
        "name": "Balanced",
        "description": "Medium — Classic heuristic, banks at 15 pts.",
        "badge": "Medium",
    },
    "aggressive": {
        "name": "Aggressive",
        "description": "Hard — High-roller, pushes for 22+ pts each turn.",
        "badge": "Hard",
    },
    "adaptive": {
        "name": "Adaptive",
        "description": "Master — Dynamically evaluates score deficit & win distance.",
        "badge": "Master",
    },
}


def evaluate_bot_decision(difficulty, turn_score, bot_score, player_score, target_score=50):
    """Determine whether the AI Bot should bank points or roll again.

    Args:
        difficulty: One of 'cautious', 'balanced', 'aggressive', 'adaptive'.
        turn_score: Points accumulated in the current turn.
        bot_score: Current banked score of the bot.
        player_score: Current banked score of the human player.
        target_score: Target score needed to win the match (default 50).

    Returns:
        bool: True if the bot should bank points, False to roll again.
    """
    # Rule 1: Always bank if the current turn points will win the match!
    if bot_score + turn_score >= target_score:
        return True

    diff = difficulty.lower()

    if diff == "cautious":
        return turn_score >= 10

    if diff == "aggressive":
        deficit = player_score - bot_score
        target_threshold = 25 if deficit >= 15 else 22
        return turn_score >= target_threshold

    if diff == "adaptive":
        deficit = player_score - bot_score
        dist_to_win = target_score - bot_score
        opp_dist = target_score - player_score

        if opp_dist <= 15 and deficit > 0:
            threshold = min(dist_to_win, max(18, opp_dist + 5))
        elif deficit <= -15:
            threshold = 10
        elif deficit <= -8:
            threshold = 12
        else:
            threshold = int(round(15 + deficit * 0.35))
            threshold = max(10, min(24, threshold))

        threshold = min(threshold, dist_to_win)
        return turn_score >= threshold

    # Default: "balanced"
    return turn_score >= 15 or (bot_score >= 35 and turn_score >= 10)


def get_difficulty_name(difficulty):
    """Return the display name for a difficulty key."""
    info = AI_DIFFICULTIES.get(difficulty.lower())
    return info["name"] if info else "Balanced"

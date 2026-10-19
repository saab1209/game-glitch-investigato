import random

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}

HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def get_attempt_limit(difficulty: str):
    """Return the number of attempts allowed for a given difficulty."""
    return ATTEMPT_LIMITS.get(difficulty, ATTEMPT_LIMITS["Normal"])


def get_hint_message(outcome: str):
    """Return the hint text shown to the player for an outcome."""
    return HINT_MESSAGES[outcome]


def new_game_state(difficulty: str, rng=random):
    """Return a fresh game state with a secret inside the difficulty's range."""
    low, high = get_range_for_difficulty(difficulty)
    return {
        "secret": rng.randint(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
        "difficulty": difficulty,
    }


def get_game_status(outcome: str, attempts: int, attempt_limit: int):
    """Return "won", "lost", or "playing" after a guess."""
    if outcome == "Win":
        return "won"
    if attempts >= attempt_limit:
        return "lost"
    return "playing"


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: AI and agent mode agreed invalid input should not create a game attempt.
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except (TypeError, ValueError):
        return False, None, "That is not a number."

    return True, value, None


def record_guess(history: list, attempts: int, guess: int):
    """Record one valid guess and return the updated attempts and history."""
    return attempts + 1, [*history, guess]


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: AI identified the inverted hint logic; comparisons now describe the actual guess.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Agent mode removed the alternating penalty and made score changes consistent.
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score

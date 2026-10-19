from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_game_status,
    get_hint_message,
    new_game_state,
    parse_guess,
    record_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_blank_guess_is_rejected():
    result = parse_guess(" ")
    assert result == (False, None, "Enter a guess.")


def test_non_numeric_guess_is_rejected():
    result = parse_guess("not a number")
    assert result == (False, None, "That is not a number.")


def test_valid_guess_is_parsed_as_an_integer():
    result = parse_guess("42")
    assert result == (True, 42, None)


def test_record_guess_updates_attempts_and_history_together():
    attempts, history = record_guess([25], 1, 50)
    assert attempts == 2
    assert history == [25, 50]


def test_record_guess_does_not_mutate_previous_history():
    previous_history = [25]
    record_guess(previous_history, 1, 50)
    assert previous_history == [25]


def test_wrong_guesses_reduce_score_consistently():
    assert update_score(10, "Too High", 1) == 5
    assert update_score(10, "Too Low", 1) == 5


def test_first_attempt_win_awards_full_score():
    assert update_score(0, "Win", 1) == 100


def test_guess_50_with_secret_74_says_go_higher():
    outcome = check_guess(50, 74)
    assert outcome == "Too Low"
    assert get_hint_message(outcome) == "📈 Go HIGHER!"


def test_new_game_state_resets_everything():
    state = new_game_state("Easy")
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert 1 <= state["secret"] <= 20


def test_new_game_state_returns_a_fresh_history_list():
    first = new_game_state("Normal")
    first["history"].append(10)
    assert new_game_state("Normal")["history"] == []


def test_game_status_after_guess():
    assert get_game_status("Win", 3, 8) == "won"
    assert get_game_status("Too Low", 8, 8) == "lost"
    assert get_game_status("Too High", 2, 8) == "playing"


def test_attempt_limits_by_difficulty():
    assert get_attempt_limit("Easy") == 6
    assert get_attempt_limit("Normal") == 8
    assert get_attempt_limit("Hard") == 5

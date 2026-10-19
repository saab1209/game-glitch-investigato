import streamlit as st

from logic_utils import (
    # FIX: Agent mode helped move reusable game logic out of the Streamlit UI.
    check_guess,
    get_attempt_limit,
    get_game_status,
    get_hint_message,
    get_range_for_difficulty,
    new_game_state,
    parse_guess,
    record_guess,
    update_score,
)


def start_new_game(difficulty: str):
    """Replace every game value in session state and clear the guess box."""
    st.session_state.update(new_game_state(difficulty))
    # A new key gives the text input a fresh, empty widget.
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: Start a fresh game on first load or when the difficulty changes,
# so the secret always fits the current range.
if st.session_state.get("difficulty") != difficulty:
    start_new_game(difficulty)

st.subheader("Make a guess")

if st.button("New Game 🔁"):
    start_new_game(difficulty)
    st.session_state.flash = "New game started."
    st.rerun()

if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

# FIX: AI-assisted debugging identified the alternating-submit issue; the form submits input atomically.
with st.form("guess_form", clear_on_submit=True):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{st.session_state.game_id}",
    )

    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button(
            "Submit Guess 🚀",
            disabled=st.session_state.status != "playing",
        )
    with col2:
        show_hint = st.checkbox("Show hint", value=True)

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        # FIX: We used agent mode to keep valid guesses, attempts, and history synchronized.
        st.session_state.attempts, st.session_state.history = record_guess(
            history=st.session_state.history,
            attempts=st.session_state.attempts,
            guess=guess_int,
        )

        # FIX: AI review corrected the hint mapping so it matches the guess outcome.
        outcome = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(get_hint_message(outcome))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )
        st.session_state.status = get_game_status(
            outcome, st.session_state.attempts, attempt_limit
        )

        if st.session_state.status == "won":
            st.balloons()

# FIX: Status messages render from session state, so they persist across reruns
# instead of halting the script with st.stop().
if st.session_state.status == "won":
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}. Start a new game to try again."
    )

attempts_left = attempt_limit - st.session_state.attempts

# FIX: AI-assisted debugging moved these displays after processing so they show current state immediately.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)

st.sidebar.divider()
st.sidebar.header("Game Tracker")
st.sidebar.metric("Attempts used", f"{st.session_state.attempts} / {attempt_limit}")
st.sidebar.metric("Attempts left", attempts_left)
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.subheader("Guess History")
if st.session_state.history:
    for number, guess in enumerate(st.session_state.history, start=1):
        st.sidebar.write(f"{number}. {guess}")
else:
    st.sidebar.caption("No guesses yet.")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

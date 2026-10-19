# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.
The purpose of the game is to guess an already determined number in the given range.
- [X] Detail which bugs you found.
The hints were inverted - when guess was too high it would say too low, vice versa
The attempts were not loading or being remembered correctly
The new game button didn't work at all - scores were not reset.
- [X] Explain what fixes you applied.
I applied all the fixes noted above.

# MY EXPERIENCE EXPLAINED
- [X] Describe the game's purpose.
The purpose of the game is to guess an already determined number in the given range. When you initialize a round via the Streamlit interface, a randomized hidden integer is picked, and you must use sequential guessing strategy to discover it before running completely out of your allocated attempts.

- [X] Detail which bugs you found.
The hints were inverted - when guess was too high it would say too low, vice versa. During my Phase 1 glitch hunt, guessing 50 on a hidden target of 74 threw an incorrect direction cue. I also discovered that the attempts were not loading or being remembered correctly in the sidebar UI, and the new game button didn't work at all - scores were not reset when clicked.

- [X] Explain what fixes you applied.
I applied all the fixes noted above by executing a structured refactor. I used my AI assistant to clean up the code by migrating core processing functions out of app.py and into logic_utils.py. From there, I corrected the inverted hints comparison logic, repaired the broken Streamlit session state trackers so attempts update properly, and successfully wired up the new game reset function. I manually confirmed the fix by guessing 74 to trigger the winning screen, and verified the build using automated tools, which resulted in a 15/15 passing pytest run.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 50
2. Game returns "Too Low"
3. User enters a guess of 75, and the game shows "Too High"
4. Score updates correctly after each guess
5. Game ends after the correct guess or the user runs out of attempts

## MY Demo Walkthrough

1. The game initializes a secret number of 74 and sets attempts remaining to 8.
2. User enters an initial guess of 50; the system correctly returns the hint "📈 Go HIGHER!".
3. User enters a secondary guess of 75; the system correctly returns the hint "📉 Go LOWER!".
4. User narrows down the selection by entering 62 and 68, receiving accurate higher hints.
5. User inputs consecutive guesses of 71 and 73, and the sidebar logs history dynamically.
6. User enters the exact secret number of 74; the game triggers the win state successfully.
7. User clicks the "New Game" button; the environment state fully wipes and resets cleanly.



**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= 10 passed in 0.02s =========================
```
#MY TEST RESULTS BELOW
================================================= test session starts ==================================================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/salmaa/Documents/GitHub/ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
plugins: anyio-4.15.1
collected 15 items                                                                                                     

tests/test_game_logic.py ...............                                                                         [100%]

================================================== 15 passed in 0.02s ==============================



## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional] .

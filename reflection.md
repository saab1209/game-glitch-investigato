# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game the Streamlit interface loaded successfully in my browser, but the underlying gameplay mechanics were heavily glitched. When I entered a guess of 50, the app provided a completely backward hint telling me to guess lower when the secret number was actually higher. Additionally, as I kept playing I noticed that the guess history log, total attempts, and attempts left counters failed to update on the screen. Clicking the "New Game" button also did absolutely nothing, meaning the application lacked a working reset function to start a fresh round. I suspect these logic errors are split between a flipped comparison inside the check guess function also missing session state updates for the scoring systems, and an unmapped reset function.

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
When I put in 50 it told me to guess lower when I really should have guessed higher. Should be in check guess function.
I noticed that history, attempts, and attempts left were not updating properly. Bug should be in update score.
The new game button didn't work at all. Should have a reset funciton.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `50` when the secret number is higher | The game should say to guess higher. | The game said to guess lower. | No console error. |
| Enter one or more guesses | History and attempt counts should update after each guess, including attempts left. | History, attempts, and attempts left did not update properly. | No console error. |
| Click the New Game button | The game should reset and start a new round. | Nothing happened; the game did not reset. | No console error. |

| Guess `50` when the secret number is 74 | The game should display a "Too Low" hint and suggest a higher number. | The game stated the guess was too high and told me to go lower. | No console error. |
| Submitting multiple sequential guesses | The sidebar trackers should decrease remaining attempts and append guesses to the history list. | The counter values remained static and the history log stayed blank. | No console error. |
| Clicking the interactive "New Game" button | The application should wipe the state, pick a new secret number, and refresh the attempts to 8. | The application remained completely frozen on the finished state without resetting. | No console error. |

---

## 2. How did you use AI as a teammate?

**What the AI suggested:** The AI suggested extracting the core calculation mechanics out of `app.py` and implementing a distinct `check_guess` modular utility inside `logic_utils.py`.
- **Why it was correct:** This recommendation was correct because it successfully separated the visual Streamlit presentation layout from the transactional mathematics, making it easier to evaluate relational operators.
- **How you verified the result:** I verified this by launching the interface using Streamlit, submitting a test value of 50 against 74, and seeing the correct high/low hint appear dynamically.

 **What the AI suggested:** The AI initially proposed adding a highly complex, multi-tiered error logging library wrapper to catch non-integer string types in the input box.
- **Why it was rejected/modified:** I modified this approach because it was heavily over-engineered for our basic game context, so I chose to implement a straightforward, clean Python try-except block to handle input validation safely instead.
- **How you verified the result:** I verified this change by inputting arbitrary alphabetic characters into the guess input box and observing that the system caught the exception smoothly without breaking the active session state.


- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Copilot in VSCode
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I told it to fix the hint algorithm and that it was giving inverted advice. I verified the result by manually testing it and i asked it to make test cases and those passed.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
I asked it to make the attempts and history match, and at first the bug it gave me was very buggy. It would only accept every other attempt. Also the test cases it gave did really test what i asked it to test. I rewrote the prompt and it gave me the code i have now.

---

## 3. Debugging and testing your fixes

I verified the repairs across our files by using automated unit tests with the pytest framework. When running the test suite via the terminal, a total of 15 automated validation cases targeting boundary metrics, state transitions, and custom user values successfully passed in 0.02 seconds with absolute zero failures recorded. Additionally, manual end-to-end user playthroughs verified that the game safely reduces remaining available attempts down by 1 on incorrect entries and resets cleanly upon clicking the "New Game" interface control.




- How did you decide whether a bug was really fixed?
I had the AI make test cases, and when those passed, then i manually went in and checked. Thats when I noticed that the submission button was still buggy and went back to fix that bug.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
When I ran the pytest to check if the history was updating, it said it was valid, but when i ran it on my computer I was actually thrown an import error.
- Did AI help you design or understand any tests? How?
The AI helped me understand where the bug was and how they were linked to each other. When it was editing the code it summarized what was wrong and why the change would fix it. I was able to follow along and learn as it fixed the bug.

---

## 4. What did you learn about Streamlit and state?

Streamlit operates by completely rerunning the entire Python script from top to bottom every single time a user interacts with any interactive element or button on the screen. Because of this continuous rerun cycle, standard local variables are completely wiped and reset back to their starting values on every click, which originally caused our game's secret number to keep changing after each guess. To solve this, `st.session_state` acts like a short-term memory tracker for the website, securely storing data like the hidden target number, remaining attempt metrics, and guess logs safely in the background between page refreshes. Without implementing session state boundaries, a game application would be completely unplayable because it would reset its internal variables back to zero after every single submission.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns the script whenever the user interacts with a widget. `st.session_state` saves values like the secret number, attempts, and history between reruns. Without it, the game would reset its values after each interaction.

---

## 5. Looking ahead: your developer habits

Moving forward into future labs, I want to formally integrate writing automated test suites rather than relying entirely on manual hand-testing. While playing through the live UI helps with immediate verification, being able to construct targeted test cases with specific expected outputs inside pytest made it much faster to verify my code changes with absolute certainty. 

The next time I collaborate with an AI assistant on a coding task, I plan to be significantly more intentional and restrictive with my prompts. I noticed during this refactor that the assistant would frequently generate out-of-scope code blocks to "improve" things I never asked for, so keeping prompts tightly constrained will prevent that over-engineering. 

This project completely changed my perspective on AI-generated code by proving that automated outputs are rarely perfect, regardless of how specific your prompt is. It has a tendency to write massive, over-complicated blocks of software when a clean human-in-the-loop engineering fix actually only required switching a single relational operator from less-than to greater-than.

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
I want to write more test cases for projects. I usually go in and test by hand, but i like being able to make and run test cases with my desired outputs.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
One thing I would do differently is be more intentional with my prompts. I noticed that sometimes it would do other side things that were "improving the code" but were things I didn't ask for.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
It made me realize that the AI code it generates is never perfect no matter how specific you are. It likes to write a lot of code when it could have been 1 or two lines of changes or even something as easy as changing < to >.

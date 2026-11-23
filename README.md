# High Roller Dice - Vegas Casino Edition

A feature-rich dice gambling game with a casino aesthetic, available in both a **Tkinter Graphical UI** (`diceGUI.py`) and an interactive **Terminal / CLI Edition** (`dice.py`).

---

## Game Rules & Mechanics

### Goal
Roll a single die to accumulate a running total between **3 and 6** to win. If your total exceeds **20**, you **Bust** and lose your wager!

### Gameplay Loop
1. **Select Wager:** Choose between **$1**, **$5**, **$10**, or **$25** coins. Once you roll, your wager is locked for that round.
2. **Roll Die:** Adds a random roll (**1–6**) to your running total.
3. **Power Down:** Subtracts a random **1–5** from your total to help avoid busting.
   - ⚠️ *Warning:* Using Power Down 3 times in a row backfires and adds **+20** to your total!
4. **Check Out:** When your total is inside the win range (**3–6**), check out to win **double your wager** (`wager * 2`).
5. **Double Up Mode:**
   - On a win, you can choose to **Double Up** instead of cashing out.
   - Your payout carries forward as the next round's wager.
   - The win range narrows by 1 (e.g., 3–6 → 3–5 → 3–4 → 3–3).
   - Win again to double your pot again; bust and you lose the pot.
   - When the range reaches 3–3, winnings are automatically cashed out.

---

## Running the Game

### Requirements
- **Python 3.8+**
- **Pillow** (for GUI image rendering):
  ```bash
  pip install -r requirements.txt
  ```
- *Sound effects are supported on Windows via `winsound`.*

### 1. Graphical Interface (GUI)
Run the desktop GUI with felt green casino styling, visual dice faces, sound effects, and scoreboard:

```bash
python diceGUI.py
```
*(Also callable via `python dicevGUI.py`)*

### 2. Command Line Interface (CLI)
Play the full game in your terminal with single-die ASCII art:

```bash
python dice.py
```

#### CLI Controls:
- **`Enter`** or **`r`**: Roll single die
- **`p`**: Power Down (-1 to -5)
- **`c`**: Check Out (if total is within win range)
- **`w`**: Change wager (before rolling)
- **`g`**: Launch GUI version
- **`q`**: Quit and view session summary

---

## Project Structure

```
Dice/
├── dice.py            # Terminal / CLI High Roller game
├── diceGUI.py         # Tkinter GUI High Roller game
├── dicevGUI.py        # Alias launcher for diceGUI.py
├── requirements.txt   # Python dependencies (Pillow)
├── 1.png ... 6.png    # Die face images
├── 7.jpg              # Special die face image
├── *.wav              # Sound effect audio files
└── README.md          # Documentation
```

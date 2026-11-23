# Dice Arcade - Sleek Minimalist Terminal Dice Games

An interactive suite of sleek, eye-catching terminal dice games featuring the classic push-your-luck game **Pig**, **High Roller Casino**, and a **Free Dice Roller** with realistic tumbling animations and clean typography.

---

## Game Modes

### 1. Pig (Push Your Luck) — *Featured*
A fast-paced, addictive dice game of risk versus reward. Play against an intelligent **Computer AI Bot** or in **2-Player Local Pass & Play** mode!

- **Objective:** First player to reach **50 points** (or target score) wins.
- **Rules:**
  - On your turn, roll the die repeatedly to accumulate **Turn Points**.
  - **Roll 2–6:** The roll adds to your active turn points. Roll again or choose to bank.
  - **Roll a 1 ("Pig Out"):** You lose **all unbanked points** accumulated during that turn, and your turn ends immediately!
  - **Bank Points:** Safely adds your turn points to your permanent bank score.
- **Sleek Visuals:** Minimalist progress bars (`[██████░░░░] 25/50`), clean box-drawing frames, and dynamic tumbling roll animations.

### 2. High Roller (Vegas Casino CLI)
- Roll a single die to build a total inside the win range (**3–6**).
- Use **Power Down** (-1 to -5) to avoid busting over **20** (beware: 3 consecutive uses backfire!).
- Check out when in range to win double your wager, or **Double Up** to narrow the range and multiply your pot!

### 3. Free Dice Roller (Multi-Dice Sandbox)
- Roll anywhere from 1 to 5 dice simultaneously with ASCII art faces and running statistics (total rolls, highest total, average roll).

### 4. High Roller Desktop GUI (`diceGUI.py`)
- Full desktop Tkinter GUI application featuring green felt casino aesthetic, image-rendered dice faces, and sound effects.

---

## How to Run

### Requirements
- **Python 3.8+**
- **Pillow** (optional, needed only for GUI mode):
  ```bash
  pip install -r requirements.txt
  ```
- *Sound effects are supported automatically on Windows via `winsound`.*

### Launch Terminal Arcade
```bash
python dice.py
```

Press **`Enter`** at the main menu to immediately launch **Pig vs Computer Bot**!

#### Pig Controls:
- **`Enter`** or **`r`**: Roll die
- **`b`**: Bank points and pass turn
- **`q`**: Quit game

#### High Roller CLI Controls:
- **`Enter`** or **`r`**: Roll single die
- **`p`**: Power Down (-1 to -5)
- **`c`**: Check Out (if total is within win range)
- **`w`**: Change wager ($1, $5, $10, $25)
- **`g`**: Launch desktop GUI (`diceGUI.py`)
- **`q`**: Quit round

---

## Project Structure

```
Dice/
├── dice.py            # Terminal Dice Arcade (Pig, High Roller, Free Roller)
├── diceGUI.py         # Tkinter GUI High Roller game
├── dicevGUI.py        # Alias launcher for diceGUI.py
├── requirements.txt   # Python dependencies (Pillow)
├── 1.png ... 6.png    # Die face images
├── 7.jpg              # Special die face image
├── *.wav              # Sound effect audio files
└── README.md          # Documentation
```

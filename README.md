# Dice Arcade — Sleek Desktop GUI & Terminal Suite

A modern, minimalist dice game suite featuring the addictive push-your-luck game **Pig**, **High Roller Casino**, and a **Free Dice Roller**. Designed with an executive dark-mode aesthetic, smooth tumbling roll animations, visual progress meters, and dynamic AI opponents.

Available as both a **Sleek Desktop GUI** (`diceGUI.py`) and an interactive **Terminal / CLI Edition** (`dice.py`).

---

## 🎮 Game Modes

### 1. Pig (Push Your Luck) — *Featured*
A fast-paced, addictive dice game of risk versus reward. Play against an intelligent **Computer AI Bot** or in **2-Player Local Pass & Play** mode!

- **Objective:** First player to reach **50 points** wins.
- **Gameplay:**
  - On your turn, roll the die repeatedly to accumulate **Turn Points**.
  - **Roll 2–6:** The roll adds to your active turn points. Roll again or choose to bank.
  - **Roll a 1 ("Pig Out"):** You lose **all unbanked points** accumulated during that turn, and your turn ends immediately!
  - **Bank Points:** Safely locks your turn points into your permanent score.
- **Sleek Design:** Smooth 6-frame tumbling roll animation, minimalist progress bars (`0/50 pts`), clean card typography, and audio effects.

### 2. High Roller (Vegas Casino Mode)
- Roll a single die to build a total inside the win range (**3–6**).
- Use **Power Down** (-1 to -5) to avoid busting over **20** (beware: 3 consecutive uses backfire!).
- Check out when in range to win double your wager, or **Double Up** to narrow the range and multiply your pot!

### 3. Free Dice Roller (Multi-Dice Sandbox - CLI)
- Roll 1 to 5 dice simultaneously with ASCII art faces and running statistics (total rolls, highest total, average roll).

---

## 🚀 How to Run

### Requirements
- **Python 3.8+**
- **Pillow** (installed, required for desktop GUI image scaling):
  ```bash
  pip install -r requirements.txt
  ```
- *Audio is supported on Windows automatically via `winsound`.*

---

### Option A: Launch the Sleek Desktop GUI (Recommended)
Run the dedicated desktop GUI featuring smooth animations and executive dark theme:

```bash
python diceGUI.py
```
*(Also callable via `python dicevGUI.py` or `python dice.py --gui`)*

#### GUI Features:
- **Tab Switcher:** Seamlessly switch between **Pig Game** and **High Roller**.
- **AI Opponent:** Watch the computer bot make strategic push-your-luck decisions in real time.
- **Smooth Animations:** Tumbling die animations cycle dynamically before landing.
- **Audio Feedback:** Authentic sounds on roll, bank, win, and Pig Out.

---

### Option B: Launch Terminal / CLI Arcade
Run the clean ASCII terminal edition:

```bash
python dice.py
```

Press **`Enter`** at the main menu to immediately launch **Pig vs Computer Bot**!

#### CLI In-Game Controls:
- **`Enter`** or **`r`**: Roll die
- **`b`**: Bank points and pass turn
- **`g`**: Launch Desktop GUI
- **`q`**: Quit game

---

## 📁 Project Structure

```
Dice/
├── diceGUI.py         # Sleek Tkinter Desktop GUI (Pig & High Roller)
├── dicevGUI.py        # Alias launcher for diceGUI.py
├── dice.py            # Terminal Dice Arcade (Pig, High Roller, Free Roller)
├── requirements.txt   # Python dependencies (Pillow)
├── 1.png ... 6.png    # Die face images
├── 7.jpg              # Special die face image
├── *.wav              # Sound effect audio files
└── README.md          # Documentation
```

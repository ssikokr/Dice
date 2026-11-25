# Dice Arcade (V3 Edition)

A modern, minimalist dice game suite featuring the push-your-luck game **Pig**, **High Roller Casino**, and a **Free Dice Roller**. Designed with an executive dark-mode aesthetic, smooth tumbling roll animations, visual progress meters, and smart AI opponent.

Available as both a **Sleek Desktop GUI** (`diceGUI.py`) and an interactive **Terminal / CLI Edition** (`dice.py`).

---

## 🎲 New V3 Dice Rules & Mechanics

Version 3 introduces complete push-your-luck and casino gambling mechanics alongside the multi-dice rolling engine.

### 1. Pig (Push Your Luck) — *Flagship V3 Game*
A strategic race against an opponent (Computer AI or Player 2) where players push their luck each turn to reach the target score first.

- **Target Goal:** The first player to reach or exceed **50 points** wins the match.
- **Turn Sequence:**
  1. **Roll:** On your turn, roll the standard 6-sided die.
     - **Roll 2, 3, 4, 5, or 6:** The rolled value is added to your active **Turn Points** (at risk). You can choose to roll again to build a higher turn total, or bank your points.
     - **Roll a 1 ("Pig Out!"):** Your luck runs out! You lose **all unbanked points accumulated during that turn**, and your turn ends immediately. Control passes to the other player.
  2. **Bank:** You may stop rolling at any point to bank your accumulated turn points.
     - Banked points are permanently added to your total bank score.
     - Once banked, those points can never be lost.
     - Your turn ends and passes to the other player.
- **Opponent Modes:**
  - **Vs. Computer Bot (AI):** Play against an intelligent computer opponent that evaluates risk dynamically, banking when holding 15+ points or within striking distance of the win.
  - **2-Player Local:** Pass-and-play against a friend on the same machine.
- **Visual Meters:** Progress bars display score completion (`[██████░░░░] 25/50`) in real time.

---

### 2. High Roller (Vegas Casino Mode — Blind Rules)
An intense single-die target accumulation game with wagering, power-down risk mitigation, and hidden standing mechanics.

- **Target Win Range:** Accumulate a running total between **3 and 6** to win.
- **Bust Condition:** If your running total exceeds **20**, you **Bust** and lose your active wager or pot.
- **Blind / Hidden Standing Rules:**
  - **No Standing Indicators:** Your round total is **completely hidden** throughout the round.
  - **No Win Range Notifications:** You are never notified when you enter the win range or how close/far you are from winning or busting.
  - **Mental Tracking:** You must track your rolls and reductions mentally.
  - **High-Stakes Check Out:** You can attempt to Check Out at any point after rolling at least once. If your hidden total is inside the win range (3–6), you win **2× your wager**; if you are outside the win range, your check out fails and you lose the round!
- **Gameplay Flow:**
  1. **Place Wager:** Select **$1**, **$5**, **$10**, or **$25** coins before making your initial roll (wager locks upon first roll).
  2. **Roll Die:** Adds a single die roll (**1–6**) to your hidden running total.
  3. **Power Down:** Subtracts a random amount (**1–5**) from your hidden total to bring you back down towards the win range.
     - ⚠️ **Backfire Hazard:** Using Power Down 3 times in a row overloads the system, adding **+20** to your total and almost certainly causing a bust!
  4. **Check Out:** Call Check Out when you believe your hidden total is inside the win range (**3–6**).
  5. **Double Up Mode:**
     - After any win, you can choose to **Double Up** rather than cashing out.
     - Your entire payout carries forward as the wager for the next round.
     - The target win range narrows by 1 (e.g., 3–6 → 3–5 → 3–4 → 3–3).
     - Win again to double your pot again; bust or miss checkout and you forfeit the entire accumulated pot.

---

### 3. Free Dice Roller (Multi-Dice Sandbox)
A sandbox mode for rolling multiple dice with instant totals and session tracking.

- **Configurable Dice:** Roll between **1 and 5 dice** simultaneously.
- **Calculations:** Displays each individual die face with ASCII art along with the full summation equation (e.g. `2 + 5 + 4 = 11`).
- **Session Statistics:** Type `'s'` to view total rolls, total dice thrown, highest single-roll sum, and average roll total.

---

## 🖥️ How to Run & Controls

### Requirements
- **Python 3.8+**
- **Pillow** (required for desktop GUI dice face rendering):
  ```bash
  pip install -r requirements.txt
  ```
- *Asynchronous sound effects are natively supported on Windows via `winsound`.*

---

### Method 1: Desktop GUI (Recommended)
Run the dedicated desktop GUI featuring smooth tumbling animations and dark minimalist styling:

```bash
python diceGUI.py
```
*(Also launchable with `python dicevGUI.py` or `python dice.py --gui`)*

#### GUI Controls:
- **`🎲 ROLL DIE`**: Triggers a 6-frame tumbling roll animation.
- **`📥 BANK POINTS`**: Locks in your active turn points and passes the turn.
- **`● Vs Computer Bot / ○ 2-Player Local`**: Toggles opponent mode.
- **`🔄 Reset Match`**: Resets the current match scores.
- **Top Tabs**: Switch seamlessly between **Pig** and **High Roller**.

---

### Method 2: Terminal / CLI Edition
Run the lightweight terminal edition:

```bash
python dice.py
```

Press **`Enter`** at the launcher menu to start **Pig vs. Computer Bot** immediately!

#### CLI In-Game Controls:
- **`Enter`** or **`r`**: Roll die
- **`b`**: Bank points and pass turn
- **`g`**: Launch Desktop GUI
- **`q`**: Quit back to terminal

---

## 📁 Repository Structure

```
Dice/
├── diceGUI.py         # Sleek Tkinter Desktop GUI (Pig & High Roller)
├── dicevGUI.py        # Alias launcher for diceGUI.py
├── dice.py            # Terminal Dice Arcade (Pig, High Roller, Free Roller)
├── requirements.txt   # Python dependencies (Pillow)
├── 1.png ... 6.png    # Die face images
├── 7.jpg              # Special die face image
├── *.wav              # Sound effect audio files
└── README.md          # Complete documentation & V3 rules
```

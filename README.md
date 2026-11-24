# Dice Arcade (V4 Edition)

A modern, minimalist dice game suite featuring the push-your-luck game **Pig**, **High Roller Casino**, and a **Free Dice Roller**. Designed with an executive dark-mode aesthetic, smooth tumbling roll animations, visual progress meters, **4-Tier Dynamic AI Bots**, and a **Cross-Platform Audio Engine**.

Available as both a **Sleek Desktop GUI** (`diceGUI.py`) and an interactive **Terminal / CLI Edition** (`dice.py`).

---

## 🌟 What's New in Version 4

Version 4 introduces two major system upgrades:

### 1. 🧠 4-Tier Dynamic AI Opponent Engine (`ai_bot.py`)
No more one-size-fits-all computer opponent! You can now choose from 4 distinct strategic AI personalities when playing **Pig**:

* **🟢 Cautious (Easy)**:
  * Plays very defensively.
  * Banks early as soon as turn points reach **10**, minimizing Pig Out risks.
  * Perfect for beginners learning the game.
* **🔵 Balanced (Medium)**:
  * The classic V3 heuristic.
  * Banks at **15 points**, or at **10 points** once its score reaches 35+ to close out the match.
* **🟠 Aggressive (Hard)**:
  * A bold high-roller that chases big turn totals.
  * Pushes for at least **22 points** per turn, and if trailing by 15+ points, pushes even harder (**25+ points**).
* **🟣 Adaptive (Master)**:
  * Dynamically recalculates risk on every roll based on the live score difference and distance to the 50-point target:
    * If leading comfortably (+15 pts), plays conservatively and banks small gains (10–12 pts) to protect its lead.
    * If trailing an opponent near victory, gambles aggressively to catch up.
    * Always banks immediately if banked points + turn points will win the match.

Both the **GUI** (interactive difficulty buttons) and the **CLI** (menu prompt) let you select the AI personality on the fly!

---

### 2. 🔊 Cross-Platform Audio Engine & Sound Controls (`audio.py`)
* **True Cross-Platform Support**:
  * **Windows**: Native asynchronous sound via `winsound`.
  * **macOS**: Asynchronous native sound playback via `afplay`.
  * **Linux**: Native playback via `paplay` (PulseAudio), `aplay` (ALSA), or `play` (SoX).
  * **Headless / CI**: Automatic, silent fallback with zero external library overhead or crashes.
* **Sound Mute / Unmute Controls**:
  * **GUI**: Instant `🔊 Sound: ON` / `🔇 Sound: OFF` toggle button right in the header bar.
  * **CLI**: Toggle sound effects anytime using `[M]` in menus or during active gameplay.

---

## 🎲 Game Rules & Modes

### 1. Pig (Push Your Luck) — *Flagship Arcade Game*
A strategic race against an opponent (Computer Bot or Player 2) where players push their luck each turn to reach the target score first.

- **Target Goal:** The first player to reach or exceed **50 points** wins the match.
- **Turn Sequence:**
  1. **Roll:** On your turn, roll the standard 6-sided die.
     - **Roll 2, 3, 4, 5, or 6:** The rolled value is added to your active **Turn Points** (at risk). You can roll again to build a higher total, or bank your points.
     - **Roll a 1 ("Pig Out!"):** Your luck runs out! You lose **all unbanked points accumulated during that turn**, and your turn ends immediately.
  2. **Bank:** You may stop rolling at any point to bank your accumulated turn points.
     - Banked points are permanently added to your total score and can never be lost.
     - Control passes to the other player.
- **Opponent Modes:**
  - **Vs. Computer Bot:** Choose between **Cautious**, **Balanced**, **Aggressive**, or **Adaptive** AI.
  - **2-Player Local:** Pass-and-play against a friend on the same machine.
- **Visual Progress Meters:** Real-time visual progress bars display score completion (`[██████░░░░] 25/50`).

---

### 2. High Roller (Vegas Casino Mode — Blind Rules)
An intense single-die target accumulation game with wagering, power-down risk mitigation, and hidden standing mechanics.

- **Target Win Range:** Accumulate a running total between **3 and 6** to win.
- **Bust Condition:** If your running total exceeds **20**, you **Bust** and lose your active wager or pot.
- **Blind / Hidden Standing Rules:**
  - **No Standing Indicators:** Your round total is **completely hidden** throughout the round.
  - **No Win Range Notifications:** You are never told when you enter the win range; you must track your rolls and reductions mentally.
  - **High-Stakes Check Out:** Call Check Out when you believe your hidden total is inside the win range (**3–6**). If correct, you win **2× your wager**; if outside the range, you lose the round!
- **Gameplay Flow:**
  1. **Place Wager:** Select **$1**, **$5**, **$10**, or **$25** coins before rolling (wager locks upon first roll).
  2. **Roll Die:** Adds a single die roll (**1–6**) to your hidden running total.
  3. **Power Down:** Subtracts a random amount (**1–5**) from your hidden total to bring you back down towards the win range.
     - ⚠️ **Backfire Hazard:** Using Power Down 3 times in a row overloads the system, adding **+20** to your total and almost certainly causing a bust!
  4. **Check Out:** Call Check Out when your total is in the win range.
  5. **Double Up Mode:**
     - After any win, choose to **Double Up** rather than cashing out.
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
- *Audio is natively supported without extra libraries on Windows, macOS, and Linux.*

---

### Method 1: Desktop GUI (Recommended)
Run the dedicated desktop GUI featuring smooth tumbling animations, AI difficulty selector, and dark minimalist styling:

```bash
python diceGUI.py
```
*(Also launchable with `python dicevGUI.py` or `python dice.py --gui`)*

#### GUI Controls:
- **`🎲 ROLL DIE`**: Triggers a 6-frame tumbling roll animation.
- **`📥 BANK POINTS`**: Locks in your active turn points and passes the turn.
- **`● Vs Computer Bot / ○ 2-Player Local`**: Toggles opponent mode.
- **`Bot AI: [ Cautious | Balanced | Aggressive | Adaptive ]`**: Changes the computer's difficulty and risk profile.
- **`🔊 Sound: ON / OFF`**: Toggles sound effects in the header bar.
- **`🔄 Reset Match`**: Resets the current match scores.
- **Top Tabs**: Switch seamlessly between **Pig** and **High Roller**.

---

### Method 2: Terminal / CLI Edition
Run the lightweight terminal edition:

```bash
python dice.py
```

Press **`Enter`** at the launcher menu to start **Pig vs. Adaptive Bot** immediately!

#### CLI In-Game Controls:
- **`Enter`** or **`r`**: Roll die
- **`b`**: Bank points and pass turn
- **`m`**: Toggle sound effects ON / OFF
- **`g`**: Launch Desktop GUI
- **`q`**: Quit back to terminal

---

## 📁 Repository Structure

```
Dice/
├── diceGUI.py         # Sleek Tkinter Desktop GUI (Pig & High Roller)
├── dicevGUI.py        # Alias launcher for diceGUI.py
├── dice.py            # Terminal Dice Arcade (Pig, High Roller, Free Roller)
├── ai_bot.py          # 4-Tier Dynamic Bot AI logic & decision trees (V4)
├── audio.py           # Cross-platform sound engine (Windows/macOS/Linux) (V4)
├── requirements.txt   # Python dependencies (Pillow)
├── .github/workflows/ # GitHub Actions CI workflows (Pylint & Run Game)
│   ├── pylint.yml
│   └── run-game.yml
├── 1.png ... 6.png    # Die face images
├── 7.jpg              # Special die face image
├── *.wav              # Sound effect audio files
└── README.md          # Complete documentation & V4 rules
```

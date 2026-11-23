# Simple Digital Dice Roller

A lightweight, interactive Python application that simulates rolling standard six-sided dice. This project demonstrates foundational programming concepts such as loops, user input handling, string formatting, and the use of built-in libraries.

## Features
* **Visual Dice Faces:** Displays realistic ASCII art representation for each rolled die side-by-side.
* **Configurable Dice Count:** Roll anywhere from 1 to 5 dice simultaneously, showing individual dice values and their total sum.
* **Session Statistics:** Track total rolls, total dice rolled, highest total score, and average roll total across your session.
* **Interactive Interface:** Seamless controls to roll (Enter), change dice count (`1`-`5`), view stats (`s`), or quit (`q`).
* **Robust Execution:** Handles interrupts (Ctrl+C) and non-interactive environments gracefully.

## How to Run
1. Ensure you have **Python 3** installed on your computer.
2. Open your terminal or command prompt.
3. Navigate to the folder containing `dice.py`.
4. Run the following command:
   ```bash
   python dice.py
   ```

## Controls
- **Enter:** Roll dice
- **1-5:** Change number of dice to roll (default: 2)
- **s:** Display current session statistics
- **q:** Quit game

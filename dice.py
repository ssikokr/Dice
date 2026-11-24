"""Dice Arcade - Sleek Minimalist Terminal Dice Games.

V4 Edition Features:
1. Pig: The classic push-your-luck game (vs 4-Tier Dynamic AI or 2-Player).
   - Dynamic Bot AI: Cautious, Balanced, Aggressive, and Adaptive (Master).
2. High Roller: Vegas casino-style target range gambling.
3. Free Roller: Multi-dice sandbox with session statistics.
4. Cross-Platform Audio: Windows, macOS, and Linux sound engine with Mute toggle.
"""

import os
import random
import subprocess
import sys
import time

from ai_bot import AI_DIFFICULTIES, evaluate_bot_decision, get_difficulty_name
from audio import is_sound_enabled, play_sound, toggle_sound

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DICE_FACES = {
    1: (
        "┌─────────┐",
        "│         │",
        "│    o    │",
        "│         │",
        "└─────────┘",
    ),
    2: (
        "┌─────────┐",
        "│  o      │",
        "│         │",
        "│      o  │",
        "└─────────┘",
    ),
    3: (
        "┌─────────┐",
        "│  o      │",
        "│    o    │",
        "│      o  │",
        "└─────────┘",
    ),
    4: (
        "┌─────────┐",
        "│  o   o  │",
        "│         │",
        "│  o   o  │",
        "└─────────┘",
    ),
    5: (
        "┌─────────┐",
        "│  o   o  │",
        "│    o    │",
        "│  o   o  │",
        "└─────────┘",
    ),
    6: (
        "┌─────────┐",
        "│  o   o  │",
        "│  o   o  │",
        "│  o   o  │",
        "└─────────┘",
    ),
}


def render_dice_art(dice_values):
    """Render one or more dice side-by-side using sleek ASCII art.

    Args:
        dice_values: A list of integers (1-6).

    Returns:
        A formatted string representing the dice rendered side by side.
    """
    lines = ["", "", "", "", ""]
    for val in dice_values:
        art = DICE_FACES.get(val, DICE_FACES[1])
        for i in range(5):
            lines[i] += art[i] + "  "
    return "\n".join(lines)


def animated_roll(num_dice=1, animate=True):
    """Roll dice with an optional sleek tumbling animation.

    Args:
        num_dice: Number of dice to roll (default: 1).
        animate: Whether to display tumbling frames (skipped if non-interactive).

    Returns:
        List of rolled integer values.
    """
    is_interactive = sys.stdout.isatty() and animate
    play_sound("roll.wav")

    if is_interactive:
        frames = 5
        for _ in range(frames):
            temp_rolls = [random.randint(1, 6) for _ in range(num_dice)]
            dice_repr = " ".join(f"[{v}]" for v in temp_rolls)
            sys.stdout.write(f"\r  Rolling... {dice_repr} ")
            sys.stdout.flush()
            time.sleep(0.06)
        sys.stdout.write("\r" + " " * 32 + "\r")
        sys.stdout.flush()

    return [random.randint(1, 6) for _ in range(num_dice)]


def make_progress_bar(current, target, width=16):
    """Generate a sleek, minimalist text progress bar."""
    ratio = min(1.0, max(0.0, current / target if target > 0 else 0.0))
    filled = int(round(ratio * width))
    empty = width - filled
    progress_str = "█" * filled + "░" * empty
    return f"[{progress_str}] {current:2d}/{target}"


class PigGame:
    """Sleek implementation of the classic Pig push-your-luck dice game."""

    def __init__(self, target_score=50, vs_bot=True, ai_difficulty="balanced"):
        self.target_score = target_score
        self.vs_bot = vs_bot
        self.ai_difficulty = ai_difficulty.lower()
        diff_label = get_difficulty_name(self.ai_difficulty)
        self.scores = [0, 0]
        self.names = ["Player", f"Bot ({diff_label})"] if vs_bot else ["Player 1", "Player 2"]
        self.current_turn = 0
        self.turn_score = 0

    def show_scoreboard(self):
        """Display a clean, minimalist scoreboard with progress bars."""
        p1_bar = make_progress_bar(self.scores[0], self.target_score)
        p2_bar = make_progress_bar(self.scores[1], self.target_score)

        print("\n┌────────────────────────────────────────────────────────┐")
        print(f"│  PIG — PUSH YOUR LUCK                    Target: {self.target_score:<5} │")
        print("├────────────────────────────────────────────────────────┤")
        print(f"│  {self.names[0]:<12}: {p1_bar:<39}│")
        print(f"│  {self.names[1]:<12}: {p2_bar:<39}│")
        print("└────────────────────────────────────────────────────────┘")

    def switch_turn(self):
        """Switch active turn between players."""
        self.turn_score = 0
        self.current_turn = 1 - self.current_turn

    def play_bot_turn(self):
        """Execute the computer bot's turn with strategic risk thresholds."""
        print(f"\n>> {self.names[1]}'s turn...")
        if sys.stdout.isatty():
            time.sleep(0.5)

        while True:
            # Check if bot decides to bank
            if evaluate_bot_decision(
                self.ai_difficulty,
                self.turn_score,
                self.scores[1],
                self.scores[0],
                self.target_score,
            ):
                break

            roll = animated_roll(1)[0]
            print(f"  {self.names[1]} rolled a {roll}:")
            print(render_dice_art([roll]))

            if roll == 1:
                play_sound("lose.wav")
                print(f"  >> 💥 PIG OUT! {self.names[1]} rolled a 1 — turn points lost.\n")
                self.switch_turn()
                return

            self.turn_score += roll
            projected = self.scores[1] + self.turn_score
            print(f"  (Turn: +{self.turn_score} | Bank if held: {projected}/{self.target_score})\n")

            if projected >= self.target_score:
                break

            if sys.stdout.isatty():
                time.sleep(0.4)

        self.scores[1] += self.turn_score
        play_sound("neutral.wav")
        print(f"  >> 💰 {self.names[1]} banks {self.turn_score} points! Total: {self.scores[1]}/{self.target_score}\n")
        self.switch_turn()

    def run(self):
        """Run the Pig game loop."""
        print("\n========================================================")
        print("                 P I G   D I C E   G A M E              ")
        print("========================================================")
        print(f"Rules: First to {self.target_score} points wins!")
        if self.vs_bot:
            diff_desc = AI_DIFFICULTIES.get(self.ai_difficulty, {}).get("description", "")
            print(f"Opponent: {self.names[1]} — {diff_desc}")
        print("• Roll repeatedly to accumulate turn points.")
        print("• Roll a 1 ('Pig Out') and you lose all unbanked points this turn!")
        print("• Bank anytime to permanently lock in your turn score.\n")

        while max(self.scores) < self.target_score:
            self.show_scoreboard()

            if self.vs_bot and self.current_turn == 1:
                self.play_bot_turn()
                continue

            active_name = self.names[self.current_turn]
            projected = self.scores[self.current_turn] + self.turn_score
            print(f"Active: {active_name} | Turn Points: +{self.turn_score} | Projected: {projected}/{self.target_score}")
            prompt = "Action: [Enter/R]oll | [B]ank points | [M]ute/Sound | [Q]uit game: "

            try:
                action = input(prompt).strip().lower()
            except EOFError:
                print("\n[Non-interactive environment detected: performing demo turn]")
                action = "r"
            except KeyboardInterrupt:
                print("\nGame session cancelled.")
                break

            if action in ("q", "quit", "exit"):
                print("\nExiting Pig game. Thanks for playing!")
                break

            if action in ("m", "mute", "sound"):
                state = toggle_sound()
                print(f"\n  >> Sound effects turned {'ON' if state else 'OFF'}.\n")
                continue

            if action in ("b", "bank", "hold"):
                if self.turn_score == 0:
                    print("  (!) You must roll at least once before banking!\n")
                    continue
                self.scores[self.current_turn] += self.turn_score
                play_sound("neutral.wav")
                print(f"\n  >> 💰 Banked {self.turn_score} points! Total: {self.scores[self.current_turn]}/{self.target_score}\n")
                if self.scores[self.current_turn] >= self.target_score:
                    break
                self.switch_turn()
                continue

            if action in ("", "r", "roll"):
                roll = animated_roll(1)[0]
                print(f"\nYou rolled a {roll}:")
                print(render_dice_art([roll]))

                if roll == 1:
                    play_sound("lose.wav")
                    print("  >> 💥 PIG OUT! You rolled a 1 — all unbanked turn points lost!\n")
                    self.switch_turn()
                    if not sys.stdout.isatty():
                        break
                else:
                    self.turn_score += roll
                    total_proj = self.scores[self.current_turn] + self.turn_score
                    if total_proj >= self.target_score:
                        self.scores[self.current_turn] = total_proj
                        play_sound("win.wav")
                        break
                    print(f"  (Turn Points: +{self.turn_score} | Bank if held: {total_proj}/{self.target_score})\n")
                    if not sys.stdout.isatty():
                        break
            else:
                print(f"Unknown action '{action}'. Choose [R]oll, [B]ank, [M]ute, or [Q]uit.\n")

        if max(self.scores) >= self.target_score:
            self.show_scoreboard()
            winner_idx = 0 if self.scores[0] >= self.target_score else 1
            play_sound("win.wav")
            print(f"\n🏆 VICTORY! {self.names[winner_idx]} has won the match with {self.scores[winner_idx]} points!\n")


WIN_LOW = 3
WIN_HIGH_START = 6
BUST_THRESHOLD = 20
WAGER_OPTIONS = [1, 5, 10, 25]


class HighRollerCLI:
    """CLI implementation of the High Roller Dice game."""

    def __init__(self):
        self.session_wins = 0
        self.session_losses = 0
        self.current_wager = 5
        self.wager_locked = False
        self.total = 0
        self.rolled_this_round = False
        self.power_down_streak = 0
        self.double_up_mode = False
        self.accumulated_pot = 0
        self.win_high = WIN_HIGH_START

    def reset_round(self):
        """Reset state for a new round."""
        self.total = 0
        self.rolled_this_round = False
        self.power_down_streak = 0
        if not self.double_up_mode:
            self.wager_locked = False

    def show_scoreboard(self):
        """Print the current scoreboard and balance."""
        mode_str = " [DOUBLE UP ACTIVE]" if self.double_up_mode else ""
        print("\n┌────────────────────────────────────────────────────────┐")
        print(f"│  HIGH ROLLER CASINO{mode_str:<35}│")
        print("├────────────────────────────────────────────────────────┤")
        print(f"│  Wins: {self.session_wins:<4} | Losses: {self.session_losses:<4} | Pot: {self.accumulated_pot} coins | Wager: ${self.current_wager:<4} │")
        print(f"│  Target Range: {WIN_LOW}–{self.win_high:<2} | Bust Threshold: >{BUST_THRESHOLD:<2}              │")
        print("│  Round Total: [Hidden — track in your head!]           │")
        print("└────────────────────────────────────────────────────────┘")

    def set_wager_prompt(self):
        """Allow player to set wager before rolling."""
        if self.wager_locked or self.double_up_mode:
            print("\nWager is currently locked for this round!\n")
            return
        print(f"\nAvailable wagers: {WAGER_OPTIONS}")
        try:
            choice = input(f"Select wager (${self.current_wager}): ").strip()
            if choice.isdigit() and int(choice) in WAGER_OPTIONS:
                self.current_wager = int(choice)
                print(f"Wager set to ${self.current_wager}.\n")
            elif choice:
                print(f"Invalid wager. Keeping ${self.current_wager}.\n")
        except (EOFError, KeyboardInterrupt):
            pass

    def roll_die(self):
        """Roll a single die and add to total."""
        if not self.rolled_this_round:
            self.wager_locked = True
        self.rolled_this_round = True
        self.power_down_streak = 0

        roll = animated_roll(1)[0]
        self.total += roll

        print(f"\nYou rolled a {roll}!")
        print(render_dice_art([roll]))

        if self.total > BUST_THRESHOLD:
            self.handle_bust(f"Exceeded {BUST_THRESHOLD}! Final total was {self.total}.")
            return False
        return True

    def power_down(self):
        """Perform Power Down to reduce total."""
        if not self.rolled_this_round:
            print("\nYou must roll at least once before using Power Down!\n")
            return True

        self.power_down_streak += 1
        if self.power_down_streak == 3:
            self.total += 20
            self.power_down_streak = 0
            play_sound("backfire.wav")
            print("\n💥 Power Down BACKFIRED! +20 added to your hidden total!\n")
            if self.total > BUST_THRESHOLD:
                self.handle_bust(f"Power Down backfire exceeded {BUST_THRESHOLD}! Final total was {self.total}.")
                return False
        else:
            reduction = random.randint(1, 5)
            self.total = max(0, self.total - reduction)
            play_sound("powerdown.wav")
            print(f"\n⚡ Power Down activated! -{reduction} (Streak: {self.power_down_streak}/3)\n")
        return True

    def checkout(self):
        """Attempt to check out if total is in win range."""
        if not self.rolled_this_round:
            print("\nYou must roll at least once before checking out!\n")
            return None

        if WIN_LOW <= self.total <= self.win_high:
            return self.handle_win()

        self.handle_bust(f"Failed Check Out! Final total was {self.total} (outside {WIN_LOW}–{self.win_high}).")
        return False

    def handle_bust(self, reason):
        """Handle player bust."""
        lost_amount = self.accumulated_pot if self.double_up_mode else self.current_wager
        self.session_losses += 1
        play_sound("lose.wav")
        print(f"\n💀 BUST! {reason}")
        print(f"You lost {lost_amount} coin(s)!\n")

        self.double_up_mode = False
        self.accumulated_pot = 0
        self.win_high = WIN_HIGH_START
        self.reset_round()

    def handle_win(self):
        """Handle player win with Double Up decision."""
        self.session_wins += 1
        payout = self.current_wager * 2
        new_pot = self.accumulated_pot + payout if self.double_up_mode else payout
        play_sound("win.wav")

        print(f"\n👑 WINNER! Total is {self.total} — inside {WIN_LOW}–{self.win_high}!")
        print(f"You won {payout} coins this round!")

        can_double = (self.win_high - 1) >= WIN_LOW
        going_double = False

        if can_double:
            try:
                prompt = (
                    f"\nDOUBLE UP?\n"
                    f"  • Carry {payout} coins into next round as wager\n"
                    f"  • Win range shrinks to {WIN_LOW}–{self.win_high - 1}\n"
                    f"  • Win = double pot again | Bust = lose pot\n"
                    f"Double Up? (y/N): "
                )
                ans = input(prompt).strip().lower()
                going_double = ans in ("y", "yes")
            except (EOFError, KeyboardInterrupt):
                going_double = False

        if going_double:
            self.double_up_mode = True
            self.accumulated_pot = new_pot
            self.current_wager = payout
            self.win_high -= 1
            print(f"🔥 DOUBLE UP ACTIVE! Next round wager: ${self.current_wager}, Range: {WIN_LOW}–{self.win_high}\n")
            self.reset_round()
        else:
            print(f"💰 Cashed out {new_pot} coins! Great round!\n")
            self.double_up_mode = False
            self.accumulated_pot = 0
            self.win_high = WIN_HIGH_START
            self.reset_round()

        return True

    def run(self):
        """Main game loop for High Roller."""
        print("\n========================================================")
        print("                 H I G H   R O L L E R                  ")
        print("========================================================")
        print(f"Rules: Roll 1 die to build a total between {WIN_LOW} and {self.win_high}.")
        print("Use Power Down strategically to avoid busting over 20!\n")

        while True:
            self.show_scoreboard()
            prompt = (
                "Actions: [Enter/R]oll | [P]ower Down | [C]heck Out | "
                "[W]ager | [M]ute/Sound | [G]UI | [Q]uit: "
            )
            try:
                action = input(prompt).strip().lower()
            except EOFError:
                if self.session_wins == 0 and self.session_losses == 0:
                    self.roll_die()
                    if WIN_LOW <= self.total <= self.win_high:
                        self.checkout()
                break
            except KeyboardInterrupt:
                break

            if action in ("q", "quit", "exit"):
                print("\nThanks for playing High Roller!")
                break
            if action in ("m", "mute", "sound"):
                state = toggle_sound()
                print(f"\n  >> Sound effects turned {'ON' if state else 'OFF'}.\n")
                continue
            if action in ("", "r", "roll"):
                self.roll_die()
            elif action in ("p", "power", "powerdown"):
                self.power_down()
            elif action in ("c", "checkout", "check"):
                self.checkout()
            elif action in ("w", "wager"):
                self.set_wager_prompt()
            elif action in ("g", "gui"):
                launch_gui()
            else:
                print(f"Unknown action '{action}'. Choose [R]oll, [P]ower Down, [C]heck Out, [W]ager, [M]ute, or [Q]uit.\n")


def free_dice_roller():
    """Interactive multi-dice rolling sandbox with session statistics."""
    print("\n========================================================")
    print("             F R E E   D I C E   R O L L E R            ")
    print("========================================================")
    print("Roll 1 to 5 dice at once with realistic ASCII visuals and stats.\n")

    stats = {
        "total_rolls": 0,
        "total_dice": 0,
        "highest_total": 0,
        "sum_of_totals": 0,
    }
    num_dice = 2

    while True:
        try:
            prompt = (
                f"Press Enter to roll ({num_dice} dice), "
                "1-5 to change count, 's' for stats, 'q' to quit: "
            )
            choice = input(prompt).strip().lower()
        except EOFError:
            if stats["total_rolls"] == 0:
                choice = ""
            else:
                break
        except KeyboardInterrupt:
            break

        if choice in ("q", "quit", "exit"):
            print("\nSession complete.")
            break

        if choice == "s":
            if stats["total_rolls"] == 0:
                print("\nNo rolls recorded yet!\n")
            else:
                avg = stats["sum_of_totals"] / stats["total_rolls"]
                print("\n--- Session Statistics ---")
                print(f"Total Rolls     : {stats['total_rolls']}")
                print(f"Dice Rolled     : {stats['total_dice']}")
                print(f"Highest Total   : {stats['highest_total']}")
                print(f"Average Total   : {avg:.2f}")
                print("--------------------------\n")
            continue

        if choice.isdigit():
            count = int(choice)
            if 1 <= count <= 5:
                num_dice = count
                print(f"Dice count set to {num_dice}.\n")
            else:
                print("Please enter a number between 1 and 5.\n")
            continue

        if choice != "":
            print(f"Unknown option '{choice}'. Press Enter to roll, or 'q' to quit.\n")
            continue

        rolls = animated_roll(num_dice)
        total = sum(rolls)

        stats["total_rolls"] += 1
        stats["total_dice"] += num_dice
        stats["sum_of_totals"] += total
        if total > stats["highest_total"]:
            stats["highest_total"] = total

        print(f"\nRoll #{stats['total_rolls']}:")
        print(render_dice_art(rolls))
        if num_dice == 1:
            print(f"You got: {rolls[0]}\n")
        else:
            dice_str = " + ".join(str(r) for r in rolls)
            print(f"You got: {dice_str} = {total} (Total: {total})\n")


def launch_gui():
    """Launch the sleek desktop GUI."""
    print("Launching sleek Desktop GUI (diceGUI.py)...")
    try:
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "diceGUI.py")])
    except (OSError, ValueError) as exc:
        print(f"Could not launch GUI: {exc}")


def start_game():
    """Main launcher entrypoint offering all dice game modes."""
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--gui", "-g", "gui"):
        launch_gui()
        return

    while True:
        sound_status = "ON" if is_sound_enabled() else "OFF"
        print("┌────────────────────────────────────────────────────────┐")
        print("│                   D I C E   A R C A D E                │")
        print("│       V4 Edition: Dynamic AI & Cross-Platform Audio    │")
        print("└────────────────────────────────────────────────────────┘")
        print("  [1] Play Pig (vs Computer Bot)  -- [Default]")
        print("  [2] Play Pig (2-Player Pass & Play)")
        print("  [3] High Roller (Casino Win Range)")
        print("  [4] Free Dice Roller (1-5 Dice & Stats)")
        print(f"  [M] Toggle Sound Effects [{sound_status}]")
        print("  [G] Launch Sleek Desktop GUI")
        print("  [Q] Quit")
        print()

        try:
            choice = input("Select an option [1-4, M, G, Q] (Press Enter for Pig vs Bot): ").strip().lower()
        except EOFError:
            choice = "1"
        except KeyboardInterrupt:
            return

        if choice in ("", "1"):
            print("\nSelect Bot AI Difficulty:")
            print("  [1] Cautious   (Easy — Banks early at 10 pts)")
            print("  [2] Balanced   (Medium — Classic V3 Heuristic)")
            print("  [3] Aggressive (Hard — Chases 22+ pts)")
            print("  [4] Adaptive   (Master — Dynamic Risk Evaluator) -- [Default]")
            try:
                diff_input = input("Choose difficulty [1-4] (Press Enter for Adaptive): ").strip().lower()
            except EOFError:
                diff_input = "4"
            except KeyboardInterrupt:
                continue

            diff_map = {
                "1": "cautious",
                "2": "balanced",
                "3": "aggressive",
                "4": "adaptive",
            }
            chosen_diff = diff_map.get(diff_input, "adaptive")
            PigGame(target_score=50, vs_bot=True, ai_difficulty=chosen_diff).run()
            if not sys.stdout.isatty():
                break
        elif choice == "2":
            PigGame(target_score=50, vs_bot=False).run()
            if not sys.stdout.isatty():
                break
        elif choice == "3":
            HighRollerCLI().run()
            if not sys.stdout.isatty():
                break
        elif choice == "4":
            free_dice_roller()
            if not sys.stdout.isatty():
                break
        elif choice in ("m", "sound", "mute"):
            new_state = toggle_sound()
            print(f"\n>> Sound effects turned {'ON' if new_state else 'OFF'}.\n")
        elif choice in ("g", "gui", "0"):
            launch_gui()
            if not sys.stdout.isatty():
                break
        elif choice in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        else:
            print(f"Unknown choice '{choice}'. Launching Pig vs Bot...")
            PigGame(target_score=50, vs_bot=True, ai_difficulty="adaptive").run()
            if not sys.stdout.isatty():
                break


if __name__ == "__main__":
    start_game()

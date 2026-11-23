"""High Roller Dice Game (CLI Edition).

A dice gambling game based on High Roller Dice (diceGUI.py).
Roll a single die, accumulate your total towards the target win range (3-6),
use Power Down strategically to avoid busting over 20, and risk it all
with Double Up!
"""

import os
import random
import subprocess
import sys

# Theme & Win Range Constants matching diceGUI.py
WIN_LOW = 3
WIN_HIGH_START = 6
BUST_THRESHOLD = 20
WAGER_OPTIONS = [1, 5, 10, 25]

# Single-die ASCII Art representation (1-7)
DICE_ART = {
    1: (
        "+-------+",
        "|       |",
        "|   o   |",
        "|       |",
        "+-------+",
    ),
    2: (
        "+-------+",
        "| o     |",
        "|       |",
        "|     o |",
        "+-------+",
    ),
    3: (
        "+-------+",
        "| o     |",
        "|   o   |",
        "|     o |",
        "+-------+",
    ),
    4: (
        "+-------+",
        "| o   o |",
        "|       |",
        "| o   o |",
        "+-------+",
    ),
    5: (
        "+-------+",
        "| o   o |",
        "|   o   |",
        "| o   o |",
        "+-------+",
    ),
    6: (
        "+-------+",
        "| o   o |",
        "| o   o |",
        "| o   o |",
        "+-------+",
    ),
    7: (
        "+-------+",
        "| o   o |",
        "| o o o |",
        "| o   o |",
        "+-------+",
    ),
}


def render_die(val):
    """Return ASCII art string for a single die.

    Args:
        val: Integer value representing the die face.

    Returns:
        Rendered ASCII string representation of the die.
    """
    art = DICE_ART.get(val, DICE_ART[1])
    return "\n".join(art)


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

    def reset_round(self, full_session=False):
        """Reset state for a new round or full session."""
        self.total = 0
        self.rolled_this_round = False
        self.power_down_streak = 0

        if full_session:
            self.win_high = WIN_HIGH_START
            self.double_up_mode = False
            self.accumulated_pot = 0
            self.current_wager = 5
            self.session_wins = 0
            self.session_losses = 0

        if not self.double_up_mode:
            self.wager_locked = False

    def show_scoreboard(self):
        """Print the current scoreboard and balance."""
        mode_str = " 🔥 DOUBLE UP MODE 🔥" if self.double_up_mode else ""
        print("\n" + "=" * 48)
        print(f" [HIGH ROLLER DICE]{mode_str}")
        print(f" WINS: {self.session_wins} | LOSSES: {self.session_losses} | POT: {self.accumulated_pot} coins")
        print(f" WIN RANGE: {WIN_LOW}–{self.win_high} | BUST AT: >{BUST_THRESHOLD} | WAGER: ${self.current_wager}")
        print(f" CURRENT ROUND TOTAL: {self.total}")
        print("=" * 48)

    def set_wager_prompt(self):
        """Allow player to set wager before rolling."""
        if self.wager_locked or self.double_up_mode:
            print("\nWager is currently locked for this round!")
            return
        print(f"\nAvailable wagers: {WAGER_OPTIONS}")
        try:
            choice = input(f"Select wager (${self.current_wager}): ").strip()
            if choice.isdigit() and int(choice) in WAGER_OPTIONS:
                self.current_wager = int(choice)
                print(f"Wager set to ${self.current_wager}.")
            elif choice:
                print(f"Invalid wager. Keeping ${self.current_wager}.")
        except (EOFError, KeyboardInterrupt):
            pass

    def roll_die(self):
        """Roll a single die and add to total."""
        if not self.rolled_this_round:
            self.wager_locked = True
        self.rolled_this_round = True
        self.power_down_streak = 0

        roll = random.randint(1, 6)
        self.total += roll

        print(f"\nYou rolled a {roll}!")
        print(render_die(roll))
        print(f"Running Total: {self.total} (Win range: {WIN_LOW}–{self.win_high})\n")

        if self.total > BUST_THRESHOLD:
            self.handle_bust(f"Total reached {self.total} — over {BUST_THRESHOLD}!")
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
            print("\n💥 Power Down BACKFIRED! +20 added to your total!")
            print(f"Running Total: {self.total}\n")
            if self.total > BUST_THRESHOLD:
                self.handle_bust("Power Down overload caused a bust!")
                return False
        else:
            reduction = random.randint(1, 5)
            self.total = max(0, self.total - reduction)
            print(f"\n⚡ Power Down activated! -{reduction} (Streak: {self.power_down_streak}/3)")
            print(f"Running Total: {self.total} (Win range: {WIN_LOW}–{self.win_high})\n")
        return True

    def checkout(self):
        """Attempt to check out if total is in win range."""
        if not self.rolled_this_round:
            print("\nYou must roll at least once before checking out!\n")
            return None

        if WIN_LOW <= self.total <= self.win_high:
            return self.handle_win()

        print(f"\nNot there yet! Your total is {self.total}.")
        print(f"You need between {WIN_LOW} and {self.win_high} to win.\n")
        return None

    def handle_bust(self, reason):
        """Handle player bust."""
        lost_amount = self.accumulated_pot if self.double_up_mode else self.current_wager
        self.session_losses += 1
        print(f"\n💀 BUST! {reason}")
        print(f"You lost {lost_amount} coin(s)!")

        self.double_up_mode = False
        self.accumulated_pot = 0
        self.win_high = WIN_HIGH_START
        self.reset_round()

    def handle_win(self):
        """Handle player win with Double Up decision."""
        self.session_wins += 1
        payout = self.current_wager * 2
        new_pot = self.accumulated_pot + payout if self.double_up_mode else payout

        print(f"\n👑 KING! Total is {self.total} — inside {WIN_LOW}–{self.win_high}!")
        print(f"You won {payout} coins this round!")

        can_double = (self.win_high - 1) >= WIN_LOW
        going_double = False

        if can_double:
            try:
                prompt = (
                    f"\n🔥 DOUBLE UP?\n"
                    f"  • Carry {payout} coins into next round as wager\n"
                    f"  • Win range shrinks to {WIN_LOW}–{self.win_high - 1}\n"
                    f"  • Win = double your pot again | Bust = lose everything\n"
                    f"Double Up? (y/N): "
                )
                ans = input(prompt).strip().lower()
                going_double = ans in ("y", "yes")
            except (EOFError, KeyboardInterrupt):
                going_double = False
        else:
            print(f"Win range is at minimum ({WIN_LOW}–{self.win_high}). Cashing out automatically!")

        if going_double:
            self.double_up_mode = True
            self.accumulated_pot = new_pot
            self.current_wager = payout
            self.win_high -= 1
            print(f"🔥 DOUBLE UP ACTIVE! Next round wager: ${self.current_wager}, Range: {WIN_LOW}–{self.win_high}")
            self.reset_round()
        else:
            print(f"💰 Cashed out {new_pot} coins! Great game!")
            self.double_up_mode = False
            self.accumulated_pot = 0
            self.win_high = WIN_HIGH_START
            self.reset_round()

        return True

    def run(self):
        """Main game loop."""
        print("=========================================")
        print("   🎰 HIGH ROLLER DICE (Vegas Casino) 🎰   ")
        print("=========================================")
        print("Rules:")
        print(f" • Roll 1 die to build a total between {WIN_LOW} and {self.win_high}.")
        print(" • Use Power Down (-1 to -5) if you get close to 20.")
        print(f" • Exceed {BUST_THRESHOLD} and you BUST!")
        print(" • Win and Double Up to shrink the win range and multiply winnings!\n")

        while True:
            self.show_scoreboard()
            prompt = (
                "Actions: [Enter/R]oll | [P]ower Down | [C]heck Out | "
                "[W]ager | [G]UI | [Q]uit: "
            )
            try:
                action = input(prompt).strip().lower()
            except EOFError:
                if self.session_wins == 0 and self.session_losses == 0:
                    print("\n[Non-interactive mode: running demo roll]")
                    self.roll_die()
                    if WIN_LOW <= self.total <= self.win_high:
                        self.checkout()
                    print("\nDemo completed. Exiting.")
                break
            except KeyboardInterrupt:
                print("\nSession interrupted.")
                break

            if action in ("q", "quit", "exit"):
                print("\nThanks for playing High Roller Dice!")
                self.show_scoreboard()
                break

            if action in ("", "r", "roll"):
                self.roll_die()
            elif action in ("p", "power", "powerdown"):
                self.power_down()
            elif action in ("c", "checkout", "check"):
                self.checkout()
            elif action in ("w", "wager"):
                self.set_wager_prompt()
            elif action in ("g", "gui"):
                print("Launching GUI version (diceGUI.py)...")
                try:
                    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "diceGUI.py")])
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    print(f"Could not launch GUI: {exc}")
            else:
                print(f"Unknown action '{action}'. Choose [R]oll, [P]ower Down, [C]heck Out, [W]ager, or [Q]uit.")


def start_game():
    """Start the High Roller CLI game."""
    game = HighRollerCLI()
    game.run()


if __name__ == "__main__":
    start_game()

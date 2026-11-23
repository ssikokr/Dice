"""Simple Digital Dice Roller Game.

An interactive console game that rolls standard six-sided dice with ASCII
visuals, customizable dice count, and session statistics.
"""

import random

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
}


def render_dice(dice_values):
    """Render multiple dice side-by-side using ASCII art.

    Args:
        dice_values: A list of integers representing the rolled values (1-6).

    Returns:
        A string containing the rendered dice side by side.
    """
    lines = ["", "", "", "", ""]
    for val in dice_values:
        art = DICE_ART.get(val, DICE_ART[1])
        for i in range(5):
            lines[i] += art[i] + "  "
    return "\n".join(lines)


def display_stats(stats):
    """Display overall game statistics."""
    total_rolls = stats["total_rolls"]
    if total_rolls == 0:
        print("\nNo rolls recorded yet!\n")
        return

    print("\n--- Game Statistics ---")
    print(f"Total rolls: {total_rolls}")
    print(f"Total dice rolled: {stats['total_dice']}")
    print(f"Highest single roll total: {stats['highest_total']}")
    avg_total = stats["sum_of_totals"] / total_rolls
    print(f"Average roll total: {avg_total:.2f}")
    print("------------------------\n")


def start_game():
    """Start and run the interactive dice roller game."""
    print("=================================")
    print("   Welcome to the Dice Roller!   ")
    print("=================================")
    print("Roll realistic ASCII dice, track your stats,")
    print("and choose how many dice to roll each turn!\n")

    stats = {
        "total_rolls": 0,
        "total_dice": 0,
        "highest_total": 0,
        "sum_of_totals": 0,
    }
    num_dice = 2  # default to rolling 2 dice

    while True:
        try:
            prompt = (
                f"Press Enter to roll ({num_dice} dice), "
                "1-5 to change count, 's' for stats, 'q' to quit: "
            )
            choice = input(prompt).strip().lower()
        except EOFError:
            # Handle non-interactive execution (e.g. CI workflow or piped input)
            if stats["total_rolls"] == 0:
                print("\n[Non-interactive mode detected: performing demo roll]")
                choice = ""
            else:
                print("\nEnd of input reached. Thanks for playing!")
                break
        except KeyboardInterrupt:
            print("\nGame interrupted. Thanks for playing!")
            break

        if choice == "q":
            print("\nThank you for playing!")
            display_stats(stats)
            break

        if choice == "s":
            display_stats(stats)
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

        # Perform roll
        rolls = [random.randint(1, 6) for _ in range(num_dice)]
        total = sum(rolls)

        stats["total_rolls"] += 1
        stats["total_dice"] += num_dice
        stats["sum_of_totals"] += total
        if total > stats["highest_total"]:
            stats["highest_total"] = total

        print(f"\nRoll #{stats['total_rolls']}:")
        print(render_dice(rolls))
        if num_dice == 1:
            print(f"You got: {rolls[0]}\n")
        else:
            dice_str = " + ".join(str(r) for r in rolls)
            print(f"You got: {dice_str} = {total} (Total: {total})\n")


if __name__ == "__main__":
    start_game()

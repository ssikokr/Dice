"""High Roller Dice - Vegas Casino GUI Application.

# pylint: disable=import-error,global-statement,too-many-statements,too-many-locals,too-many-branches,broad-exception-caught

A tkinter-based dice gambling game featuring single-die rolls, wagering,
power down reductions, checkout win range targets, and double-up streaks.
"""

# --- Imports ---
import os
import random
import tkinter as tk
from tkinter import messagebox

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def play_sound(filename):
    """Play a sound asynchronously if winsound is supported."""
    if not HAS_SOUND:
        return
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)


def load_images():
    """Load and resize dice face images (1 through 7)."""
    images = []
    if not HAS_PIL:
        return images
    for i in range(1, 8):
        for ext in ("png", "jpg", "jpeg", "gif"):
            path = os.path.join(BASE_DIR, f"{i}.{ext}")
            if os.path.exists(path):
                img = Image.open(path).resize((140, 140), Image.LANCZOS)
                images.append(ImageTk.PhotoImage(img))
                break
    return images


# -----------------------------------------------------------------------
# Theme colours
# -----------------------------------------------------------------------
FELT       = "#0d2818"
FELT_LIGHT = "#1a3a2a"
FELT_MID   = "#254d38"
GOLD       = "#d4af37"
GOLD_DARK  = "#a07d1c"
GOLD_LIGHT = "#e8c547"
TEXT_LIGHT = "#f0e6c8"
RED_ACCENT = "#e74c3c"
GREEN_WIN  = "#27ae60"
ORANGE_PWR = "#e67e22"

WAGER_OPTIONS = [1, 5, 10, 25]

# Win range constants
WIN_LOW        = 3    # lower bound never changes
WIN_HIGH_START = 6    # upper bound starts here, shrinks by 1 each Double Up


def main():
    """Initialize and run the High Roller Tkinter application."""
    app = tk.Tk()
    app.title("HIGH ROLLER DICE - Vegas Casino")
    app.geometry("380x750")
    app.resizable(False, False)
    app.configure(bg=FELT)

    dice_images = load_images()

    # Game state
    state = {
        "total": 0,
        "rolled_this_round": False,
        "power_down_streak": 0,
        "current_wager": 5,
        "wager_locked": False,
        "session_wins": 0,
        "session_losses": 0,
        "double_up_mode": False,
        "accumulated_pot": 0,
        "win_high": WIN_HIGH_START,
    }

    wager_buttons = {}

    def set_wager(amount):
        if state["wager_locked"]:
            return
        state["current_wager"] = amount
        wager_label.config(text=f"Selected: ${state['current_wager']}")
        for amt, btn in wager_buttons.items():
            if amt == amount:
                btn.config(relief="sunken", bg=GOLD_LIGHT, fg=FELT)
            else:
                btn.config(relief="raised", bg=FELT_MID, fg=GOLD)

    def lock_wager():
        state["wager_locked"] = True
        for btn in wager_buttons.values():
            btn.config(state="disabled")

    def unlock_wager():
        state["wager_locked"] = False
        for btn in wager_buttons.values():
            btn.config(state="normal")
        set_wager(state["current_wager"])

    def update_scoreboard():
        wins_label.config(text=f"{state['session_wins']}")
        losses_label.config(text=f"{state['session_losses']}")
        pot_label.config(text=f"{state['accumulated_pot']}¢")
        range_label.config(text=f"{WIN_LOW}–{state['win_high']}")
        if state["double_up_mode"]:
            mode_label.config(text="🔥 DOUBLE UP MODE 🔥")
        else:
            mode_label.config(text="")

    def reset_game(full_session=False):
        state["total"] = 0
        state["rolled_this_round"] = False
        state["power_down_streak"] = 0

        if full_session:
            state["win_high"] = WIN_HIGH_START
            state["double_up_mode"] = False
            state["accumulated_pot"] = 0
            state["current_wager"] = 5
            state["session_wins"] = 0
            state["session_losses"] = 0
            update_scoreboard()

        total_label.config(text="Total: 0")
        if dice_images:
            dice_label.config(image=dice_images[0], text="")
        else:
            dice_label.config(text="[ DIE ]")

        roll_btn.config(state="normal")
        checkout_btn.config(state="disabled")
        power_down_btn.config(state="disabled")

        if state["double_up_mode"]:
            wager_label.config(text=f"Selected: ${state['current_wager']}  🔒 DOUBLED")
            result_label.config(
                text=f"🔥 Double Up active! Win range shrunk to {WIN_LOW}–{state['win_high']}\nWager is locked!"
            )
            lock_wager()
        else:
            result_label.config(text="Place your wager & roll")
            unlock_wager()

        update_scoreboard()

    def handle_bust(reason_text):
        checkout_btn.config(state="disabled")
        roll_btn.config(state="disabled")
        power_down_btn.config(state="disabled")
        play_sound("lose.wav")

        lost_amount = state["accumulated_pot"] if state["double_up_mode"] else state["current_wager"]
        state["session_losses"] += 1
        update_scoreboard()

        state["double_up_mode"] = False
        state["accumulated_pot"] = 0
        state["win_high"] = WIN_HIGH_START

        answer = messagebox.askquestion(
            "💀 Bust!",
            f"{reason_text}\nYou lost {lost_amount} coin(s).\nPlay again?",
            icon="warning"
        )
        if answer == "yes":
            reset_game()
        else:
            app.quit()

    def handle_win():
        play_sound("win.wav")
        roll_btn.config(state="disabled")
        checkout_btn.config(state="disabled")
        power_down_btn.config(state="disabled")

        state["session_wins"] += 1
        update_scoreboard()

        payout = state["current_wager"] * 2
        new_pot = state["accumulated_pot"] + payout if state["double_up_mode"] else payout
        can_double = (state["win_high"] - 1) >= WIN_LOW

        if can_double:
            answer = messagebox.askquestion(
                "👑 KING!",
                f"Total is {state['total']} — You're a King!\n\n"
                f"You won {payout} coins.\n\n"
                f"🔥 DOUBLE UP?\n"
                f"  • Carry {payout} coins into the next round\n"
                f"  • Win range narrows to {WIN_LOW}–{state['win_high'] - 1}\n"
                f"  • Win → double your pot again\n"
                f"  • Bust → lose everything\n\n"
                f"Yes = Double Up    No = Cash Out",
            )
            going_double = (answer == "yes")
        else:
            messagebox.showinfo(
                "👑 KING!",
                f"Total is {state['total']} — You're a King!\n\n"
                f"You won {payout} coins.\n\n"
                f"Win range is already at minimum ({WIN_LOW}–{state['win_high']}).\n"
                f"No further Double Up available — cashing out!"
            )
            going_double = False

        if going_double:
            state["double_up_mode"] = True
            state["accumulated_pot"] = new_pot
            state["current_wager"] = payout
            state["win_high"] -= 1
            reset_game()
        else:
            state["double_up_mode"] = False
            state["accumulated_pot"] = 0
            state["win_high"] = WIN_HIGH_START
            reset_game()

    def check_game_state():
        if state["total"] > 20:
            handle_bust(f"Total hit {state['total']} — over 20!")

    def roll_dice():
        if not state["rolled_this_round"]:
            lock_wager()

        max_face = len(dice_images) if dice_images else 6
        number = random.randint(1, max_face)
        state["total"] += number
        state["rolled_this_round"] = True
        state["power_down_streak"] = 0

        play_sound("roll.wav")

        if dice_images and number <= len(dice_images):
            dice_label.config(image=dice_images[number - 1], text="")
        else:
            dice_label.config(text=f"[ {number} ]")

        result_label.config(text=f"You rolled: {number} 🎲")
        total_label.config(text=f"TOTAL: {state['total']}")

        checkout_btn.config(state="normal")
        power_down_btn.config(state="normal")

        check_game_state()

    def power_down():
        state["power_down_streak"] += 1

        if state["power_down_streak"] == 3:
            state["total"] += 20
            play_sound("backfire.wav")
            result_label.config(text="💥 Power Down backfired! +20!")
            total_label.config(text=f"TOTAL: {state['total']}")
            messagebox.showwarning(
                "💥 Backfire!",
                "The Power Down overloaded!\n+20 has been added to your total!"
            )
            state["power_down_streak"] = 0
        else:
            reduction = random.randint(1, 5)
            state["total"] = max(0, state["total"] - reduction)
            play_sound("powerdown.wav")
            result_label.config(text=f"⚡ Power Down! -{reduction}")
            total_label.config(text=f"TOTAL: {state['total']}")

        check_game_state()

    def checkout():
        if not state["rolled_this_round"]:
            return

        if WIN_LOW <= state["total"] <= state["win_high"]:
            handle_win()
        else:
            play_sound("neutral.wav")
            messagebox.showinfo(
                "Not there yet",
                f"Your total is {state['total']}.\nNeed {WIN_LOW}–{state['win_high']} to win."
            )

    # --- Title/Header ---
    header_frame = tk.Frame(app, bg=GOLD, height=60)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame, text="🎰 HIGH ROLLER 🎰", font=("Georgia", 18, "bold"),
        bg=GOLD, fg=FELT
    ).pack(pady=8)

    tk.Label(
        header_frame, text="DICE GAMBLING GAME", font=("Courier", 9),
        bg=GOLD, fg=FELT
    ).pack()

    # --- Scoreboard & Balance ---
    info_frame = tk.Frame(app, bg=FELT_MID, bd=2, relief="ridge")
    info_frame.pack(fill="x", padx=8, pady=8)

    top_row = tk.Frame(info_frame, bg=FELT_MID)
    top_row.pack(fill="x", padx=8, pady=6)

    tk.Label(
        top_row, text="WINS:", font=("Courier", 9, "bold"),
        bg=FELT_MID, fg=GOLD
    ).pack(side="left")

    wins_label = tk.Label(
        top_row, text="0", font=("Courier", 12, "bold"),
        bg=FELT_MID, fg=GREEN_WIN
    )
    wins_label.pack(side="left", padx=8)

    tk.Label(
        top_row, text="LOSSES:", font=("Courier", 9, "bold"),
        bg=FELT_MID, fg=GOLD
    ).pack(side="left", padx=(16, 0))

    losses_label = tk.Label(
        top_row, text="0", font=("Courier", 12, "bold"),
        bg=FELT_MID, fg=RED_ACCENT
    )
    losses_label.pack(side="left", padx=8)

    tk.Label(
        top_row, text="POT:", font=("Courier", 9, "bold"),
        bg=FELT_MID, fg=GOLD
    ).pack(side="right", padx=(0, 8))

    pot_label = tk.Label(
        top_row, text="0¢", font=("Courier", 12, "bold"),
        bg=FELT_MID, fg=GOLD_LIGHT
    )
    pot_label.pack(side="right", padx=8)

    # --- Win Range Display ---
    range_frame = tk.Frame(info_frame, bg=FELT_MID)
    range_frame.pack(fill="x", padx=8, pady=(0, 6))

    tk.Label(
        range_frame, text="WIN RANGE:", font=("Courier", 8, "bold"),
        bg=FELT_MID, fg=GOLD
    ).pack(side="left")

    range_label = tk.Label(
        range_frame, text="3–6", font=("Courier", 11, "bold"),
        bg=FELT_MID, fg=GOLD_LIGHT
    )
    range_label.pack(side="left", padx=6)

    mode_label = tk.Label(
        range_frame, text="", font=("Courier", 8, "bold"),
        bg=FELT_MID, fg=RED_ACCENT
    )
    mode_label.pack(side="right")

    # --- Dice Display ---
    dice_frame = tk.Frame(app, bg=FELT_LIGHT, bd=3, relief="sunken")
    dice_frame.pack(pady=12, padx=8, fill="both")

    init_img = dice_images[0] if dice_images else None
    dice_label = tk.Label(dice_frame, image=init_img, text="" if init_img else "[ DIE ]", bd=0, bg=FELT_LIGHT, font=("Georgia", 16, "bold"), fg=GOLD_LIGHT)
    dice_label.pack(pady=12)

    # --- Status Text ---
    status_frame = tk.Frame(app, bg=FELT_MID, bd=1, relief="groove")
    status_frame.pack(fill="x", padx=8, pady=4)

    result_label = tk.Label(
        status_frame, text="Place your wager & roll",
        font=("Georgia", 10), bg=FELT_MID, fg=TEXT_LIGHT, wraplength=350, justify="center"
    )
    result_label.pack(pady=8, padx=8)

    # --- Total Display ---
    total_frame = tk.Frame(app, bg=FELT_LIGHT, bd=2, relief="ridge")
    total_frame.pack(fill="x", padx=8, pady=6)

    total_label = tk.Label(
        total_frame, text="TOTAL: 0",
        font=("Georgia", 16, "bold"), bg=FELT_LIGHT, fg=GOLD_LIGHT
    )
    total_label.pack(pady=8)

    # --- Wager selector ---
    wager_label_title = tk.Label(
        app, text="SELECT WAGER", font=("Courier", 9, "bold"),
        bg=FELT, fg=GOLD
    )
    wager_label_title.pack(pady=(8, 2))

    wager_frame = tk.Frame(app, bg=FELT)
    wager_frame.pack(pady=4)

    for amt in WAGER_OPTIONS:
        btn = tk.Button(
            wager_frame,
            text=f"${amt}",
            font=("Courier", 11, "bold"),
            width=6, pady=4,
            bg=FELT_MID, fg=GOLD,
            activebackground=GOLD, activeforeground=FELT,
            relief="raised", bd=2,
            command=lambda a=amt: set_wager(a)
        )
        btn.pack(side="left", padx=4)
        wager_buttons[amt] = btn

    wager_label = tk.Label(
        app, text=f"Selected: ${state['current_wager']}",
        font=("Courier", 10, "bold"), bg=FELT, fg=TEXT_LIGHT
    )
    wager_label.pack(pady=(2, 6))

    set_wager(state["current_wager"])

    # --- Action buttons ---
    button_frame = tk.Frame(app, bg=FELT)
    button_frame.pack(fill="x", padx=8, pady=8)

    roll_btn = tk.Button(
        button_frame, text="🎲 ROLL DICE", font=("Georgia", 11, "bold"),
        padx=8, pady=7,
        bg=GOLD, fg=FELT,
        activebackground=GOLD_LIGHT, activeforeground=FELT,
        relief="raised", bd=2,
        command=roll_dice
    )
    roll_btn.pack(fill="x", pady=2)

    action_frame = tk.Frame(button_frame, bg=FELT)
    action_frame.pack(fill="x", pady=2)

    power_down_btn = tk.Button(
        action_frame, text="⚡ POWER DOWN", font=("Georgia", 9, "bold"),
        padx=6, pady=6,
        bg=ORANGE_PWR, fg="white",
        activebackground="#d65a1f", activeforeground="white",
        relief="raised", bd=2,
        state="disabled",
        command=power_down
    )
    power_down_btn.pack(side="left", padx=2, fill="both", expand=True)

    checkout_btn = tk.Button(
        action_frame, text="✅ CHECK OUT", font=("Georgia", 9, "bold"),
        padx=6, pady=6,
        bg=GREEN_WIN, fg="white",
        activebackground="#229954", activeforeground="white",
        relief="raised", bd=2,
        state="disabled",
        command=checkout
    )
    checkout_btn.pack(side="right", padx=2, fill="both", expand=True)

    new_session_btn = tk.Button(
        button_frame, text="🔄 NEW SESSION", font=("Courier", 9, "bold"),
        padx=6, pady=5,
        bg=FELT_MID, fg=GOLD,
        activebackground=FELT_LIGHT, activeforeground=GOLD_LIGHT,
        relief="flat", bd=1,
        command=lambda: reset_game(full_session=True)
    )
    new_session_btn.pack(fill="x", pady=(4, 0))

    app.mainloop()


if __name__ == "__main__":
    main()

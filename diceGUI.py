"""Sleek Desktop GUI for Dice Arcade (Pig & High Roller).

Featuring a minimalist, modern dark aesthetic with smooth tumbling roll
animations, visual progress meters, and smart AI opponent.
"""

# pylint: disable=broad-exception-caught,too-many-instance-attributes,too-many-statements,too-many-lines

import os
import random
import sys
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
    """Play sound asynchronously if supported."""
    if not HAS_SOUND:
        return
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        try:
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Sleek Minimalist Color Palette (Executive Dark Mode)
# ---------------------------------------------------------------------------
BG_DARK = "#0f1117"
CARD_BG = "#181b24"
CARD_BORDER = "#262b3a"
TEXT_PRIMARY = "#f8fafc"
TEXT_MUTED = "#94a3b8"
TEXT_SUBTLE = "#64748b"
BTN_BG = "#222736"
BTN_HOVER = "#2e3449"
BTN_ACTIVE = "#1a1d28"
BTN_PRIMARY = "#31384e"
ACCENT_INDIGO = "#6366f1"
ACCENT_SLATE = "#64748b"
ACCENT_GREEN = "#10b981"
ACCENT_RED = "#ef4444"
TRACK_BG = "#262b3a"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SUBTITLE = ("Segoe UI", 9)
FONT_HEADING = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SCORE = ("Segoe UI", 18, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 10)


def load_dice_images():
    """Load dice face images 1 through 6 resized to 130x130."""
    images = {}
    if not HAS_PIL:
        return images
    for i in range(1, 7):
        path = os.path.join(BASE_DIR, f"{i}.png")
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGBA").resize((130, 130), Image.LANCZOS)
                images[i] = ImageTk.PhotoImage(img)
            except Exception:
                pass
    return images


class DiceArcadeGUI:
    """Main GUI controller for the sleek Dice Arcade."""

    def __init__(self, root):
        self.root = root
        self.root.title("Dice Arcade — Sleek Desktop Edition")
        self.root.geometry("450x740")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)

        self.dice_images = load_dice_images()
        self.is_animating = False
        self.current_mode = "pig"  # "pig" or "high_roller"

        # --- Pig Game State ---
        self.pig_target = 50
        self.pig_vs_bot = True
        self.pig_scores = [0, 0]  # [Player, Bot / P2]
        self.pig_turn = 0         # 0 = Player, 1 = Bot / P2
        self.pig_turn_score = 0
        self.pig_game_over = False

        # --- High Roller State ---
        self.hr_win_low = 3
        self.hr_win_high = 6
        self.hr_bust_limit = 20
        self.hr_total = 0
        self.hr_wager = 5
        self.hr_wager_locked = False
        self.hr_rolled_round = False
        self.hr_power_streak = 0
        self.hr_double_mode = False
        self.hr_pot = 0
        self.hr_wins = 0
        self.hr_losses = 0

        self.setup_ui()
        self.switch_mode("pig")

    def setup_ui(self):
        """Construct the UI layout and widgets."""
        # Top Header & Mode Switcher
        header_frame = tk.Frame(self.root, bg=BG_DARK, pady=12)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="D I C E   A R C A D E",
            font=FONT_TITLE,
            fg=TEXT_PRIMARY,
            bg=BG_DARK,
        ).pack()

        tk.Label(
            header_frame,
            text="Sleek Minimalist Push-Your-Luck & Casino Games",
            font=FONT_SUBTITLE,
            fg=TEXT_MUTED,
            bg=BG_DARK,
        ).pack(pady=(2, 8))

        # Mode Selector Buttons
        mode_btn_frame = tk.Frame(header_frame, bg=CARD_BG, padx=4, pady=4, highlightthickness=1, highlightbackground=CARD_BORDER)
        mode_btn_frame.pack()

        self.pig_tab_btn = tk.Button(
            mode_btn_frame,
            text="🎲  Pig (Push Your Luck)",
            font=FONT_SMALL,
            fg=TEXT_PRIMARY,
            bg=BTN_PRIMARY,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.switch_mode("pig"),
        )
        self.pig_tab_btn.pack(side="left", padx=2)

        self.hr_tab_btn = tk.Button(
            mode_btn_frame,
            text="🎰  High Roller (Casino)",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.switch_mode("high_roller"),
        )
        self.hr_tab_btn.pack(side="left", padx=2)

        # Central Dynamic Container
        self.content_frame = tk.Frame(self.root, bg=BG_DARK, padx=16, pady=4)
        self.content_frame.pack(fill="both", expand=True)

        # Construct sub-frames for both modes
        self.setup_pig_frame()
        self.setup_hr_frame()

    # =========================================================================
    # PIG GAME UI & LOGIC
    # =========================================================================
    def setup_pig_frame(self):
        """Construct the Pig Game interface."""
        self.pig_frame = tk.Frame(self.content_frame, bg=BG_DARK)

        # Mode sub-toggle: Vs Bot / 2-Player
        toggle_row = tk.Frame(self.pig_frame, bg=BG_DARK)
        toggle_row.pack(fill="x", pady=(0, 8))

        self.bot_mode_btn = tk.Button(
            toggle_row,
            text="● Vs Computer Bot",
            font=FONT_SMALL,
            fg=TEXT_PRIMARY,
            bg=BTN_PRIMARY,
            relief="flat",
            padx=10,
            pady=2,
            command=lambda: self.set_pig_opponent(True),
        )
        self.bot_mode_btn.pack(side="left", padx=(0, 4))

        self.p2_mode_btn = tk.Button(
            toggle_row,
            text="○ 2-Player Local",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
            relief="flat",
            padx=10,
            pady=2,
            command=lambda: self.set_pig_opponent(False),
        )
        self.p2_mode_btn.pack(side="left")

        # Scoreboard Card
        score_card = tk.Frame(
            self.pig_frame,
            bg=CARD_BG,
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
        )
        score_card.pack(fill="x", pady=(0, 10))

        # Player 1 row
        p1_header = tk.Frame(score_card, bg=CARD_BG)
        p1_header.pack(fill="x")
        self.p1_label = tk.Label(p1_header, text="Player 1", font=FONT_HEADING, fg=TEXT_PRIMARY, bg=CARD_BG)
        self.p1_label.pack(side="left")
        self.p1_score_val = tk.Label(p1_header, text="0 / 50", font=FONT_SCORE, fg=TEXT_PRIMARY, bg=CARD_BG)
        self.p1_score_val.pack(side="right")

        self.p1_canvas = tk.Canvas(score_card, width=390, height=8, bg=TRACK_BG, highlightthickness=0)
        self.p1_canvas.pack(fill="x", pady=(4, 10))

        # Opponent row
        p2_header = tk.Frame(score_card, bg=CARD_BG)
        p2_header.pack(fill="x")
        self.p2_label = tk.Label(p2_header, text="Computer Bot", font=FONT_HEADING, fg=TEXT_MUTED, bg=CARD_BG)
        self.p2_label.pack(side="left")
        self.p2_score_val = tk.Label(p2_header, text="0 / 50", font=FONT_SCORE, fg=TEXT_MUTED, bg=CARD_BG)
        self.p2_score_val.pack(side="right")

        self.p2_canvas = tk.Canvas(score_card, width=390, height=8, bg=TRACK_BG, highlightthickness=0)
        self.p2_canvas.pack(fill="x", pady=(4, 2))

        # Die Display Area (Clean Frame)
        die_card = tk.Frame(
            self.pig_frame,
            bg=CARD_BG,
            padx=20,
            pady=16,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
        )
        die_card.pack(fill="x", pady=(0, 10))

        self.pig_die_label = tk.Label(die_card, bg=CARD_BG)
        self.pig_die_label.pack()
        self.show_pig_die(1)

        # Status & Turn Info Card
        self.pig_status_label = tk.Label(
            die_card,
            text="Roll to build points, bank to lock them in!",
            font=FONT_BODY,
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            wraplength=380,
        )
        self.pig_status_label.pack(pady=(10, 4))

        self.pig_turn_info = tk.Label(
            die_card,
            text="Turn Points: +0 | Projected Total: 0",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
        )
        self.pig_turn_info.pack()

        # Action Buttons
        action_card = tk.Frame(self.pig_frame, bg=BG_DARK)
        action_card.pack(fill="x", pady=(0, 8))

        btn_row = tk.Frame(action_card, bg=BG_DARK)
        btn_row.pack(fill="x")

        self.pig_roll_btn = tk.Button(
            btn_row,
            text="🎲  ROLL DIE",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_PRIMARY,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            height=2,
            cursor="hand2",
            command=self.on_pig_roll,
        )
        self.pig_roll_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.pig_bank_btn = tk.Button(
            btn_row,
            text="📥  BANK POINTS",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_BG,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            height=2,
            cursor="hand2",
            state="disabled",
            command=self.on_pig_bank,
        )
        self.pig_bank_btn.pack(side="right", fill="x", expand=True, padx=(6, 0))

        # Bottom Bar: Reset Match
        bottom_row = tk.Frame(self.pig_frame, bg=BG_DARK)
        bottom_row.pack(fill="x", pady=(8, 0))

        tk.Button(
            bottom_row,
            text="🔄  Reset Match",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=BG_DARK,
            activebackground=CARD_BG,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            command=self.reset_pig_match,
        ).pack(side="right")

    def show_pig_die(self, value):
        """Render die value either from image or clean fallback."""
        if value in self.dice_images:
            self.pig_die_label.config(image=self.dice_images[value], text="")
        else:
            self.pig_die_label.config(
                text=f"[ {value} ]",
                font=("Segoe UI", 32, "bold"),
                fg=TEXT_PRIMARY,
                image="",
            )

    def draw_progress(self, canvas, current, target=50, color=ACCENT_INDIGO):
        """Draw sleek minimalist rounded progress bar."""
        canvas.delete("all")
        w = canvas.winfo_width()
        if w <= 1:
            w = 390
        h = 8
        ratio = min(1.0, max(0.0, current / target))
        fill_w = int(round(ratio * w))

        # Track background
        canvas.create_rectangle(0, 0, w, h, fill=TRACK_BG, width=0)
        # Fill
        if fill_w > 0:
            canvas.create_rectangle(0, 0, fill_w, h, fill=color, width=0)

    def update_pig_ui(self):
        """Synchronize UI with Pig game state."""
        self.p1_score_val.config(text=f"{self.pig_scores[0]} / {self.pig_target}")
        self.p2_score_val.config(text=f"{self.pig_scores[1]} / {self.pig_target}")

        self.draw_progress(self.p1_canvas, self.pig_scores[0], self.pig_target, ACCENT_INDIGO)
        self.draw_progress(self.p2_canvas, self.pig_scores[1], self.pig_target, ACCENT_SLATE if self.pig_vs_bot else ACCENT_INDIGO)

        active_name = "Player 1" if self.pig_turn == 0 else ("Computer Bot" if self.pig_vs_bot else "Player 2")
        proj = self.pig_scores[self.pig_turn] + self.pig_turn_score

        if self.pig_turn == 0:
            self.p1_label.config(fg=TEXT_PRIMARY, text="● Player 1 (Active)")
            self.p2_label.config(fg=TEXT_MUTED, text="Computer Bot" if self.pig_vs_bot else "Player 2")
        else:
            self.p1_label.config(fg=TEXT_MUTED, text="Player 1")
            self.p2_label.config(
                fg=TEXT_PRIMARY,
                text=f"● {'Computer Bot' if self.pig_vs_bot else 'Player 2'} (Active)",
            )

        self.pig_turn_info.config(
            text=f"Active: {active_name} | Turn Points: +{self.pig_turn_score} | Projected Total: {proj}/{self.pig_target}"
        )

        if self.pig_game_over:
            self.pig_roll_btn.config(state="disabled")
            self.pig_bank_btn.config(state="disabled")
        elif self.pig_vs_bot and self.pig_turn == 1:
            self.pig_roll_btn.config(state="disabled")
            self.pig_bank_btn.config(state="disabled")
        else:
            self.pig_roll_btn.config(state="normal")
            self.pig_bank_btn.config(state="normal" if self.pig_turn_score > 0 else "disabled")

    def set_pig_opponent(self, vs_bot):
        """Switch between Bot AI and 2-Player Local."""
        self.pig_vs_bot = vs_bot
        if vs_bot:
            self.bot_mode_btn.config(fg=TEXT_PRIMARY, bg=BTN_PRIMARY, text="● Vs Computer Bot")
            self.p2_mode_btn.config(fg=TEXT_MUTED, bg=CARD_BG, text="○ 2-Player Local")
            self.p2_label.config(text="Computer Bot")
        else:
            self.bot_mode_btn.config(fg=TEXT_MUTED, bg=CARD_BG, text="○ Vs Computer Bot")
            self.p2_mode_btn.config(fg=TEXT_PRIMARY, bg=BTN_PRIMARY, text="● 2-Player Local")
            self.p2_label.config(text="Player 2")
        self.reset_pig_match()

    def reset_pig_match(self):
        """Reset scores and turn state."""
        self.pig_scores = [0, 0]
        self.pig_turn = 0
        self.pig_turn_score = 0
        self.pig_game_over = False
        self.show_pig_die(1)
        self.pig_status_label.config(
            text="New match started! Roll to build turn points.",
            fg=TEXT_PRIMARY,
        )
        self.update_pig_ui()

    def animate_roll(self, final_value, callback):
        """Run smooth tumbling animation for ~300ms, then invoke callback."""
        if self.is_animating:
            return
        self.is_animating = True
        self.pig_roll_btn.config(state="disabled")
        self.pig_bank_btn.config(state="disabled")
        play_sound("roll.wav")

        frames = 6
        delay = 45

        def step(idx):
            if idx < frames:
                val = random.randint(1, 6)
                self.show_pig_die(val)
                self.root.after(delay, lambda: step(idx + 1))
            else:
                self.show_pig_die(final_value)
                self.is_animating = False
                callback(final_value)

        step(0)

    def on_pig_roll(self):
        """Handle human roll action."""
        if self.pig_game_over or self.is_animating:
            return

        roll_val = random.randint(1, 6)

        def finish_roll(val):
            if val == 1:
                # Pig Out!
                play_sound("lose.wav")
                self.pig_status_label.config(
                    text="💥 PIG OUT! You rolled a 1 — all unbanked points lost!",
                    fg=ACCENT_RED,
                )
                self.pig_turn_score = 0
                self.pig_turn = 1 - self.pig_turn
                self.update_pig_ui()
                if self.pig_vs_bot and self.pig_turn == 1:
                    self.root.after(700, self.run_bot_turn)
            else:
                self.pig_turn_score += val
                proj = self.pig_scores[self.pig_turn] + self.pig_turn_score
                if proj >= self.pig_target:
                    # Player wins!
                    self.pig_scores[self.pig_turn] = proj
                    self.pig_game_over = True
                    play_sound("win.wav")
                    self.pig_status_label.config(
                        text=f"🏆 VICTORY! Player 1 won the match with {proj} points!",
                        fg=ACCENT_GREEN,
                    )
                    self.update_pig_ui()
                else:
                    self.pig_status_label.config(
                        text=f"Rolled a {val}! Roll again or bank your +{self.pig_turn_score} points.",
                        fg=TEXT_PRIMARY,
                    )
                    self.update_pig_ui()

        self.animate_roll(roll_val, finish_roll)

    def on_pig_bank(self):
        """Handle human bank action."""
        if self.pig_game_over or self.pig_turn_score == 0:
            return

        play_sound("neutral.wav")
        self.pig_scores[self.pig_turn] += self.pig_turn_score
        banked = self.pig_turn_score
        self.pig_turn_score = 0

        if self.pig_scores[self.pig_turn] >= self.pig_target:
            self.pig_game_over = True
            play_sound("win.wav")
            self.pig_status_label.config(
                text=f"🏆 VICTORY! Player 1 reached {self.pig_scores[self.pig_turn]} points!",
                fg=ACCENT_GREEN,
            )
            self.update_pig_ui()
            return

        self.pig_status_label.config(
            text=f"💰 Banked {banked} points! Total: {self.pig_scores[self.pig_turn]}/{self.pig_target}.",
            fg=ACCENT_GREEN,
        )
        self.pig_turn = 1 - self.pig_turn
        self.update_pig_ui()

        if self.pig_vs_bot and self.pig_turn == 1:
            self.root.after(700, self.run_bot_turn)

    def run_bot_turn(self):
        """Execute automated Bot AI turn with dynamic pacing."""
        if self.pig_game_over or not self.pig_vs_bot or self.pig_turn != 1:
            return

        # Bot decision: Bank or Roll?
        if (self.pig_scores[1] + self.pig_turn_score >= self.pig_target) or \
           (self.pig_turn_score >= 15) or \
           (self.pig_scores[1] >= 35 and self.pig_turn_score >= 10):
            # Bot banks
            play_sound("neutral.wav")
            self.pig_scores[1] += self.pig_turn_score
            banked = self.pig_turn_score
            self.pig_turn_score = 0

            if self.pig_scores[1] >= self.pig_target:
                self.pig_game_over = True
                play_sound("lose.wav")
                self.pig_status_label.config(
                    text=f"💀 Computer Bot won the match with {self.pig_scores[1]} points!",
                    fg=ACCENT_RED,
                )
                self.update_pig_ui()
                return

            self.pig_status_label.config(
                text=f"💰 Bot banked {banked} points. Total: {self.pig_scores[1]}/{self.pig_target}. Your turn!",
                fg=TEXT_PRIMARY,
            )
            self.pig_turn = 0
            self.update_pig_ui()
            return

        # Bot decides to roll
        self.pig_status_label.config(text="● Bot is rolling...", fg=TEXT_MUTED)
        roll_val = random.randint(1, 6)

        def finish_bot_roll(val):
            if val == 1:
                play_sound("lose.wav")
                self.pig_status_label.config(
                    text="💥 PIG OUT! Bot rolled a 1 — turn points lost. Your turn!",
                    fg=ACCENT_GREEN,
                )
                self.pig_turn_score = 0
                self.pig_turn = 0
                self.update_pig_ui()
            else:
                self.pig_turn_score += val
                proj = self.pig_scores[1] + self.pig_turn_score
                if proj >= self.pig_target:
                    self.pig_scores[1] = proj
                    self.pig_game_over = True
                    play_sound("lose.wav")
                    self.pig_status_label.config(
                        text=f"💀 Computer Bot won with {proj} points!",
                        fg=ACCENT_RED,
                    )
                    self.update_pig_ui()
                else:
                    self.pig_status_label.config(
                        text=f"Bot rolled a {val} (Turn: +{self.pig_turn_score})...",
                        fg=TEXT_MUTED,
                    )
                    self.update_pig_ui()
                    self.root.after(550, self.run_bot_turn)

        self.animate_roll(roll_val, finish_bot_roll)

    # =========================================================================
    # HIGH ROLLER GAME UI & LOGIC
    # =========================================================================
    def setup_hr_frame(self):
        """Construct High Roller Casino interface in matching sleek dark theme."""
        self.hr_frame = tk.Frame(self.content_frame, bg=BG_DARK)

        # Scoreboard Card
        hr_score_card = tk.Frame(
            self.hr_frame,
            bg=CARD_BG,
            padx=14,
            pady=10,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
        )
        hr_score_card.pack(fill="x", pady=(0, 8))

        stats_row = tk.Frame(hr_score_card, bg=CARD_BG)
        stats_row.pack(fill="x")

        self.hr_stats_label = tk.Label(
            stats_row,
            text="Wins: 0  |  Losses: 0  |  Pot: 0 coins",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
        )
        self.hr_stats_label.pack(side="left")

        self.hr_mode_badge = tk.Label(
            stats_row,
            text="",
            font=FONT_SMALL,
            fg=ACCENT_RED,
            bg=CARD_BG,
        )
        self.hr_mode_badge.pack(side="right")

        self.hr_target_label = tk.Label(
            hr_score_card,
            text=f"Target Win Range: {self.hr_win_low}–{self.hr_win_high}  |  Bust Threshold: >{self.hr_bust_limit}",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
        )
        self.hr_target_label.pack(anchor="w", pady=(4, 0))

        # Wager Row
        wager_card = tk.Frame(self.hr_frame, bg=CARD_BG, padx=14, pady=8, highlightthickness=1, highlightbackground=CARD_BORDER)
        wager_card.pack(fill="x", pady=(0, 8))

        tk.Label(wager_card, text="Wager:", font=FONT_SMALL, fg=TEXT_MUTED, bg=CARD_BG).pack(side="left", padx=(0, 8))

        self.wager_btns = {}
        for amt in [1, 5, 10, 25]:
            btn = tk.Button(
                wager_card,
                text=f"${amt}",
                font=FONT_SMALL,
                fg=TEXT_PRIMARY if amt == self.hr_wager else TEXT_MUTED,
                bg=BTN_PRIMARY if amt == self.hr_wager else BTN_BG,
                relief="flat",
                padx=8,
                pady=1,
                cursor="hand2",
                command=lambda a=amt: self.set_hr_wager(a),
            )
            btn.pack(side="left", padx=2)
            self.wager_btns[amt] = btn

        # Die Card
        hr_die_card = tk.Frame(self.hr_frame, bg=CARD_BG, padx=20, pady=12, highlightthickness=1, highlightbackground=CARD_BORDER)
        hr_die_card.pack(fill="x", pady=(0, 8))

        self.hr_die_label = tk.Label(hr_die_card, bg=CARD_BG)
        self.hr_die_label.pack()
        self.show_hr_die(1)

        self.hr_total_label = tk.Label(
            hr_die_card,
            text="Round Total: 0",
            font=FONT_SCORE,
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
        )
        self.hr_total_label.pack(pady=(6, 2))

        self.hr_status_label = tk.Label(
            hr_die_card,
            text="Place wager and roll to begin!",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
            wraplength=380,
        )
        self.hr_status_label.pack()

        # Action Buttons
        hr_actions = tk.Frame(self.hr_frame, bg=BG_DARK)
        hr_actions.pack(fill="x", pady=(0, 6))

        self.hr_roll_btn = tk.Button(
            hr_actions,
            text="🎲  ROLL",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_PRIMARY,
            relief="flat",
            height=2,
            cursor="hand2",
            command=self.on_hr_roll,
        )
        self.hr_roll_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.hr_pwr_btn = tk.Button(
            hr_actions,
            text="⚡  POWER DOWN",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_BG,
            relief="flat",
            height=2,
            cursor="hand2",
            state="disabled",
            command=self.on_hr_power_down,
        )
        self.hr_pwr_btn.pack(side="left", fill="x", expand=True, padx=4)

        self.hr_check_btn = tk.Button(
            hr_actions,
            text="💰  CHECK OUT",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_BG,
            relief="flat",
            height=2,
            cursor="hand2",
            state="disabled",
            command=self.on_hr_checkout,
        )
        self.hr_check_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))

    def show_hr_die(self, val):
        """Display die image in High Roller."""
        if val in self.dice_images:
            self.hr_die_label.config(image=self.dice_images[val], text="")
        else:
            self.hr_die_label.config(text=f"[ {val} ]", font=("Segoe UI", 32, "bold"), fg=TEXT_PRIMARY, image="")

    def set_hr_wager(self, amount):
        """Set active wager if unlocked."""
        if self.hr_wager_locked:
            return
        self.hr_wager = amount
        for amt, btn in self.wager_btns.items():
            if amt == amount:
                btn.config(bg=BTN_PRIMARY, fg=TEXT_PRIMARY)
            else:
                btn.config(bg=BTN_BG, fg=TEXT_MUTED)

    def on_hr_roll(self):
        """Roll in High Roller mode."""
        self.hr_wager_locked = True
        self.hr_rolled_round = True
        self.hr_power_streak = 0
        roll_val = random.randint(1, 6)

        def finish(val):
            self.hr_total += val
            self.hr_total_label.config(text=f"Round Total: {self.hr_total}")
            self.hr_pwr_btn.config(state="normal")

            if self.hr_total > self.hr_bust_limit:
                # Bust
                play_sound("lose.wav")
                lost = self.hr_pot if self.hr_double_mode else self.hr_wager
                self.hr_losses += 1
                self.hr_status_label.config(
                    text=f"💀 BUST! Total reached {self.hr_total} (>20). Lost ${lost}!",
                    fg=ACCENT_RED,
                )
                self.hr_double_mode = False
                self.hr_pot = 0
                self.hr_win_high = 6
                self.reset_hr_round()
                return

            if self.hr_win_low <= self.hr_total <= self.hr_win_high:
                self.hr_check_btn.config(state="normal")
                self.hr_status_label.config(
                    text=f"👑 Inside Win Range ({self.hr_win_low}–{self.hr_win_high})! Check Out to win!",
                    fg=ACCENT_GREEN,
                )
            else:
                self.hr_check_btn.config(state="disabled")
                self.hr_status_label.config(
                    text=f"Total is {self.hr_total}. Target: {self.hr_win_low}–{self.hr_win_high}.",
                    fg=TEXT_PRIMARY,
                )

        self.animate_roll(roll_val, finish)

    def on_hr_power_down(self):
        """Power Down to reduce total."""
        if not self.hr_rolled_round:
            return
        self.hr_power_streak += 1
        if self.hr_power_streak == 3:
            play_sound("backfire.wav")
            self.hr_total += 20
            self.hr_power_streak = 0
            self.hr_total_label.config(text=f"Round Total: {self.hr_total}")
            if self.hr_total > self.hr_bust_limit:
                self.hr_losses += 1
                play_sound("lose.wav")
                self.hr_status_label.config(text="💥 Power Down BACKFIRED! +20 caused a BUST!", fg=ACCENT_RED)
                self.reset_hr_round()
                return
        else:
            play_sound("powerdown.wav")
            reduction = random.randint(1, 5)
            self.hr_total = max(0, self.hr_total - reduction)
            self.hr_total_label.config(text=f"Round Total: {self.hr_total}")
            self.hr_status_label.config(
                text=f"⚡ Power Down: -{reduction} (Streak: {self.hr_power_streak}/3).",
                fg=TEXT_PRIMARY,
            )

        if self.hr_win_low <= self.hr_total <= self.hr_win_high:
            self.hr_check_btn.config(state="normal")
        else:
            self.hr_check_btn.config(state="disabled")

    def on_hr_checkout(self):
        """Handle winning checkout and double up."""
        if not (self.hr_win_low <= self.hr_total <= self.hr_win_high):
            return

        play_sound("win.wav")
        self.hr_wins += 1
        payout = self.hr_wager * 2
        new_pot = self.hr_pot + payout if self.hr_double_mode else payout

        # Offer Double Up
        if (self.hr_win_high - 1) >= self.hr_win_low:
            resp = messagebox.askyesno(
                "👑 WINNER!",
                f"You won {payout} coins! (Total Pot: {new_pot})\n\n"
                f"Double Up for the next round?\n"
                f"• Wager becomes ${payout}\n"
                f"• Win range narrows to {self.hr_win_low}–{self.hr_win_high - 1}\n",
            )
            if resp:
                self.hr_double_mode = True
                self.hr_pot = new_pot
                self.hr_wager = payout
                self.hr_win_high -= 1
                self.hr_mode_badge.config(text="[DOUBLE UP ACTIVE]")
                self.reset_hr_round()
                return

        messagebox.showinfo("💰 Cashed Out", f"Successfully cashed out {new_pot} coins!")
        self.hr_double_mode = False
        self.hr_pot = 0
        self.hr_win_high = 6
        self.hr_mode_badge.config(text="")
        self.reset_hr_round()

    def reset_hr_round(self):
        """Reset state for a new High Roller round."""
        self.hr_total = 0
        self.hr_rolled_round = False
        self.hr_power_streak = 0
        self.hr_total_label.config(text="Round Total: 0")
        self.hr_stats_label.config(
            text=f"Wins: {self.hr_wins}  |  Losses: {self.hr_losses}  |  Pot: {self.hr_pot} coins"
        )
        self.hr_target_label.config(
            text=f"Target Win Range: {self.hr_win_low}–{self.hr_win_high}  |  Bust Threshold: >{self.hr_bust_limit}"
        )
        self.hr_pwr_btn.config(state="disabled")
        self.hr_check_btn.config(state="disabled")
        self.hr_roll_btn.config(state="normal")
        if not self.hr_double_mode:
            self.hr_wager_locked = False
        self.set_hr_wager(self.hr_wager)

    # =========================================================================
    # TAB SWITCHER
    # =========================================================================
    def switch_mode(self, mode):
        """Switch between Pig and High Roller views."""
        self.current_mode = mode
        if mode == "pig":
            self.hr_frame.pack_forget()
            self.pig_frame.pack(fill="both", expand=True)
            self.pig_tab_btn.config(bg=BTN_PRIMARY, fg=TEXT_PRIMARY)
            self.hr_tab_btn.config(bg=CARD_BG, fg=TEXT_MUTED)
            self.update_pig_ui()
        else:
            self.pig_frame.pack_forget()
            self.hr_frame.pack(fill="both", expand=True)
            self.pig_tab_btn.config(bg=CARD_BG, fg=TEXT_MUTED)
            self.hr_tab_btn.config(bg=BTN_PRIMARY, fg=TEXT_PRIMARY)
            self.reset_hr_round()


def main():
    """Application entrypoint."""
    root = tk.Tk()
    DiceArcadeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

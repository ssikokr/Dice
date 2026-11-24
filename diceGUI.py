"""Sleek Desktop GUI for Dice Arcade (Pig & High Roller).

V4 Edition Features:
- 4-Tier Dynamic AI Bot (Cautious, Balanced, Aggressive, Adaptive) with selector.
- Cross-platform audio engine with header Mute/Unmute sound controls.
- Minimalist modern dark aesthetic with smooth tumbling roll animations.
"""

import os
import random
import tkinter as tk
from tkinter import messagebox

from ai_bot import AI_DIFFICULTIES, evaluate_bot_decision, get_difficulty_name
from audio import is_sound_enabled, play_sound, toggle_sound

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
            except (OSError, ValueError):
                pass
    return images


class DiceArcadeGUI:
    """Main GUI controller for the sleek Dice Arcade."""

    def __init__(self, root):
        self.root = root
        self.root.title("Dice Arcade — Sleek Desktop Edition (V4)")
        self.root.geometry("450x770")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)

        self.dice_images = load_dice_images()
        self.is_animating = False
        self.current_mode = "pig"

        self.pig_target = 50
        self.pig_vs_bot = True
        self.ai_difficulty = "adaptive"
        self.pig_scores = [0, 0]
        self.pig_turn = 0
        self.pig_turn_score = 0
        self.pig_game_over = False

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

        self.diff_btns = {}
        self.sound_btn = None
        self.bot_mode_btn = None
        self.p2_mode_btn = None
        self.toggle_row = None
        self.diff_row = None
        self.score_card = None
        self.p1_label = None
        self.p1_score_val = None
        self.p1_canvas = None
        self.p2_label = None
        self.p2_score_val = None
        self.p2_canvas = None
        self.pig_die_label = None
        self.pig_status_label = None
        self.pig_turn_info = None
        self.pig_roll_btn = None
        self.pig_bank_btn = None
        self.pig_frame = None
        self.pig_tab_btn = None
        self.hr_tab_btn = None
        self.content_frame = None

        self.hr_frame = None
        self.hr_stats_label = None
        self.hr_mode_badge = None
        self.hr_target_label = None
        self.wager_btns = {}
        self.hr_die_label = None
        self.hr_total_label = None
        self.hr_status_label = None
        self.hr_roll_btn = None
        self.hr_pwr_btn = None
        self.hr_check_btn = None

        self.setup_ui()
        self.switch_mode("pig")

    def toggle_audio(self):
        """Toggle sound effects on or off and update button text."""
        new_state = toggle_sound()
        self.sound_btn.config(
            text="🔊 Sound: ON" if new_state else "🔇 Sound: OFF",
            fg=TEXT_PRIMARY if new_state else TEXT_MUTED,
        )

    def set_ai_difficulty(self, diff_key):
        """Set active bot AI difficulty and update buttons."""
        self.ai_difficulty = diff_key
        for key, btn in self.diff_btns.items():
            if key == diff_key:
                btn.config(fg=TEXT_PRIMARY, bg=BTN_PRIMARY)
            else:
                btn.config(fg=TEXT_MUTED, bg=CARD_BG)
        self.update_pig_ui()

    def setup_ui(self):
        """Construct the UI layout and widgets."""
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
            text="V4 Edition: Dynamic AI & Cross-Platform Audio",
            font=FONT_SUBTITLE,
            fg=TEXT_MUTED,
            bg=BG_DARK,
        ).pack(pady=(2, 6))

        mode_btn_frame = tk.Frame(
            header_frame,
            bg=CARD_BG,
            padx=4,
            pady=4,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
        )
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

        self.sound_btn = tk.Button(
            header_frame,
            text="🔊 Sound: ON" if is_sound_enabled() else "🔇 Sound: OFF",
            font=FONT_SMALL,
            fg=TEXT_PRIMARY if is_sound_enabled() else TEXT_MUTED,
            bg=CARD_BG,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.toggle_audio,
        )
        self.sound_btn.pack(pady=(6, 0))

        self.content_frame = tk.Frame(self.root, bg=BG_DARK, padx=16, pady=4)
        self.content_frame.pack(fill="both", expand=True)

        self.setup_pig_frame()
        self.setup_hr_frame()

    def setup_pig_frame(self):
        """Construct the Pig Game interface."""
        self.pig_frame = tk.Frame(self.content_frame, bg=BG_DARK)

        self.toggle_row = tk.Frame(self.pig_frame, bg=BG_DARK)
        self.toggle_row.pack(fill="x", pady=(0, 6))

        self.bot_mode_btn = tk.Button(
            self.toggle_row,
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
            self.toggle_row,
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

        self.diff_row = tk.Frame(self.pig_frame, bg=BG_DARK)
        self.diff_row.pack(fill="x", pady=(0, 8))

        tk.Label(
            self.diff_row,
            text="Bot AI:",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=BG_DARK,
        ).pack(side="left", padx=(0, 6))

        for diff_key in ("cautious", "balanced", "aggressive", "adaptive"):
            btn = tk.Button(
                self.diff_row,
                text=AI_DIFFICULTIES[diff_key]["name"],
                font=FONT_SMALL,
                fg=TEXT_PRIMARY if diff_key == self.ai_difficulty else TEXT_MUTED,
                bg=BTN_PRIMARY if diff_key == self.ai_difficulty else CARD_BG,
                activebackground=BTN_HOVER,
                activeforeground=TEXT_PRIMARY,
                relief="flat",
                padx=6,
                pady=1,
                cursor="hand2",
                command=lambda d=diff_key: self.set_ai_difficulty(d),
            )
            btn.pack(side="left", padx=2)
            self.diff_btns[diff_key] = btn

        self.score_card = tk.Frame(
            self.pig_frame,
            bg=CARD_BG,
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
        )
        self.score_card.pack(fill="x", pady=(0, 10))

        p1_header = tk.Frame(self.score_card, bg=CARD_BG)
        p1_header.pack(fill="x")
        self.p1_label = tk.Label(p1_header, text="Player 1", font=FONT_HEADING, fg=TEXT_PRIMARY, bg=CARD_BG)
        self.p1_label.pack(side="left")
        self.p1_score_val = tk.Label(p1_header, text="0 / 50", font=FONT_SCORE, fg=TEXT_PRIMARY, bg=CARD_BG)
        self.p1_score_val.pack(side="right")

        self.p1_canvas = tk.Canvas(self.score_card, width=390, height=8, bg=TRACK_BG, highlightthickness=0)
        self.p1_canvas.pack(fill="x", pady=(4, 10))

        p2_header = tk.Frame(self.score_card, bg=CARD_BG)
        p2_header.pack(fill="x")
        self.p2_label = tk.Label(p2_header, text="Computer Bot", font=FONT_HEADING, fg=TEXT_MUTED, bg=CARD_BG)
        self.p2_label.pack(side="left")
        self.p2_score_val = tk.Label(p2_header, text="0 / 50", font=FONT_SCORE, fg=TEXT_MUTED, bg=CARD_BG)
        self.p2_score_val.pack(side="right")

        self.p2_canvas = tk.Canvas(self.score_card, width=390, height=8, bg=TRACK_BG, highlightthickness=0)
        self.p2_canvas.pack(fill="x", pady=(4, 2))

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
        self.pig_bank_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))

        bottom_row = tk.Frame(self.pig_frame, bg=BG_DARK)
        bottom_row.pack(fill="x", pady=(8, 0))

        tk.Button(
            bottom_row,
            text="🔄  Reset Match",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.reset_pig_match,
        ).pack(side="right")

    def show_pig_die(self, val):
        """Display the corresponding die face image or fallback text."""
        if val in self.dice_images:
            self.pig_die_label.config(image=self.dice_images[val], text="")
        else:
            self.pig_die_label.config(
                text=f"[{val}]",
                font=("Consolas", 48, "bold"),
                fg=TEXT_PRIMARY,
            )

    def draw_progress(self, canvas, current, target, fill_color):
        """Draw an anti-aliased progress bar on a canvas."""
        canvas.delete("all")
        width = canvas.winfo_width()
        if width <= 1:
            width = 390
        height = 8

        canvas.create_rectangle(0, 0, width, height, fill=TRACK_BG, outline="")
        ratio = min(1.0, max(0.0, current / target if target > 0 else 0.0))
        filled_width = int(width * ratio)
        if filled_width > 0:
            canvas.create_rectangle(0, 0, filled_width, height, fill=fill_color, outline="")

    def update_pig_ui(self):
        """Synchronize Pig Game state with UI widgets."""
        self.p1_score_val.config(text=f"{self.pig_scores[0]} / {self.pig_target}")
        self.p2_score_val.config(text=f"{self.pig_scores[1]} / {self.pig_target}")

        self.draw_progress(self.p1_canvas, self.pig_scores[0], self.pig_target, ACCENT_INDIGO)
        self.draw_progress(
            self.p2_canvas,
            self.pig_scores[1],
            self.pig_target,
            ACCENT_SLATE if self.pig_vs_bot else ACCENT_INDIGO,
        )

        bot_title = f"Computer Bot ({get_difficulty_name(self.ai_difficulty)})" if self.pig_vs_bot else "Player 2"
        active_name = "Player 1" if self.pig_turn == 0 else bot_title
        proj = self.pig_scores[self.pig_turn] + self.pig_turn_score

        if self.pig_turn == 0:
            self.p1_label.config(fg=TEXT_PRIMARY, text="● Player 1 (Active)")
            self.p2_label.config(fg=TEXT_MUTED, text=bot_title)
        else:
            self.p1_label.config(fg=TEXT_MUTED, text="Player 1")
            self.p2_label.config(
                fg=TEXT_PRIMARY,
                text=f"● {bot_title} (Active)",
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
            self.diff_row.pack(fill="x", pady=(0, 8), before=self.score_card)
        else:
            self.bot_mode_btn.config(fg=TEXT_MUTED, bg=CARD_BG, text="○ Vs Computer Bot")
            self.p2_mode_btn.config(fg=TEXT_PRIMARY, bg=BTN_PRIMARY, text="● 2-Player Local")
            self.diff_row.pack_forget()
        self.reset_pig_match()

    def reset_pig_match(self):
        """Reset scores and turn state."""
        self.pig_scores = [0, 0]
        self.pig_turn = 0
        self.pig_turn_score = 0
        self.pig_game_over = False
        self.show_pig_die(1)
        self.pig_status_label.config(
            text="New match started! First to 50 points wins.",
            fg=TEXT_PRIMARY,
        )
        self.update_pig_ui()

    def animate_roll(self, final_value, callback):
        """Display an animated tumbling sequence for rolling dice."""
        self.is_animating = True
        self.pig_roll_btn.config(state="disabled")
        self.pig_bank_btn.config(state="disabled")

        play_sound("roll.wav")
        frames = 6
        delays = [50, 60, 70, 80, 90, 110]

        def step(idx):
            if idx < frames:
                val = random.randint(1, 6)
                delay = delays[idx] if idx < len(delays) else 80
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

        bot_name = f"Bot ({get_difficulty_name(self.ai_difficulty)})"

        # Check if bot decides to bank points
        should_bank = evaluate_bot_decision(
            self.ai_difficulty,
            self.pig_turn_score,
            self.pig_scores[1],
            self.pig_scores[0],
            self.pig_target,
        )

        if should_bank and self.pig_turn_score > 0:
            play_sound("neutral.wav")
            self.pig_scores[1] += self.pig_turn_score
            banked = self.pig_turn_score
            self.pig_turn_score = 0

            if self.pig_scores[1] >= self.pig_target:
                self.pig_game_over = True
                play_sound("lose.wav")
                self.pig_status_label.config(
                    text=f"💀 {bot_name} won the match with {self.pig_scores[1]} points!",
                    fg=ACCENT_RED,
                )
                self.update_pig_ui()
                return

            self.pig_status_label.config(
                text=f"💰 {bot_name} banked {banked} points. Total: {self.pig_scores[1]}/{self.pig_target}. Your turn!",
                fg=TEXT_PRIMARY,
            )
            self.pig_turn = 0
            self.update_pig_ui()
            return

        self.pig_status_label.config(text=f"● {bot_name} is rolling...", fg=TEXT_MUTED)
        roll_val = random.randint(1, 6)

        def finish_bot_roll(val):
            if val == 1:
                play_sound("lose.wav")
                self.pig_status_label.config(
                    text=f"💥 PIG OUT! {bot_name} rolled a 1 — turn points lost. Your turn!",
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
                        text=f"💀 {bot_name} won with {proj} points!",
                        fg=ACCENT_RED,
                    )
                    self.update_pig_ui()
                else:
                    self.pig_status_label.config(
                        text=f"{bot_name} rolled a {val} (Turn: +{self.pig_turn_score})...",
                        fg=TEXT_MUTED,
                    )
                    self.update_pig_ui()
                    self.root.after(550, self.run_bot_turn)

        self.animate_roll(roll_val, finish_bot_roll)

    def setup_hr_frame(self):
        """Construct the High Roller Casino interface."""
        self.hr_frame = tk.Frame(self.content_frame, bg=BG_DARK)

        stats_card = tk.Frame(
            self.hr_frame,
            bg=CARD_BG,
            padx=14,
            pady=10,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
        )
        stats_card.pack(fill="x", pady=(0, 10))

        header_row = tk.Frame(stats_card, bg=CARD_BG)
        header_row.pack(fill="x")

        tk.Label(header_row, text="CASINO STANDINGS", font=FONT_HEADING, fg=TEXT_PRIMARY, bg=CARD_BG).pack(side="left")

        self.hr_stats_label = tk.Label(
            header_row,
            text=f"Wins: {self.hr_wins}  |  Losses: {self.hr_losses}  |  Pot: {self.hr_pot} coins",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
        )
        self.hr_stats_label.pack(side="right")

        self.hr_mode_badge = tk.Label(
            stats_card,
            text="SINGLE ROUND BETTING",
            font=FONT_SMALL,
            fg=ACCENT_SLATE,
            bg=CARD_BG,
        )
        self.hr_mode_badge.pack(anchor="w", pady=(2, 4))

        self.hr_target_label = tk.Label(
            stats_card,
            text=f"Target Win Range: {self.hr_win_low}–{self.hr_win_high}  |  Bust Threshold: >{self.hr_bust_limit}",
            font=FONT_SMALL,
            fg=TEXT_MUTED,
            bg=CARD_BG,
        )
        self.hr_target_label.pack(anchor="w")

        wager_row = tk.Frame(self.hr_frame, bg=BG_DARK)
        wager_row.pack(fill="x", pady=(0, 10))

        tk.Label(wager_row, text="Select Wager:", font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DARK).pack(side="left", padx=(0, 8))

        for amt in (1, 5, 10, 25):
            btn = tk.Button(
                wager_row,
                text=f"${amt}",
                font=FONT_SMALL,
                fg=TEXT_PRIMARY if amt == self.hr_wager else TEXT_MUTED,
                bg=BTN_PRIMARY if amt == self.hr_wager else CARD_BG,
                activebackground=BTN_HOVER,
                activeforeground=TEXT_PRIMARY,
                relief="flat",
                padx=10,
                pady=2,
                cursor="hand2",
                command=lambda a=amt: self.set_hr_wager(a),
            )
            btn.pack(side="left", padx=3)
            self.wager_btns[amt] = btn

        hr_die_card = tk.Frame(
            self.hr_frame,
            bg=CARD_BG,
            padx=20,
            pady=16,
            highlightthickness=1,
            highlightbackground=CARD_BORDER,
        )
        hr_die_card.pack(fill="x", pady=(0, 10))

        self.hr_die_label = tk.Label(hr_die_card, bg=CARD_BG)
        self.hr_die_label.pack()
        self.show_hr_die(1)

        self.hr_total_label = tk.Label(
            hr_die_card,
            text="Round Total: [Hidden — track in your head!]",
            font=FONT_BODY,
            fg=TEXT_MUTED,
            bg=CARD_BG,
        )
        self.hr_total_label.pack(pady=(8, 2))

        self.hr_status_label = tk.Label(
            hr_die_card,
            text=f"Place a wager and roll. Build a total between {self.hr_win_low} and {self.hr_win_high}!",
            font=FONT_SMALL,
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
            wraplength=380,
        )
        self.hr_status_label.pack(pady=(2, 6))

        hr_btn_frame = tk.Frame(self.hr_frame, bg=BG_DARK)
        hr_btn_frame.pack(fill="x")

        self.hr_roll_btn = tk.Button(
            hr_btn_frame,
            text="🎲  ROLL DIE",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_PRIMARY,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            height=2,
            cursor="hand2",
            command=self.on_hr_roll,
        )
        self.hr_roll_btn.pack(fill="x", pady=(0, 6))

        sec_btns = tk.Frame(hr_btn_frame, bg=BG_DARK)
        sec_btns.pack(fill="x")

        self.hr_pwr_btn = tk.Button(
            sec_btns,
            text="⚡  POWER DOWN",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_BG,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            height=2,
            cursor="hand2",
            state="disabled",
            command=self.on_hr_power_down,
        )
        self.hr_pwr_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.hr_check_btn = tk.Button(
            sec_btns,
            text="💰  CHECK OUT",
            font=FONT_HEADING,
            fg=TEXT_PRIMARY,
            bg=BTN_BG,
            activebackground=BTN_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            height=2,
            cursor="hand2",
            state="disabled",
            command=self.on_hr_check_out,
        )
        self.hr_check_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))

    def show_hr_die(self, val):
        """Display die face in High Roller view."""
        if val in self.dice_images:
            self.hr_die_label.config(image=self.dice_images[val], text="")
        else:
            self.hr_die_label.config(text=f"[{val}]", font=("Consolas", 48, "bold"), fg=TEXT_PRIMARY)

    def set_hr_wager(self, amt):
        """Set active wager if unlocked."""
        if self.hr_wager_locked or self.hr_double_mode:
            return
        self.hr_wager = amt
        for val, btn in self.wager_btns.items():
            if val == amt:
                btn.config(fg=TEXT_PRIMARY, bg=BTN_PRIMARY)
            else:
                btn.config(fg=TEXT_MUTED, bg=CARD_BG)

    def on_hr_roll(self):
        """Handle single die roll in High Roller."""
        if self.is_animating:
            return

        if not self.hr_rolled_round:
            self.hr_wager_locked = True
            for btn in self.wager_btns.values():
                btn.config(state="disabled")

        self.hr_rolled_round = True
        self.hr_power_streak = 0
        roll_val = random.randint(1, 6)

        def finish_hr_roll(val):
            self.hr_total += val
            self.hr_pwr_btn.config(state="normal")
            self.hr_check_btn.config(state="normal")

            if self.hr_total > self.hr_bust_limit:
                self.handle_hr_bust(f"Exceeded {self.hr_bust_limit}! Final total was {self.hr_total}.")
            else:
                self.hr_status_label.config(
                    text=f"You rolled a {val}. Decide to Roll again, Power Down, or Check Out!",
                    fg=TEXT_PRIMARY,
                )

        self.animate_roll(roll_val, finish_hr_roll)

    def on_hr_power_down(self):
        """Execute Power Down reduction."""
        if not self.hr_rolled_round:
            return

        self.hr_power_streak += 1
        if self.hr_power_streak == 3:
            self.hr_total += 20
            self.hr_power_streak = 0
            play_sound("backfire.wav")
            if self.hr_total > self.hr_bust_limit:
                self.handle_hr_bust(f"Power Down BACKFIRED (+20)! Final total was {self.hr_total}.")
                return
            self.hr_status_label.config(
                text="💥 Power Down BACKFIRED! +20 added to your hidden total!",
                fg=ACCENT_RED,
            )
        else:
            reduction = random.randint(1, 5)
            self.hr_total = max(0, self.hr_total - reduction)
            play_sound("powerdown.wav")
            self.hr_status_label.config(
                text=f"⚡ Power Down: -{reduction} points (Streak: {self.hr_power_streak}/3).",
                fg=ACCENT_INDIGO,
            )

    def on_hr_check_out(self):
        """Attempt to check out active total."""
        if not self.hr_rolled_round:
            return

        if self.hr_win_low <= self.hr_total <= self.hr_win_high:
            self.handle_hr_win()
        else:
            self.handle_hr_bust(f"Check Out Failed! Total was {self.hr_total} (outside {self.hr_win_low}–{self.hr_win_high}).")

    def handle_hr_win(self):
        """Handle winning checkout and Double Up decision."""
        self.hr_wins += 1
        payout = self.hr_wager * 2
        new_pot = self.hr_pot + payout if self.hr_double_mode else payout
        play_sound("win.wav")

        can_double = (self.hr_win_high - 1) >= self.hr_win_low
        going_double = False

        if can_double:
            msg = (
                f"🎉 WINNER! Total was {self.hr_total}!\n"
                f"You earned ${payout}!\n\n"
                f"DOUBLE UP?\n"
                f"• Wager: ${payout}\n"
                f"• Target Range: {self.hr_win_low}–{self.hr_win_high - 1}\n\n"
                "Do you want to Double Up?"
            )
            going_double = messagebox.askyesno("Double Up Opportunity", msg)

        if going_double:
            self.hr_double_mode = True
            self.hr_pot = new_pot
            self.hr_wager = payout
            self.hr_win_high -= 1
            self.hr_status_label.config(
                text=f"🔥 DOUBLE UP ACTIVE! Wager: ${self.hr_wager}, Range: {self.hr_win_low}–{self.hr_win_high}.",
                fg=ACCENT_GREEN,
            )
            self.hr_mode_badge.config(
                text=f"🔥 DOUBLE UP ROUND (POT: ${self.hr_pot})",
                fg=ACCENT_GREEN,
            )
            self.reset_hr_round()
        else:
            self.hr_status_label.config(
                text=f"👑 WINNER! Cashed out ${new_pot}! Round reset.",
                fg=ACCENT_GREEN,
            )
            self.hr_double_mode = False
            self.hr_pot = 0
            self.hr_win_high = 6
            self.hr_mode_badge.config(text="SINGLE ROUND BETTING", fg=ACCENT_SLATE)
            self.reset_hr_round()

    def handle_hr_bust(self, reason):
        """Handle bust outcome."""
        lost = self.hr_pot if self.hr_double_mode else self.hr_wager
        self.hr_losses += 1
        play_sound("lose.wav")

        self.hr_status_label.config(
            text=f"💀 BUST! {reason} Lost ${lost}!",
            fg=ACCENT_RED,
        )
        self.hr_double_mode = False
        self.hr_pot = 0
        self.hr_win_high = 6
        self.hr_mode_badge.config(text="SINGLE ROUND BETTING", fg=ACCENT_SLATE)
        self.reset_hr_round()

    def reset_hr_round(self):
        """Reset single round state."""
        self.hr_total = 0
        self.hr_rolled_round = False
        self.hr_power_streak = 0
        self.hr_total_label.config(text="Round Total: [Hidden]")
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
            for btn in self.wager_btns.values():
                btn.config(state="normal")
        self.set_hr_wager(self.hr_wager)

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

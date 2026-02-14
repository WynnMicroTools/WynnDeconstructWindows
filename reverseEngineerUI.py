import tkinter as tk
from tkinter import ttk, messagebox
import threading
from multiprocessing import freeze_support

try:
    from IngredientDeconstruction import reverse_engineer
except ImportError:
    def reverse_engineer(values, item_type):
        print(f"reverse_engineer called with {values}, {item_type}")
        return None

inv_id_map = {
  "jump height": "jh",
  "stealing": "eSteal",
  "max mana": "maxMana",
  "knock back": "kb",
  "neutral melee damage raw": "nMdRaw",
  "air melee damage raw": "aMdRaw",
  "earth melee damage raw": "eMdRaw",
  "thunder melee damage raw": "tMdRaw",
  "fire melee damage raw": "fMdRaw",
  "water melee damage raw": "wMdRaw",
  "air spell damage raw": "aSdRaw",
  "earth spell damage raw": "eSdRaw",
  "thunder spell damage raw": "tSdRaw",
  "fire spell damage raw": "fSdRaw",
  "water spell damage raw": "wSdRaw",
  "sprint bonus": "sprint",
  "sprint regen bonus": "sprintReg",
  "damage %": "damPct",
  "neutral damage raw": "nDamRaw",
  "exploding": "expd",
  "air spell damage %": "aSdPct",
  "earth spell damage %": "eSdPct",
  "thunder spell damage %": "tSdPct",
  "fire spell damage %": "fSdPct",
  "water spell damage %": "wSdPct",
  "fire damage raw": "fDamRaw",
  "water damage raw": "wDamRaw",
  "thunder damage raw": "tDamRaw",
  "earth damage raw": "eDamRaw",
  "air damage raw": "aDamRaw",
  "raw health regen": "hprRaw",
  "combat xp bonus": "xpb",
  "poison": "poison",
  "life steal": "ls",
  "attack speed bonus": "atkTier",
  "air damage %": "aDamPct",
  "fire damage %": "fDamPct",
  "water damage %": "wDamPct",
  "thunder damage %": "tDamPct",
  "earth damage %": "eDamPct",
  "elemental damage %": "rDamPct",
  "air defense %": "aDefPct",
  "fire defense %": "fDefPct",
  "water defense %": "wDefPct",
  "thunder defense %": "tDefPct",
  "earth defense %": "eDefPct",
  "elemental defense %": "rDefPct",
  "agility": "agi",
  "defense": "def",
  "dexterity": "dex",
  "intelligence": "int",
  "strength": "str",
  "spell damage %": "sdPct",
  "melee damage %": "mdPct",
  "spell damage raw": "sdRaw",
  "melee damage raw": "mdRaw",
  "gathering xp bonus": "gXp",
  "gathering speed bonus": "gSpd",
  "health regen %": "hprPct",
  "mana regen": "mr",
  "mana steal": "ms",
  "thorns": "thorns",
  "reflection": "ref",
  "walk speed bonus": "spd",
  "heal effectiveness %": "healPct",
  "loot bonus": "lb",
  "health bonus": "hpBonus",
  "loot quality": "lq"
}

skill_types = {
    "helmet": "ARMORING",
    "chestplate": "ARMORING",
    "leggings": "TAILORING",
    "boots": "TAILORING",
    "spear": "WEAPONSMITHING",
    "dagger": "WEAPONSMITHING",
    "bow": "WOODWORKING",
    "wand": "WOODWORKING",
    "relik": "WOODWORKING",
    "ring": "JEWELING",
    "bracelet": "JEWELING",
    "necklace": "JEWELING",
    "alchemism": "POTIONS",
    "scroll": "SCRIBING",
    "food": "COOKING"
}

BG = "#1a1a2e"
PANEL = "#16213e"
CARD = "#0f3460"
ACCENT = "#e94560"
ACCENT2 = "#53d8fb"
TEXT = "#eaeaea"
TEXT_DIM = "#8888aa"
ADDED = "#1e3a2f"
ADDED_BORDER = "#2ecc71"
BTN_NORMAL = "#1e2a4a"
BTN_HOVER = "#2a3a6a"
BTN_SELECTED = "#e94560"

FONT_MONO = ("Courier New", 9)
FONT_UI = ("Courier New", 10)
FONT_TITLE = ("Courier New", 13, "bold")
FONT_SMALL = ("Courier New", 8)


class ReverseEngineerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ingredient Reverse Engineer")
        self.geometry("1100x700")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._search_after_id = None

        # State
        self.values = {}          # { stat_label: int_value }
        self.active_stat = None   # currently selected stat button label

        self._build_ui()

    # ------------------------------------------------------------------ #
    #  Layout                                                              #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        # ── top bar ──────────────────────────────────────────────────────
        top = tk.Frame(self, bg=PANEL, pady=8)
        top.pack(fill=tk.X)

        tk.Label(top, text="INGREDIENT REVERSE ENGINEER",
                 font=FONT_TITLE, bg=PANEL, fg=ACCENT).pack(side=tk.LEFT, padx=16)

        # item type
        type_frame = tk.Frame(top, bg=PANEL)
        type_frame.pack(side=tk.RIGHT, padx=16)
        tk.Label(type_frame, text="Item Type:", font=FONT_UI,
                 bg=PANEL, fg=TEXT_DIM).pack(side=tk.LEFT)
        self.item_type_var = tk.StringVar()
        self.item_type_var.set("leggings")
        cb = ttk.Combobox(type_frame, textvariable=self.item_type_var,
                          values=list(skill_types.keys()),
                          state="readonly", width=14, font=FONT_UI)
        cb.pack(side=tk.LEFT, padx=6)
        self._style_combobox(cb)

        # ── main area: left = stat picker, right = active stats ──────────
        main = tk.Frame(self, bg=BG)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        # LEFT – scrollable stat buttons
        left = tk.Frame(main, bg=PANEL, bd=0)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        tk.Label(left, text="SELECT STAT", font=FONT_SMALL,
                 bg=PANEL, fg=TEXT_DIM).pack(anchor="w", padx=8, pady=(6, 2))

        # search box
        search_frame = tk.Frame(left, bg=PANEL)
        search_frame.pack(fill=tk.X, padx=8, pady=(0, 4))
        tk.Label(search_frame, text="🔍", bg=PANEL, fg=TEXT_DIM,
                 font=FONT_UI).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                bg=BTN_NORMAL, fg=TEXT, insertbackground=TEXT,
                                relief=tk.FLAT, font=FONT_UI, bd=4)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # canvas + grid of buttons
        btn_canvas = tk.Canvas(left, bg=PANEL, highlightthickness=0)
        vsb = tk.Scrollbar(left, orient="vertical", command=btn_canvas.yview)
        btn_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        btn_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.btn_inner = tk.Frame(btn_canvas, bg=PANEL)
        self._btn_window = btn_canvas.create_window((0, 0), window=self.btn_inner, anchor="nw")
        self.btn_inner.bind("<Configure>",
                            lambda e: btn_canvas.configure(
                                scrollregion=btn_canvas.bbox("all")))
        btn_canvas.bind("<Configure>",
                        lambda e: btn_canvas.itemconfig(
                            self._btn_window, width=e.width))

        self._stat_buttons = {}      # label -> tk.Button
        self._build_stat_buttons(list(inv_id_map.keys()))

        # mouse-wheel scroll
        btn_canvas.bind_all("<MouseWheel>",
                            lambda e: btn_canvas.yview_scroll(-1*(e.delta//120), "units"))

        # RIGHT – value entry + active stats list
        right = tk.Frame(main, bg=PANEL, width=320)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 0))
        right.pack_propagate(False)

        tk.Label(right, text="ACTIVE STATS", font=FONT_SMALL,
                 bg=PANEL, fg=TEXT_DIM).pack(anchor="w", padx=8, pady=(6, 2))

        # value entry row
        entry_frame = tk.Frame(right, bg=PANEL)
        entry_frame.pack(fill=tk.X, padx=8, pady=4)

        self.selected_label = tk.Label(entry_frame, text="— none selected —",
                                       font=FONT_UI, bg=PANEL, fg=TEXT_DIM,
                                       anchor="w", width=22)
        self.selected_label.pack(side=tk.LEFT)

        self.value_entry = tk.Entry(entry_frame, width=7,
                                    bg=BTN_NORMAL, fg=TEXT,
                                    insertbackground=TEXT,
                                    relief=tk.FLAT, font=FONT_UI, bd=4)
        self.value_entry.pack(side=tk.LEFT, padx=4)
        self.value_entry.bind("<Return>", lambda e: self._set_value())

        tk.Button(entry_frame, text="SET", command=self._set_value,
                  bg=ACCENT, fg="white", relief=tk.FLAT,
                  font=FONT_SMALL, padx=6, cursor="hand2").pack(side=tk.LEFT)

        # active stats list (scrollable)
        list_canvas = tk.Canvas(right, bg=PANEL, highlightthickness=0)
        lvsb = tk.Scrollbar(right, orient="vertical", command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=lvsb.set)
        lvsb.pack(side=tk.RIGHT, fill=tk.Y)
        list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))

        self.list_inner = tk.Frame(list_canvas, bg=PANEL)
        self._list_window = list_canvas.create_window((0, 0), window=self.list_inner, anchor="nw")
        self.list_inner.bind("<Configure>",
                             lambda e: list_canvas.configure(
                                 scrollregion=list_canvas.bbox("all")))
        list_canvas.bind("<Configure>",
                         lambda e: list_canvas.itemconfig(
                             self._list_window, width=e.width))

        # ── bottom bar ────────────────────────────────────────────────────
        bottom = tk.Frame(self, bg=PANEL, pady=8)
        bottom.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(bottom, text="Ready.",
                                     font=FONT_SMALL, bg=PANEL, fg=TEXT_DIM)
        self.status_label.pack(side=tk.LEFT, padx=16)

        tk.Button(bottom, text="CLEAR ALL", command=self._clear_all,
                  bg=BTN_NORMAL, fg=TEXT_DIM, relief=tk.FLAT,
                  font=FONT_UI, padx=12, cursor="hand2").pack(side=tk.RIGHT, padx=8)

        tk.Button(bottom, text="▶  RUN", command=self._run,
                  bg=ACCENT, fg="white", relief=tk.FLAT,
                  font=FONT_TITLE, padx=20, cursor="hand2").pack(side=tk.RIGHT, padx=4)

    # ------------------------------------------------------------------ #
    #  Stat buttons                                                        #
    # ------------------------------------------------------------------ #
    def _build_stat_buttons(self, stats, cols=3):
        # First time: create all buttons once
        if not self._stat_buttons:
            for i, stat in enumerate(inv_id_map.keys()):
                already_added = stat in self.values
                btn = tk.Button(
                    self.btn_inner, text=stat,
                    bg=ADDED if already_added else BTN_NORMAL,
                    fg=ADDED_BORDER if already_added else TEXT,
                    activebackground=BTN_HOVER, activeforeground=TEXT,
                    relief=tk.FLAT, font=FONT_SMALL,
                    padx=4, pady=4, cursor="hand2",
                    command=lambda s=stat: self._select_stat(s)
                )
                self._stat_buttons[stat] = btn

        # Show/hide based on filter, reposition visible ones
        visible = set(stats)
        pos = 0
        for stat, btn in self._stat_buttons.items():
            if stat in visible:
                btn.grid(row=pos // cols, column=pos % cols,
                        padx=3, pady=3, sticky="ew")
                pos += 1
            else:
                btn.grid_remove()  # hide but don't destroy

        for c in range(cols):
            self.btn_inner.columnconfigure(c, weight=1)

        self._refresh_buttons()
    def _on_search(self, *_):
        # term = self.search_var.get().lower()
        # filtered = [s for s in inv_id_map.keys() if term in s.lower()]
        # self._build_stat_buttons(filtered)
        if self._search_after_id is not None:
            self.after_cancel(self._search_after_id)
        
        # Schedule new search after 300ms of no typing
        self._search_after_id = self.after(300, self._do_search)
    def _do_search(self):
        self._search_after_id = None
        term = self.search_var.get().lower()
        filtered = [s for s in inv_id_map.keys() if term in s.lower()]
        self._build_stat_buttons(filtered)
    # ------------------------------------------------------------------ #
    #  Interactions                                                        #
    # ------------------------------------------------------------------ #
    def _select_stat(self, stat):
        self.active_stat = stat
        self.selected_label.configure(text=stat, fg=TEXT)
        # pre-fill entry with existing value if set
        self.value_entry.delete(0, tk.END)
        if stat in self.values:
            self.value_entry.insert(0, str(self.values[stat]))
        self.value_entry.focus_set()
        # refresh button colours
        self._refresh_buttons()

    def _set_value(self):
        if not self.active_stat:
            messagebox.showwarning("No stat selected", "Click a stat first.")
            return
        raw = self.value_entry.get().strip()
        if not raw:
            messagebox.showwarning("Empty value", "Enter a number.")
            return
        try:
            val = int(raw)
        except ValueError:
            messagebox.showerror("Invalid", "Value must be an integer.")
            return

        self.values[self.active_stat] = val
        self._refresh_buttons()
        self._refresh_active_list()
        self.status_label.configure(
            text=f"Set  {self.active_stat}  →  {val}", fg=ACCENT2)

    def _remove_stat(self, stat):
        self.values.pop(stat, None)
        if self.active_stat == stat:
            self.active_stat = None
            self.selected_label.configure(text="— none selected —", fg=TEXT_DIM)
            self.value_entry.delete(0, tk.END)
        self._refresh_buttons()
        self._refresh_active_list()

    def _clear_all(self):
        self.values.clear()
        self.active_stat = None
        self.selected_label.configure(text="— none selected —", fg=TEXT_DIM)
        self.value_entry.delete(0, tk.END)
        self._refresh_buttons()
        self._refresh_active_list()

    # ------------------------------------------------------------------ #
    #  Refresh helpers                                                     #
    # ------------------------------------------------------------------ #
    def _refresh_buttons(self):
        for stat, btn in self._stat_buttons.items():
            if stat == self.active_stat:
                btn.configure(bg=BTN_SELECTED, fg="white")
            elif stat in self.values:
                btn.configure(bg=ADDED, fg=ADDED_BORDER)
            else:
                btn.configure(bg=BTN_NORMAL, fg=TEXT)

    def _refresh_active_list(self):
        for w in self.list_inner.winfo_children():
            w.destroy()

        if not self.values:
            tk.Label(self.list_inner, text="No stats added yet.",
                     font=FONT_SMALL, bg=PANEL, fg=TEXT_DIM).pack(anchor="w", padx=4)
            return

        for stat, val in self.values.items():
            row = tk.Frame(self.list_inner, bg=ADDED, pady=2)
            row.pack(fill=tk.X, padx=2, pady=2)

            # coloured left border
            tk.Frame(row, bg=ADDED_BORDER, width=3).pack(side=tk.LEFT, fill=tk.Y)

            tk.Label(row, text=stat, font=FONT_UI,
                     bg=ADDED, fg=TEXT, anchor="w").pack(side=tk.LEFT, padx=6, expand=True, fill=tk.X)

            val_color = ACCENT if val < 0 else ACCENT2
            tk.Label(row, text=str(val), font=("Courier New", 10, "bold"),
                     bg=ADDED, fg=val_color, width=7, anchor="e").pack(side=tk.LEFT, padx=4)

            tk.Button(row, text="✕", command=lambda s=stat: self._remove_stat(s),
                      bg=ADDED, fg=ACCENT, relief=tk.FLAT,
                      font=FONT_SMALL, cursor="hand2", padx=4).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------ #
    #  Run                                                                 #
    # ------------------------------------------------------------------ #
    def _run(self):
        if not self.item_type_var.get():
            messagebox.showwarning("Missing", "Select an item type.")
            return
        if not self.values:
            messagebox.showwarning("Missing", "Add at least one stat.")
            return

        # convert display labels to id keys
        mapped = {inv_id_map[k]: v for k, v in self.values.items()}

        self.status_label.configure(text="Running… please wait.", fg=ACCENT)
        self.update_idletasks()

        def worker():
            try:
                result = reverse_engineer(mapped, self.item_type_var.get())
                self.after(0, lambda: self._show_result(result))
            except Exception as exc:
                self.after(0, lambda: self._show_error(str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _show_result(self, result):
        self.status_label.configure(text="Done!", fg=ADDED_BORDER)
        win = tk.Toplevel(self)
        win.title("Result")
        win.configure(bg=BG)
        win.geometry("500x300")
        tk.Label(win, text="RESULT", font=FONT_TITLE,
                 bg=BG, fg=ACCENT).pack(pady=10)
        txt = tk.Text(win, bg=PANEL, fg=TEXT, font=FONT_MONO,
                      relief=tk.FLAT, padx=10, pady=10)
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        txt.insert(tk.END, str(result) if result is not None else "No solution found.")
        txt.configure(state=tk.DISABLED)

    def _show_error(self, msg):
        self.status_label.configure(text="Error.", fg=ACCENT)
        messagebox.showerror("Error", msg)

    # ------------------------------------------------------------------ #
    #  Misc                                                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _style_combobox(cb):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=BTN_NORMAL,
                        background=BTN_NORMAL,
                        foreground=TEXT,
                        selectbackground=CARD,
                        selectforeground=TEXT)


if __name__ == "__main__":
    freeze_support()
    ReverseEngineerUI().mainloop()
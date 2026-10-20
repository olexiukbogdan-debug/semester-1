"""Tkinter interface for the alchemist RPG."""

import tkinter as tk
from tkinter import messagebox, ttk

from game import Game
from potions import POTIONS, POTIONS_BY_NUMBER


class AlchemistWindow:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.root.title("Алхімік — шлях до королівського двору")
        self.root.geometry("1050x720")
        self.root.minsize(850, 600)
        self.root.configure(bg="#17221d")

        self._configure_style()
        self._build_window()
        self._log(
            f"Твоя мета — заробити {self.game.WINNING_GOLD} золотих "
            f"за {self.game.MAX_DAYS} днів."
        )
        self._log_daily_reward()
        self._refresh()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#f5f0df",
            fieldbackground="#f5f0df",
            foreground="#25352c",
            rowheight=25,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#d5b778",
            foreground="#24352b",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=7,
        )
        style.configure("TNotebook.Tab", padding=(12, 7), font=("Segoe UI", 10))

    def _build_window(self):
        header = tk.Frame(self.root, bg="#263b30", padx=18, pady=14)
        header.pack(fill="x")
        tk.Label(
            header,
            text="⚗  АЛХІМІК",
            bg="#263b30",
            fg="#f2d68d",
            font=("Segoe UI", 22, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text="Звари зілля. Здобудь прихильність короля.",
            bg="#263b30",
            fg="#eceddf",
            font=("Segoe UI", 11),
        ).pack(side="left", padx=20, pady=(5, 0))

        self.status_label = tk.Label(
            self.root,
            bg="#e7dfc7",
            fg="#263b30",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
            padx=18,
            pady=10,
        )
        self.status_label.pack(fill="x")

        body = tk.Frame(self.root, bg="#17221d", padx=14, pady=12)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        left = tk.Frame(body, bg="#17221d")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        right = tk.Frame(body, bg="#17221d")
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self._build_catalog(left)
        self._build_inventory(right)
        self._build_actions(body)
        self._build_journal(body)

    def _build_catalog(self, parent):
        tk.Label(
            parent,
            text="Книга рецептів",
            bg="#17221d",
            fg="#f2d68d",
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 7))

        frame = tk.Frame(parent, bg="#17221d")
        frame.pack(fill="both", expand=True)
        columns = ("name", "recipe", "price")
        self.catalog = ttk.Treeview(frame, columns=columns, show="headings")
        self.catalog.heading("name", text="Зілля")
        self.catalog.heading("recipe", text="Інгредієнти (будь-які 2 з 4)")
        self.catalog.heading("price", text="Ціна")
        self.catalog.column("name", width=165, stretch=True)
        self.catalog.column("recipe", width=285, stretch=True)
        self.catalog.column("price", width=70, anchor="center", stretch=False)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.catalog.yview)
        self.catalog.configure(yscrollcommand=scrollbar.set)
        self.catalog.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for potion in POTIONS:
            recipe = ", ".join(potion.ingredients)
            self.catalog.insert(
                "",
                "end",
                iid=str(potion.number),
                values=(potion.name, recipe, f"{potion.price} зол."),
            )
        self.catalog.bind("<<TreeviewSelect>>", self._select_catalog_potion)

        controls = tk.Frame(parent, bg="#17221d", pady=9)
        controls.pack(fill="x")
        tk.Label(
            controls,
            text="Кількість:",
            bg="#17221d",
            fg="#eceddf",
        ).pack(side="left")
        self.craft_amount = tk.StringVar(value="1")
        self.craft_amount_box = ttk.Spinbox(
            controls, from_=1, to=100, width=5, textvariable=self.craft_amount
        )
        self.craft_amount_box.pack(side="left", padx=7)
        self.craft_button = ttk.Button(
            controls, text="Зварити зілля", command=self._craft_selected
        )
        self.craft_button.pack(side="left")

    def _build_inventory(self, parent):
        tk.Label(
            parent,
            text="Інвентар",
            bg="#17221d",
            fg="#f2d68d",
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 7))

        self.ingredient_heading = tk.Label(
            parent, bg="#17221d", fg="#eceddf", anchor="w"
        )
        self.ingredient_heading.pack(fill="x")
        self.ingredient_tree = self._make_inventory_tree(
            parent, ("name", "count"), ("Інгредієнт", "К-сть"), (270, 70)
        )

        self.potion_heading = tk.Label(
            parent, bg="#17221d", fg="#eceddf", anchor="w"
        )
        self.potion_heading.pack(fill="x", pady=(10, 0))
        self.potion_tree = self._make_inventory_tree(
            parent, ("name", "count"), ("Зілля", "К-сть"), (270, 70)
        )

        self.sell_button = ttk.Button(
            parent, text="Продати всі зілля", command=self._sell_all
        )
        self.sell_button.pack(fill="x", pady=(8, 0))

    @staticmethod
    def _make_inventory_tree(parent, columns, headings, widths):
        frame = tk.Frame(parent, bg="#17221d")
        frame.pack(fill="both", expand=True, pady=(3, 0))
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=7)
        for column, heading, width in zip(columns, headings, widths):
            tree.heading(column, text=heading)
            tree.column(column, width=width, anchor="w")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def _build_actions(self, parent):
        frame = tk.Frame(parent, bg="#263b30", padx=12, pady=9)
        frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(9, 8))
        self.end_day_button = ttk.Button(
            frame, text="Завершити день →", command=self._finish_day
        )
        self.end_day_button.pack(side="right")
        tk.Label(
            frame,
            text="На початку кожного дня ти отримуєш до 5 нових інгредієнтів.",
            bg="#263b30",
            fg="#eceddf",
            font=("Segoe UI", 10),
        ).pack(side="left")

    def _build_journal(self, parent):
        tk.Label(
            parent,
            text="Події",
            bg="#17221d",
            fg="#f2d68d",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).grid(row=2, column=0, columnspan=2, sticky="ew")
        self.journal = tk.Text(
            parent,
            height=5,
            bg="#f5f0df",
            fg="#25352c",
            font=("Segoe UI", 10),
            wrap="word",
            state="disabled",
        )
        self.journal.grid(row=3, column=0, columnspan=2, sticky="ew")

    def _log(self, message):
        self.journal.configure(state="normal")
        self.journal.insert("end", f"• {message}\n")
        self.journal.see("end")
        self.journal.configure(state="disabled")

    def _log_daily_reward(self):
        received = self.game.daily_ingredients
        self._log(
            f"День {self.game.day}: отримано інгредієнтів "
            f"{len(received)}/{self.game.DAILY_INGREDIENTS}."
        )
        for ingredient in received:
            self._log(f"  + {ingredient}")
        if len(received) < self.game.DAILY_INGREDIENTS:
            self._log("Інвентар заповнений — частину інгредієнтів не отримано.")

    def _selected_potion_number(self):
        selection = self.catalog.selection()
        if not selection:
            return None
        try:
            return int(selection[0])
        except ValueError:
            self._log("Не вдалося визначити зілля з вибору.")
            return None

    def _select_catalog_potion(self, event):
        selection = event.widget.selection()
        if not selection:
            return
        try:
            number = int(selection[0])
        except ValueError:
            self._log("Не вдалося визначити зілля з вибору.")
            return
        potion = POTIONS_BY_NUMBER.get(number)
        if potion is not None:
            self._log(
                f"Вибрано «{potion.name}». Для варіння потрібні будь-які "
                "2 з 4 інгредієнтів рецепта."
            )

    def _craft_selected(self):
        try:
            number = self._selected_potion_number()
            if number is None:
                messagebox.showinfo("Рецепт не вибрано", "Вибери зілля в книзі рецептів.")
                return
            amount = int(self.craft_amount.get())
            if amount <= 0:
                raise ValueError("Кількість має бути більшою за нуль.")
        except (ValueError, tk.TclError) as error:
            messagebox.showerror("Некоректна кількість", str(error))
            return

        crafted = self.game.craft_potion(number, amount)
        potion = POTIONS_BY_NUMBER[number]
        if crafted:
            self._log(f"Зварено «{potion.name}»: {crafted} шт.")
        else:
            self._log(
                "Не вистачає потрібних інгредієнтів, місця або місткості "
                "стаку зіль."
            )
        self._refresh()

    def _sell_all(self):
        if not self.game.inventory.potions:
            self._log("Немає зіль для продажу.")
            return
        sold, earned = self.game.sell_potions()
        self._log(f"Продано зіль: {sold}. Отримано {earned} золотих.")
        self._refresh()
        self._show_ending()

    def _finish_day(self):
        self.game.finish_day()
        if self.game.won or self.game.lost:
            self._refresh()
            self._show_ending()
            return
        self._log_daily_reward()
        self._refresh()

    def _refresh(self):
        inventory = self.game.inventory
        self.status_label.configure(
            text=(
                f"День {self.game.day}/{self.game.MAX_DAYS}     "
                f"Золото: {self.game.gold}/{self.game.WINNING_GOLD}"
            )
        )
        self.ingredient_heading.configure(
            text=(
                f"Інгредієнти — {len(inventory.ingredients)}/"
                f"{inventory.INGREDIENT_SLOT_LIMIT} слотів"
            )
        )
        self.potion_heading.configure(
            text=(
                f"Зілля — {len(inventory.potions)}/"
                f"{inventory.POTION_SLOT_LIMIT} слотів"
            )
        )
        self._replace_tree(
            self.ingredient_tree,
            (
                (name, f"{count}/{inventory.INGREDIENT_STACK_LIMIT}")
                for name, count in sorted(inventory.ingredients.items())
            ),
        )
        self._replace_tree(
            self.potion_tree,
            (
                (name, f"{count}/{inventory.POTION_STACK_LIMIT}")
                for name, count in sorted(inventory.potions.items())
            ),
        )
        if self.game.won or self.game.lost:
            self.craft_button.configure(state="disabled")
            self.end_day_button.configure(state="disabled")
            self.sell_button.configure(state="disabled")

    @staticmethod
    def _replace_tree(tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", "end", values=row)

    def _show_ending(self):
        if self.game.won:
            messagebox.showinfo(
                "Перемога!",
                f"Ти зібрав {self.game.gold} золотих і став королівським алхіміком!",
            )
            self._log("Перемога! Королівський двір запросив тебе на службу.")
        elif self.game.lost:
            messagebox.showinfo(
                "Гру завершено",
                f"За {self.game.MAX_DAYS} днів зібрано {self.game.gold} із "
                f"{self.game.WINNING_GOLD} золотих. Король найняв іншого алхіміка.",
            )
            self._log("Поразка: потрібна сума не зібрана вчасно.")


def launch_game():
    try:
        root = tk.Tk()
    except tk.TclError as error:
        raise RuntimeError(
            "Не вдалося відкрити графічне вікно. Переконайся, що Python "
            "встановлений із підтримкою Tkinter."
        ) from error
    AlchemistWindow(root)
    root.mainloop()

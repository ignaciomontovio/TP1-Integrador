import tkinter as tk
from tkinter import ttk


class Theme:
    BG = "#F1FAEE"
    FG = "#1D3557"
    RED = "#E63946"
    BG_LIGHT = "#A8DADC"
    BORDER_BG = "#1D3557"
    BORDER_BG_N = "#E63946"
    BORDER_BG_A = "#457B9D"
    BORDER_BG_P = "#1D3557"
    TEXT_SELECTED_BG = "#457B9D"

    def style(app: tk.Tk, font_name: str = "TkDefaultFont"):
        app.style = ttk.Style(app)
        app.style.configure("Main.TFrame", background=Theme.BORDER_BG)
        app.style.configure("Light.TFrame", background=Theme.BG_LIGHT)
        app.style.configure("Sub.TFrame", background=Theme.BG)

        app.style.configure(
            "TLabelframe", background=Theme.BG_LIGHT, borderwidth=3, relief=tk.GROOVE
        )
        app.style.configure(
            "TLabelframe.Label",
            background=Theme.BG_LIGHT,
            foreground=Theme.FG,
            font=(font_name, 14, "bold"),
        )

        app.style.configure(
            "TLabel",
            background=Theme.BG_LIGHT,
            foreground=Theme.FG,
            font=(font_name, 12),
        )

        app.style.configure(
            "TButton",
            font=(font_name, 14),
            background=Theme.BORDER_BG_N,
            foreground=Theme.BG,
        )
        app.style.map(
            "TButton",
            background=[
                ("pressed", Theme.BORDER_BG_P),
                ("active", Theme.BG),
                ("disabled", Theme.BORDER_BG_P),
            ],
            foreground=[("active", Theme.BORDER_BG_P)],
        )

        app.style.configure(
            "Sub.TButton",
            font=(font_name, 14),
            background=Theme.BORDER_BG_A,
            foreground=Theme.BG,
        )
        app.style.map(
            "Sub.TButton",
            background=[
                ("pressed", Theme.BORDER_BG_P),
                ("active", Theme.BG),
                ("disabled", Theme.BORDER_BG_P),
            ],
            foreground=[("active", Theme.BORDER_BG_P)],
        )

        app.style.configure(
            "TEntry",
            foreground=Theme.FG,
            insertcolor=Theme.RED,
            fieldbackground=Theme.BG,
            selectbackground=Theme.TEXT_SELECTED_BG,
            selectforeground=Theme.BG,
        )

        app.style.configure(
            "TCombobox",
            foreground=Theme.FG,
            insertcolor=Theme.RED,
            fieldbackground=Theme.BG,
            selectbackground=Theme.TEXT_SELECTED_BG,
            selectforeground=Theme.BG,
            background=Theme.BG_LIGHT,
            arrowcolor=Theme.TEXT_SELECTED_BG,
            arrowsize=15,
        )

        app.style.configure(
            "TSpinbox",
            foreground=Theme.FG,
            insertcolor=Theme.RED,
            fieldbackground=Theme.BG,
            selectbackground=Theme.TEXT_SELECTED_BG,
            selectforeground=Theme.BG,
            background=Theme.BG_LIGHT,
            arrowcolor=Theme.TEXT_SELECTED_BG,
            arrowsize=15,
        )

        app.option_add("*TCombobox*Listbox.background", Theme.BG)
        app.option_add("*TCombobox*Listbox.foreground", Theme.FG)
        app.option_add("*TCombobox*Listbox.selectBackground", Theme.TEXT_SELECTED_BG)
        app.option_add("*TCombobox*Listbox.selectForeground", Theme.BG)
        app.option_add("*TCombobox*Listbox.font", (font_name, 14))

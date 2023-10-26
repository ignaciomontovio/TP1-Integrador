import tkinter as tk
from tkinter import ttk


class Theme:
    BG = "#F1FAEE"
    FG = "#1D3557"
    RED = "#E63946"
    BORDER_BG = "#1D3557"
    BORDER_BG_N = "#E63946"
    BORDER_BG_A = "#457B9D"
    BORDER_BG_P = "#1D3557"
    TEXT_SELECTED_BG = "#457B9D"

    def style(app: tk.Tk, font_name: str = "TkDefaultFont"):
        app.style = ttk.Style(app)
        app.style.configure("Main.TFrame", background=Theme.BORDER_BG)
        app.style.configure("Sub.TFrame", background=Theme.BG)
        app.style.configure("TLabelframe", background="#A8DADC", relief="flat")
        app.style.configure(
            "TLabelframe.Label",
            background="#A8DADC",
            foreground=Theme.FG,
            font=(font_name, 14),
        )
        app.style.configure(
            "TLabel",
            background="#A8DADC",
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
                ("active", Theme.BORDER_BG_A),
                ("disabled", Theme.BORDER_BG_P),
            ],
        )
        app.style.configure(
            "TText",
            background=Theme.BG,
            selectbackground=Theme.TEXT_SELECTED_BG,
            foreground=Theme.FG,
            selectforeground=Theme.BG,
            insertbackground=Theme.RED,
            wrap="word",
            spacing2=3,
        )

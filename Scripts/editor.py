import tkinter as tk
from tkinter import ttk
from config import *

class BetterPaint:
    def __init__(self, window):
        self.root = window
        self.root.geometry("1400x750")
        self.root.title("Better Paint")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, bg="white", width=1300, height=750)
        self.canvas.pack(side="right")

        self.bind()
        self.last_x = self.last_y = None
        self.is_drawing = False
        self.brush_size = Width.LIGHT.value
        self.brush_color = Color.BLACK

        self.tool_frame = tk.Frame(self.root, width=100, bg='lightgray')
        self.tool_frame.pack(side="left", fill="y")
        self.tool_frame.pack_propagate(False)

        self.create_tool_frame()

    def bind(self):
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def drawing(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            if self.last_x and self.last_y:
                self.canvas.create_line(
                    self.last_x, self.last_y,
                    x, y,
                    fill=self.brush_color,
                    width=self.brush_size,
                    capstyle="round",
                    smooth=True,
                    splinesteps=36
                )
            self.last_x, self.last_y = x, y

    def start_drawing(self, event):
        self.is_drawing = True
        self.last_x, self.last_y = event.x, event.y

    def stop_drawing(self, event):
        self.is_drawing = False
        self.last_x, self.last_y = None, None

    def change_brush_size(self, new_size):
        self.brush_size = new_size

    def change_brush_color(self, new_color):
        self.brush_color = new_color
        self.color_indicator.config(bg=new_color)

    def create_tool_frame(self):
        colors = [
            Color.BLACK,
            Color.DIM_GRAY,
            Color.SLATE_GRAY,
            Color.LIGHT_SLATE_GRAY,
            Color.GAINSBORO,
            Color.WHITE,
            Color.DARK_RED,
            Color.CRIMSON,
            Color.FIREBRICK,
            Color.INDIAN_RED,
            Color.SADDLE_BROWN,
            Color.SIENNA,
            Color.CHOCOLATE,
            Color.PERU,
            Color.DARK_GOLDENROD,
            Color.GOLDENROD,
            Color.GOLD,
            Color.YELLOW,
            Color.DARK_GREEN,
            Color.FOREST_GREEN,
            Color.SEA_GREEN,
            Color.LIME_GREEN,
            Color.TEAL,
            Color.LIGHT_SEA_GREEN,
            Color.DEEP_SKY_BLUE,
            Color.DODGER_BLUE,
            Color.ROYAL_BLUE,
            Color.DARK_BLUE,
            Color.NAVY,
            Color.BLUE_VIOLET
        ]

        tk.Label(self.tool_frame, text="Current color:", bg='lightgray').pack(pady=5)

        self.color_indicator = tk.Label(
            self.tool_frame,
            width=4,
            height=2,
            bg=self.brush_color,
            relief='sunken',
            bd=2
        )
        self.color_indicator.pack(pady=2)

        palette_frame = tk.Frame(self.tool_frame, bg='lightgray')
        palette_frame.pack(pady=15)

        left_frame = tk.Frame(palette_frame, bg='lightgray')
        left_frame.pack(side="left", padx=3)

        right_frame = tk.Frame(palette_frame, bg='lightgray')
        right_frame.pack(side="left", padx=3)

        for i, color_enum in enumerate(colors):
            if i < 15:
                frame = left_frame
            else:
                frame = right_frame

            lbl = tk.Label(
                frame,
                width=4,
                height=2,
                bg=color_enum.value,
                relief='raised',
                bd=1,
                cursor='hand2'
            )

            lbl.pack(pady=1)
            lbl.bind("<Button-1>",
                     lambda e, c=color_enum.value: self.change_brush_color(c))

            lbl.bind("<Enter>", lambda e, l=lbl: l.config(relief='sunken'))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(relief='raised'))

        tk.Label(self.tool_frame, text="Brush Size:", bg='lightgray').pack(pady=(15, 0))

        self.brush_size_var = tk.StringVar()
        current_size = Width.LIGHT.value
        self.brush_size_var.set(f"{current_size} px (Light)")

        size_options = [
            f"{Width.THIN.value} px (Thin)",
            f"{Width.FINE.value} px (Fine)",
            f"{Width.LIGHT.value} px (Light)",
            f"{Width.MEDIUM.value} px (Medium)",
            f"{Width.BOLD.value} px (Bold)",
            f"{Width.THICK.value} px (Thick)",
            f"{Width.HEAVY.value} px (Heavy)",
            f"{Width.FAT.value} px (Fat)",
            f"{Width.MARKER.value} px (Marker)",
            f"{Width.BRUSH.value} px (Brush)",
            f"{Width.SPRAY.value} px (Spray)",
            f"{Width.BLOCK.value} px (Block)"
        ]

        self.size_combo = ttk.Combobox(
            self.tool_frame,
            textvariable=self.brush_size_var,
            values=size_options,
            state="readonly",
            width=10
        )
        self.size_combo.pack(pady=5)
        self.size_combo.bind("<<ComboboxSelected>>", self.on_brush_size_changed)

        tk.Button(
            self.tool_frame,
            text="Clear",
            command=self.clear_canvas,
            width=10
        ).pack(pady=10)

    def on_brush_size_changed(self, event):
        selected = self.brush_size_var.get()
        new_size_value = int(selected.split()[0])
        self.brush_size = new_size_value
        for width_enum in Width:
            if width_enum.value == new_size_value:
                self.change_brush_size(new_size_value)
                break

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.update()
        self.is_drawing = False
        self.last_x, self.last_y = None, None
import tkinter as tk

from matplotlib.dates import drange

class BetterPaint:
    def __init__(self, window):
        self.root = window
        self.root.geometry("1250x750")
        self.root.title("Better Paint")

        self.canvas = tk.Canvas(self.root, bg="white", width=1250, height=750)
        self.canvas.pack()
        self.bind()
        self.last_x = self.last_y = None
        self.is_drawing = False

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
                    fill="black",
                    width=3,
                    capstyle="round",
                    smooth=True,
                    splinesteps=36
                )
            self.last_x, self.last_y = x, y
    def start_drawing(self, event):
        self.is_drawing = True
    def stop_drawing(self, event):
        self.is_drawing = False
        self.last_x, self.last_y = None, None

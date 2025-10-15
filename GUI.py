from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import psutil

class GUI:
    BG_COLOR = "#1b0b45"
    FG_COLOR = "#f9fbf9"

    def render(self):
        self.gui = tk.Tk()
        self.gui.resizable(TRUE,TRUE)
        self.gui.iconbitmap("assets/TSA.ico")
        self.gui.title("TSA")
        self.gui.geometry("450x420")
        self.gui.configure(bg=self.BG_COLOR)
        
        # ---------- TITLE ----------
        titleFrame = tk.Frame(self.gui, bg=self.BG_COLOR)
        titleFrame.pack(side="top", fill="x", pady=10)
        welcome = tk.Label(
            titleFrame,
            text="TSA Cycle Calculator",
            bg=self.BG_COLOR,
            fg=self.FG_COLOR,
            font=("Comic Sans MS", 17, "bold")
        )
        welcome.pack()

        # ---------- TABS ----------
        notebook = ttk.Notebook(self.gui)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1
        tab1 = tk.Frame(notebook, bg=self.BG_COLOR)
        notebook.add(tab1, text="Formula 1")

        # Tab 2
        tab2 = tk.Frame(notebook, bg=self.BG_COLOR)
        notebook.add(tab2, text="Formula 2")

        self.build_section1(tab1)
        self.build_section2(tab2)

        # ---------- STYLES ----------
        ttk.Style().configure(
            'W.TButton',
            font=('Comic Sans MS', 12, 'bold'),
            foreground=self.BG_COLOR
        )

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab",
                background=self.BG_COLOR,
                foreground=self.FG_COLOR)
        style.map("TNotebook.Tab",
                background=[("active", "lightblue"), ("disabled", "gray"), ("selected", "#5089f2")],
                foreground=[("active", "black"), ("disabled", "gray")])

        # ---------- EXIT ----------
        self.gui.protocol("WM_DELETE_WINDOW",self.onDestroy)
        self.gui.mainloop()

    # ---------- SECTION 1 ----------
    def build_section1(self, parent: tk.Frame):
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Input", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 15, "bold")).grid(row=0, column=0, sticky="w")

        self.weight1 = DoubleVar()
        tk.Label(frame, text="L : Weight (하중)", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 14)).grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.weight1,
                 font=("Arial", 14), width=5).grid(row=1, column=1, padx=(10,0))
        tk.Label(frame, text="kg", bg=self.BG_COLOR, fg=self.FG_COLOR,
                 font=("Arial", 14)).grid(row=1, column=2, padx=(5,0))

        self.numWires1 = IntVar()
        tk.Label(frame, text="N : Number of wires (줄의 수)", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 14)).grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.numWires1,
                 font=("Arial", 14), width=5).grid(row=2, column=1, padx=(10,0))
        
        tk.Label(frame, text="Lifetime Prediction", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 15, "bold")).grid(row=3, column=0, sticky="w")

        tk.Label(frame, text="C(N,L) = k x N¹·²⁶ x L⁻¹·³⁸",
                 bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Arial", 14)).grid(row=4, column=0, sticky="w", columnspan=3)
        tk.Label(frame, text="k = 2.83 x 10⁵",
                 bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Arial", 14)).grid(row=5, column=0, sticky="w", columnspan=3)

        self.output1 = tk.Label(frame, text="Output: ", bg=self.BG_COLOR,
                                fg=self.FG_COLOR, font=("Arial", 14))
        self.output1.grid(row=6, column=0, sticky="w", columnspan=3)

        ttk.Button(frame, text="Calculate", command=self.calculate1, width=12).grid(
            row=7, column=0, pady=10, columnspan = 3)
        
    def calculate1(self):
        k = 2.83 * pow(10,5)
        varN = self.numWires1.get()
        varL = self.weight1.get()
        output = k * pow(varN, 1.26) * pow(varL,-1.38)
        self.output1.config(text=f"Output: {output:.2f} cycle")
        return

    # ---------- SECTION 2 ----------
    def build_section2(self, parent: tk.Frame):
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Input", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 15, "bold")).grid(row=0, column=0, sticky="w")

        self.weight2 = DoubleVar()
        tk.Label(frame, text="L : Weight (하중)", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 14)).grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.weight2,
                 font=("Arial", 14), width=5).grid(row=1, column=1, padx=(10,0))
        tk.Label(frame, text="kg", bg=self.BG_COLOR, fg=self.FG_COLOR,
                 font=("Arial", 14)).grid(row=1, column=2, padx=(5,0), sticky="w")

        self.diameter2 = DoubleVar()
        tk.Label(frame, text="D : Diameter (직경)", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 14)).grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.diameter2,
                 font=("Arial", 14), width=5).grid(row=2, column=1, padx=(10,0))
        tk.Label(frame, text="mm", bg=self.BG_COLOR, fg=self.FG_COLOR,
                 font=("Arial", 14)).grid(row=2, column=2, padx=(5,0), sticky="w")

        self.numWires2 = IntVar()
        tk.Label(frame, text="N : Number of wires (줄의 수)", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 14)).grid(row=3, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.numWires2,
                 font=("Arial", 14), width=5).grid(row=3, column=1, padx=(10,0))

        tk.Label(frame, text="Lifetime Prediction", bg=self.BG_COLOR,
                 fg=self.FG_COLOR, font=("Arial", 15, "bold")).grid(row=4, column=0, sticky="w")

        tk.Label(frame, text="C(N,L,D) = k x N¹·²²² x L⁻¹·³²⁶ x D²·⁵⁰⁹",
                 bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Arial", 14)).grid(row=5, column=0, sticky="w", columnspan=3)
        tk.Label(frame, text="k = 2.541 x 10⁵",
                 bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Arial", 14)).grid(row=6, column=0, sticky="w", columnspan=3)

        self.output2 = tk.Label(frame, text="Output: ", bg=self.BG_COLOR,
                                fg=self.FG_COLOR, font=("Arial", 14))
        self.output2.grid(row=7, column=0, sticky="w", columnspan=3)

        ttk.Button(frame, text="Calculate", command=self.calculate2, width=12).grid(
            row=8, column=0, pady=10, columnspan=3)
        
    def calculate2(self):
        k = 2.541 * pow(10,5)
        varN = self.numWires2.get()
        varL = self.weight2.get()
        varD = self.diameter2.get()
        output = k * pow(varN, 1.222) * pow(varL,-1.326) * pow(varD,2.509)
        self.output2.config(text=f"Output: {output:.2f} cycle")
        return

    def onDestroy(self):
        self.gui.destroy()
        psutil.Process(os.getpid()).terminate()

if __name__ == "__main__":
    ui = GUI()
    ui.render()
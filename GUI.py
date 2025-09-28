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
        # self.ControlWindow.iconbitmap(LOGO_PATH)
        self.gui.title("TSA")
        self.gui.geometry("900x590")
        self.gui.configure(bg=self.BG_COLOR)
        

        layoutFrame = tk.Frame(self.gui,bg=self.BG_COLOR)
        frame = tk.Frame(layoutFrame,bg=self.BG_COLOR)
        section1InputFrame = tk.Frame(layoutFrame,bg=self.BG_COLOR)
        section1OutputFrame = tk.Frame(layoutFrame,bg=self.BG_COLOR)
        button1Frame = tk.Frame(layoutFrame,bg=self.BG_COLOR)
        section2OutputFrame = tk.Frame(layoutFrame,bg=self.BG_COLOR)
        section2InputFrame = tk.Frame(layoutFrame,bg=self.BG_COLOR)
        button2Frame = tk.Frame(layoutFrame,bg=self.BG_COLOR)


        ttk.Style().configure('W.TButton', font =
               ('Comic Sans MS', 12, 'bold'),
                foreground = self.BG_COLOR)
        ttk.Style().map(
            'Custom.TCombobox',
            foreground=[('readonly', self.FG_COLOR)],
            selectforeground=[('readonly', self.FG_COLOR)],
        )
        

        # Labels
        welcome = tk.Label(frame,text="NGUYEN HAI",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Comic Sans MS",17,"bold"))
        welcome.grid(column=0,row=0,columnspan=4,sticky="news",pady=(0,20))


        inputLabel1 = tk.Label(section1InputFrame,text="Input section 1",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",15,"bold"))
        inputLabel1.grid(column=0,row=0,sticky=tk.W)

        self.weight1 = IntVar()
        weightLabel1 = tk.Label(section1InputFrame,text="Weight",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        weightLabel1.grid(column=0,row=1,sticky=tk.W)
        weightInput1 = tk.Entry(section1InputFrame,width=5,font=("Arial",14),textvariable=self.weight1)
        weightInput1.grid(column=1,row=1,sticky=W)
        weightUnit1 = tk.Label(section1InputFrame,text="gram(s)",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        weightUnit1.grid(column=2,row=1,sticky=tk.W)

        self.diameter1 = IntVar()
        diameterLabel1 = tk.Label(section1InputFrame,text="Diameter",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        diameterLabel1.grid(column=0,row=3,sticky=tk.W)
        diameterInput1 = tk.Entry(section1InputFrame,width=5,font=("Arial",14),textvariable=self.diameter1)
        diameterInput1.grid(column=1,row=3,sticky=W)
        diameterUnit1 = tk.Label(section1InputFrame,text="meter(s)",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        diameterUnit1.grid(column=2,row=3,sticky=tk.W)

        self.csa1 = IntVar()
        csaLabel1 = tk.Label(section1InputFrame,text="Cross-sectional area of the wire",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        csaLabel1.grid(column=0,row=5,sticky=tk.W)
        csaInput1 = tk.Entry(section1InputFrame,width=5,font=("Arial",14),textvariable=self.csa1)
        csaInput1.grid(column=1,row=5,sticky=W)
        csaUnit1 = tk.Label(section1InputFrame,text="square meter(s)",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        csaUnit1.grid(column=2,row=5,sticky=tk.W)

        self.numWires1 = IntVar()
        numWiresLabel1 = tk.Label(section1InputFrame,text="Number of wires",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        numWiresLabel1.grid(column=0,row=7,sticky=tk.W)
        numWiresInput1 = tk.Entry(section1InputFrame,width=5,font=("Arial",14),textvariable=self.numWires1)
        numWiresInput1.grid(column=1,row=7,sticky=W)



        outLabel1 = tk.Label(section1OutputFrame,text="Output section 1",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",15,"bold"))
        outLabel1.grid(column=0,row=0,sticky=tk.W)

        fomulaLabel1 = tk.Label(section1OutputFrame,text="C(N,L) = k x N¹·²⁶ x L⁻¹·³⁸",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        fomulaLabel1.grid(column=0,row=1,sticky=tk.W)

        kConstantLabel1 = tk.Label(section1OutputFrame,text="k = 2.83 x 10⁵",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        kConstantLabel1.grid(column=0,row=2,sticky=tk.W)

        self.output1 = tk.Label(section1OutputFrame,text="Output: ",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        self.output1.grid(column=0,row=3,sticky=tk.W, rowspan=2)

        # Button
        calculateButton1 =  ttk.Button(button1Frame,text="Calculate",style = 'W.TButton',command = self.calculate1,width=10)
        calculateButton1.grid(column=0,row=4)

        # SECTION 2
        inputLabel2 = tk.Label(section2InputFrame,text="Input section 2",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",15,"bold"))
        inputLabel2.grid(column=0,row=0,sticky=tk.W)

        self.weight2 = IntVar()
        weightLabel2 = tk.Label(section2InputFrame,text="Weight",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        weightLabel2.grid(column=0,row=1,sticky=tk.W)
        weightInput2 = tk.Entry(section2InputFrame,width=5,font=("Arial",14),textvariable=self.weight2)
        weightInput2.grid(column=1,row=1,sticky=W)
        weightUnit2 = tk.Label(section2InputFrame,text="gram(s)",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        weightUnit2.grid(column=2,row=1,sticky=tk.W)

        self.diameter2 = IntVar()
        diameterLabel2 = tk.Label(section2InputFrame,text="Diameter",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        diameterLabel2.grid(column=0,row=3,sticky=tk.W)
        diameterInput2 = tk.Entry(section2InputFrame,width=5,font=("Arial",14),textvariable=self.diameter2)
        diameterInput2.grid(column=1,row=3,sticky=W)
        diameterUnit2 = tk.Label(section2InputFrame,text="meter(s)",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        diameterUnit2.grid(column=2,row=3,sticky=tk.W)

        self.csa2 = IntVar()
        csaLabel2 = tk.Label(section2InputFrame,text="Cross-sectional area of the wire",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        csaLabel2.grid(column=0,row=5,sticky=tk.W)
        csaInput2 = tk.Entry(section2InputFrame,width=5,font=("Arial",14),textvariable=self.csa2)
        csaInput2.grid(column=1,row=5,sticky=W)
        csaUnit2 = tk.Label(section2InputFrame,text="square meter(s)",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        csaUnit2.grid(column=2,row=5,sticky=tk.W)

        self.numWires2 = IntVar()
        numWiresLabel2 = tk.Label(section2InputFrame,text="Number of wires",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        numWiresLabel2.grid(column=0,row=7,sticky=tk.W)
        numWiresInput2 = tk.Entry(section2InputFrame,width=5,font=("Arial",14),textvariable=self.numWires2)
        numWiresInput2.grid(column=1,row=7,sticky=W)



        outLabel2 = tk.Label(section2OutputFrame,text="Output section 2",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",15,"bold"))
        outLabel2.grid(column=0,row=0,sticky=tk.W)

        fomulaLabel2 = tk.Label(section2OutputFrame,text="C(N,L,D) = k x N¹·²²² x L⁻¹·³²⁶ x D²·⁵⁰⁹",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        fomulaLabel2.grid(column=0,row=1,sticky=tk.W)

        kConstantLabel2 = tk.Label(section2OutputFrame,text="k = 2.541 x 10⁵",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        kConstantLabel2.grid(column=0,row=2,sticky=tk.W)

        self.output2 = tk.Label(section2OutputFrame,text="Output: ",bg=self.BG_COLOR,fg=self.FG_COLOR,font=("Arial",14))
        self.output2.grid(column=0,row=3,sticky=tk.W, rowspan=2)

        # Button
        calculateButton2 =  ttk.Button(button2Frame,text="Calculate",style = 'W.TButton',command = self.calculate2,width=10)
        calculateButton2.grid(column=0,row=4)


        frame.grid(row=0,column=0,padx=10,columnspan=2)
        section1InputFrame.grid(row=1,column=0,sticky="w",pady=(30,0),padx=30)
        section1OutputFrame.grid(row=1,column=1,sticky="w",pady=20, padx=(30,0))
        button1Frame.grid(row=2,column=0,padx=10,columnspan=2,pady=20)
        section2InputFrame.grid(row=3,column=0,sticky="w",pady=(30,0),padx=30)
        section2OutputFrame.grid(row=3,column=1,sticky="w",pady=20, padx=(30,0))
        button2Frame.grid(row=4,column=0,padx=10,columnspan=2,pady=20)
        layoutFrame.pack()

        self.gui.protocol("WM_DELETE_WINDOW",self.onDestroy)
        self.gui.mainloop()
    

    def calculate1(self):
        k = 2.83 * pow(10,5)
        varN = self.numWires1.get()
        varL = self.weight1.get()
        output = k * pow(varN, 1.26) * pow(varL,-1.38)
        self.output1.config(text=f"Output: {output} cycle")
        return
    
    def calculate2(self):
        k = 2.541 * pow(10,5)
        varN = self.numWires2.get()
        varL = self.weight2.get()
        varD = self.diameter2.get()
        output = k * pow(varN, 1.222) * pow(varL,-1.326) * pow(varD,2.509)
        self.output2.config(text=f"Output: {output} cycle")
        return


    def onDestroy(self):
        self.gui.destroy()
        psutil.Process(os.getpid()).terminate()




if __name__ == "__main__":
    ui = GUI()
    ui.render()
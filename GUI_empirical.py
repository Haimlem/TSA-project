# tsa_gui_all_models.py
# Empirical (Formula 2) + Hybrid (Empirical + residual) + LR + RF + XGB + GPR tabs
# LR/RF/XGB/GPR tabs now mirror the Hybrid tab layout (Empirical, Model, Delta)

import os, math, psutil, numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import joblib

class TSAGUI:
    BG = "#1b0b45"
    FG = "#f9fbf9"
    ACCENT = "#5089f2"

    # Empirical (Formula 2) constants
    K = 2.541e5
    EXP_N = 1.222
    EXP_W = -1.326
    EXP_D = 2.509

    # Model files
    PATH_HYB = "tsa_cycle_predictor_hybrid.pkl"  # predicts residual
    PATH_LR  = "tsa_cycle_predictor_LN.pkl"
    PATH_RF  = "tsa_cycle_predictor_RF.pkl"
    PATH_XGB = "tsa_cycle_predictor_XGB.pkl"
    PATH_GPR = "tsa_cycle_predictor_GPR.pkl"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TSA Lifespan — Empirical, Hybrid, and ML Models")
        self.root.geometry("750x450")
        self.root.configure(bg=self.BG)
        self.root.resizable(True, True)
        try:
            self.root.iconbitmap("assets/TSA.ico")
        except Exception:
            pass

        # ttk styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("TLabel", background=self.BG, foreground=self.FG, font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 16, "bold"))
        style.configure("Small.TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 12, "bold"), foreground=self.BG)
        style.configure("TNotebook", background=self.BG)
        style.configure("TNotebook.Tab", background=self.BG, foreground=self.FG, padding=(12, 6))
        style.map("TNotebook.Tab", background=[("selected", self.ACCENT)], foreground=[("selected", "white")])

        ttk.Label(self.root, text="TSA Cycle Calculator — Empirical, Hybrid & ML", style="Header.TLabel").pack(pady=(12, 6))

        # Shared inputs
        shared = ttk.Frame(self.root); shared.pack(fill="x", padx=12, pady=(6, 0))
        self._build_shared_inputs(shared)

        # Tabs
        nb = ttk.Notebook(self.root); nb.pack(fill="both", expand=True, padx=12, pady=12)

        # Empirical
        self.tab_emp = ttk.Frame(nb); nb.add(self.tab_emp, text="Empirical (Formula 2)")
        self._build_empirical_tab(self.tab_emp)

        # Hybrid (Empirical + Residual)
        self.tab_hyb = ttk.Frame(nb); nb.add(self.tab_hyb, text="Hybrid (Empirical + Residual)")
        self._build_hybrid_like_tab(self.tab_hyb, title="Hybrid Prediction", model_key="HYB",
                                    model_path=self.PATH_HYB, is_hybrid=True)

        # LR / RF / XGB / GPR — identical layout to Hybrid tab, but direct model outputs
        self.tab_lr = ttk.Frame(nb); nb.add(self.tab_lr, text="Linear Regression")
        self._build_hybrid_like_tab(self.tab_lr, title="Linear Regression Prediction",
                                    model_key="LR", model_path=self.PATH_LR, is_hybrid=False)

        self.tab_rf = ttk.Frame(nb); nb.add(self.tab_rf, text="Random Forest")
        self._build_hybrid_like_tab(self.tab_rf, title="Random Forest Prediction",
                                    model_key="RF", model_path=self.PATH_RF, is_hybrid=False)

        self.tab_xgb = ttk.Frame(nb); nb.add(self.tab_xgb, text="XGBoost")
        self._build_hybrid_like_tab(self.tab_xgb, title="XGBoost Prediction",
                                    model_key="XGB", model_path=self.PATH_XGB, is_hybrid=False)

        self.tab_gpr = ttk.Frame(nb); nb.add(self.tab_gpr, text="GPR")
        self._build_hybrid_like_tab(self.tab_gpr, title="GPR Prediction",
                                    model_key="GPR", model_path=self.PATH_GPR, is_hybrid=False)

        self._models = {}
        self.root.protocol("WM_DELETE_WINDOW", self._on_destroy)

    # ---------------- Shared Inputs ----------------
    def _build_shared_inputs(self, parent: ttk.Frame):
        self.var_W = tk.DoubleVar(value=20.0)
        self.var_D = tk.DoubleVar(value=1.5)
        self.var_N = tk.IntVar(value=4)
        self.var_A = tk.StringVar(value="—")

        r = 0
        ttk.Label(parent, text="W (kg)").grid(row=r, column=0, sticky="w")
        ttk.Entry(parent, textvariable=self.var_W, width=10).grid(row=r, column=1, sticky="w", padx=(6, 16))

        ttk.Label(parent, text="D (mm)").grid(row=r, column=2, sticky="w")
        ttk.Entry(parent, textvariable=self.var_D, width=10).grid(row=r, column=3, sticky="w", padx=(6, 16))

        ttk.Label(parent, text="N (count)").grid(row=r, column=4, sticky="w")
        ttk.Entry(parent, textvariable=self.var_N, width=10).grid(row=r, column=5, sticky="w", padx=(6, 16))

        ttk.Label(parent, text="A (mm²)").grid(row=r, column=6, sticky="e")
        ttk.Label(parent, textvariable=self.var_A).grid(row=r, column=7, sticky="w", padx=(6, 0))

        r += 1
        ttk.Label(parent, text="Presets").grid(row=r, column=0, sticky="w", pady=(8, 0))
        presets = ttk.Combobox(parent, state="readonly", width=40, values=[
            "Sample 1 — W=15, D=1.0, N=3",
            "Sample 2 — W=20, D=1.5, N=4",
            "Sample 3 — W=25, D=2.0, N=6"
        ])
        presets.grid(row=r, column=1, columnspan=7, sticky="w", padx=(6, 0), pady=(8, 0))
        presets.bind("<<ComboboxSelected>>", lambda e: self._apply_preset(presets.get()))

        self._update_area()
        for v in (self.var_D, self.var_N):
            v.trace_add("write", lambda *_: self._update_area())

    def _apply_preset(self, label: str):
        if "Sample 1" in label:
            self.var_W.set(15.0); self.var_D.set(1.0); self.var_N.set(3)
        elif "Sample 2" in label:
            self.var_W.set(20.0); self.var_D.set(1.5); self.var_N.set(4)
        elif "Sample 3" in label:
            self.var_W.set(25.0); self.var_D.set(2.0); self.var_N.set(6)
        self._update_area()

    def _update_area(self):
        try:
            N = int(self.var_N.get()); D = float(self.var_D.get())
            if N <= 0 or D <= 0: self.var_A.set("—"); return
            self.var_A.set(f"{(N * math.pi * (D**2) / 4.0):,.2f}")
        except Exception:
            self.var_A.set("—")

    # ---------------- Empirical Tab ----------------
    def _build_empirical_tab(self, parent: ttk.Frame):
        frm = ttk.Frame(parent); frm.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(frm, text="Empirical Lifetime (Formula 2)", style="Header.TLabel").pack(anchor="w")
        ttk.Label(frm, text="C(N, W, D) = k · N^1.222 · W^-1.326 · D^2.509,    k = 2.541 × 10^5").pack(anchor="w", pady=(4, 8))

        btns = ttk.Frame(frm); btns.pack(anchor="w", pady=(4, 8))
        ttk.Button(btns, text="Calculate (Empirical)", command=self._calc_empirical, width=22).pack(side="left")

        self.emp_out = ttk.Label(frm, text="Empirical: —", style="Header.TLabel"); self.emp_out.pack(anchor="w", pady=(8, 0))

    def _calc_empirical(self):
        try:
            W, D, N = float(self.var_W.get()), float(self.var_D.get()), int(self.var_N.get())
            if W <= 0 or D <= 0 or N <= 0: raise ValueError
            c = self._empirical_cycles(W, D, N)
            self.emp_out.config(text=f"Empirical: {c:,.0f} cycles")
        except Exception:
            messagebox.showerror("Invalid Input", "Enter positive numeric values for W, D, and N.")

    @staticmethod
    def _empirical_cycles(W, D, N):
        return TSAGUI.K * (N ** TSAGUI.EXP_N) * (W ** TSAGUI.EXP_W) * (D ** TSAGUI.EXP_D)

    # ---------------- Hybrid-like Tabs (Unified Layout) ----------------
    def _build_hybrid_like_tab(self, parent: ttk.Frame, title: str, model_key: str, model_path: str, is_hybrid: bool):
        """
        Unified layout for Hybrid and all ML models:
        - Shows Empirical, Model result, and Δ vs Empirical.
        - If is_hybrid=True, the model predicts residual; final = empirical + residual.
        - Else, the model predicts final directly (optionally back-transform if log1p-trained).
        """
        # Frame & title
        frm = ttk.Frame(parent); frm.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(frm, text=title, style="Header.TLabel").pack(anchor="w")

        # Options row (for non-hybrid models: back-transform)
        opt = ttk.Frame(frm); opt.pack(anchor="w", pady=(8, 8))
        if not is_hybrid:
            setattr(self, f"ck_log_{model_key}", tk.BooleanVar(value=False))
            ttk.Checkbutton(opt,
                text="Model outputs log1p(cycles); back-transform with exp(y) - 1",
                variable=getattr(self, f"ck_log_{model_key}")
            ).pack(anchor="w")

        # Buttons
        btns = ttk.Frame(frm); btns.pack(anchor="w", pady=(10, 8))
        ttk.Button(btns, text=f"Calculate ({'Hybrid' if is_hybrid else model_key})",
                   command=lambda mk=model_key, mp=model_path, hy=is_hybrid: self._calc_hybrid_like(mk, mp, hy),
                   width=26).pack(side="left")

        # Outputs (Empirical, Model, Delta)
        setattr(self, f"{model_key}_emp", ttk.Label(frm, text="Empirical: —", style="Header.TLabel"))
        getattr(self, f"{model_key}_emp").pack(anchor="w", pady=(8, 0))

        setattr(self, f"{model_key}_out", ttk.Label(frm, text=f"{'Hybrid' if is_hybrid else model_key}: —", style="Header.TLabel"))
        getattr(self, f"{model_key}_out").pack(anchor="w")

        setattr(self, f"{model_key}_diff", ttk.Label(frm, text="Δ vs Empirical: — (— %)", style="Small.TLabel"))
        getattr(self, f"{model_key}_diff").pack(anchor="w", pady=(2, 0))

    def _calc_hybrid_like(self, model_key: str, model_path: str, is_hybrid: bool):
        # Validate inputs
        try:
            W, D, N = float(self.var_W.get()), float(self.var_D.get()), int(self.var_N.get())
            if W <= 0 or D <= 0 or N <= 0: raise ValueError
        except Exception:
            messagebox.showerror("Invalid Input", "Enter positive numeric values for W, D, and N.")
            return

        # Empirical baseline
        empirical = self._empirical_cycles(W, D, N)
        getattr(self, f"{model_key}_emp").config(text=f"Empirical: {empirical:,.0f} cycles")

        # Load model
        mdl = self._get_model(model_key, model_path)
        if mdl is None: return

        # Build features in the exact training order: [W, D, N, A]
        A = (N * math.pi * (D ** 2) / 4.0)
        x = np.array([[W, D, N, A]], dtype=float)

        # Predict
        try:
            y = float(mdl.predict(x)[0])
        except Exception as e:
            messagebox.showerror("Prediction Error", f"{'Hybrid' if is_hybrid else model_key} prediction failed:\n{e}")
            return

        if is_hybrid:
            # model output is residual
            final = empirical + y
            label_name = "Hybrid"
        else:
            # model output is final; optional back-transform
            log_flag = getattr(self, f"ck_log_{model_key}").get() if hasattr(self, f"ck_log_{model_key}") else False
            if log_flag:
                try:
                    y = math.exp(y) - 1.0
                except Exception:
                    messagebox.showerror("Transform Error", "Back-transform failed. Is the model truly log1p-trained?")
                    return
            final = y
            label_name = model_key

        getattr(self, f"{model_key}_out").config(text=f"{label_name}: {final:,.0f} cycles")

        # Delta vs empirical
        delta = final - empirical
        pct = (delta / empirical * 100.0) if empirical else 0.0
        sign = "+" if delta >= 0 else "−"
        getattr(self, f"{model_key}_diff").config(text=f"Δ vs Empirical: {sign}{abs(delta):,.0f} cycles ({sign}{abs(pct):.2f} %)")

    # ---------------- Model loading ----------------
    def _get_model(self, key: str, path: str):
        if not hasattr(self, "_models"): self._models = {}
        if key in self._models: return self._models[key]
        if not os.path.exists(path):
            messagebox.showerror("Model Missing", f"Could not find {path}.\nPlace the .pkl in the same folder.")
            return None
        try:
            mdl = joblib.load(path)
            self._models[key] = mdl
            return mdl
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load {path}:\n{e}")
            return None

    # ---------------- Run / Exit ----------------
    def run(self):
        self.root.mainloop()

    def _on_destroy(self):
        try:
            self.root.destroy()
            psutil.Process(os.getpid()).terminate()
        except Exception:
            pass

if __name__ == "__main__":
    TSAGUI().run()

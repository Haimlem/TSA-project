When you input weight, diameter, cross-sectional area of the wire, number of wires, etc., an experiment was conducted to determine after how many executions the wire broke (in this case, 8 times),
and the number of executions before breaking was recorded. Using the above table, AI is employed to calculate the expected lifespan (number of executions) based on the input conditions.
The goal is for the wire to operate without breaking for more than 60,000 executions. The second task is to implement the following formulas on a GUI screen. Since there are two types of formulas,
there will be two types of screens. For the given input values, C is calculated, where C represents the expected lifespan (number of executions). Any programming language may be used.

🧩 Predicting the Lifespan of Twisted String Actuators Using Hybrid Machine Learning Models

This repository contains the complete implementation, datasets, and GUI system for the paper:
“Predicting the Lifespan of Twisted String Actuators Using Hybrid Machine Learning Models.”

The project integrates empirical modeling with machine learning (ML)—specifically Linear Regression, Random Forest, XGBoost, Gaussian Process Regression (GPR), and a Hybrid Empirical–XGBoost model—to predict the fatigue lifespan of Twisted String Actuators (TSAs).

📘 Overview

Twisted String Actuators convert rotational motion into linear displacement through the twisting of flexible cables.
While compact and efficient, their fatigue life under cyclic loading remains a critical limitation.

This project addresses that challenge using:
  + Empirical Weibull-based regression models
  + Data-driven ML algorithms
  + A hybrid physics-guided XGBoost framework
  + A Python-based GUI for real-time testing and design exploration

⚙️ Setup and Usage
1. Clone the repository
2. Install dependencies
3. Run model training or evaluation
4. Launch the GUI (GUI_empirical.py)

🧠 Models Implemented
  + Empirical Model:	Weibull-based regression derived from mechanical fatigue data
  + Linear Regression (LR)	Baseline interpretable model for feature contribution analysis
  + Random Forest (RF)	Ensemble-based nonlinear learner for moderate data sizes
  + XGBoost (XGB)	Gradient-boosted tree model optimized for small datasets
  + Gaussian Process Regression (GPR)	Bayesian model with uncertainty quantification
  + Hybrid Empirical–XGBoost	Combines empirical equation (as prior) + residual XGBoost correction

🖥️ Graphical User Interface (GUI)
A lightweight Tkinter-based GUI enables:
  + Manual or preset input of W, D, N
  + Real-time computation of predicted lifespan (cycles)
  + Comparison across all models
  + Visualization of prediction deltas (Δ vs empirical)

📈 Dataset Description
Size: 144 samples
Variables: Weight (W), Diameter (D), Number of strings (N), Cycles to failure (C)
All experiments were conducted using a servo-motor-based TSA test rig under controlled temperature and humidity conditions.

📩 Contact
For questions, collaboration, or dataset access requests:
Email: hainguyen091520@gmail.com
Repository: https://github.com/Haimlem/TSA-project

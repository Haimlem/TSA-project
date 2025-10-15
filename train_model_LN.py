import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Load and Parse Data
df = pd.read_excel('TSA 실험데이터_250923.xlsx', sheet_name="Sheet2", header=None)

rows = []
block_starts = [(3, 15), (22, 20), (41, 25)]
diameters = [1, 1.5, 2]
n_wire_labels = [2, 3, 4, 5, 6, 7]

for block_start, weight in block_starts:
    for d_idx, diameter in enumerate(diameters):
        col_block = 2 + d_idx * 8
        area_row = block_start + 1
        for ci in range(len(n_wire_labels)):
            if area_row < df.shape[0] and (col_block + ci) < df.shape[1]:
                val = df.iloc[area_row, col_block + ci]
                try:
                    area = float(val)
                except Exception:
                    area = np.nan
                for rep in range(1, 9):
                    data_row = area_row + rep
                    if data_row < df.shape[0] and (col_block + ci) < df.shape[1]:
                        executions = df.iloc[data_row, col_block + ci]
                        try:
                            executions = float(executions)
                            rows.append({
                                "Weight": weight,
                                "Diameter": diameter,
                                "NumWires": n_wire_labels[ci],
                                "Area": area,
                                "Executions": executions
                            })
                        except Exception:
                            continue

data = pd.DataFrame(rows).dropna()

print(f"✅ Parsed {len(data)} valid experiment rows")
print(data.head())

# Linear Regression
data["LogExecutions"] = np.log(data["Executions"])

X = data[["Weight", "Diameter", "NumWires", "Area"]]
y = data["LogExecutions"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Predictions (log scale and real scale)
y_pred_log = model.predict(X_test)
y_pred_real = np.exp(y_pred_log)
y_test_real = np.exp(y_test)

# Evaluation Metrics
r2 = r2_score(y_test, y_pred_log)
rmse_log = np.sqrt(mean_squared_error(y_test, y_pred_log))
mae_log = mean_absolute_error(y_test, y_pred_log)
rmse_real = np.sqrt(mean_squared_error(y_test_real, y_pred_real))

print("\n===== Model Performance =====")
print(f"R² (log scale): {r2:.4f}")
print(f"RMSE (log scale): {rmse_log:.4f}")
print(f"MAE (log scale): {mae_log:.4f}")
print(f"RMSE (real scale): {rmse_real:.2f} cycles")

# Save Model and Coefficients
joblib.dump(model, "tsa_cycle_predictor_LN.pkl")
print("Model saved as tsa_cycle_predictor_LN.pkl")

coeffs = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_
})
coeffs["Interpretation"] = [
    "Positive → longer lifespan" if c > 0 else "Negative → shorter lifespan"
    for c in coeffs["Coefficient"]
]
coeffs.to_csv("tsa_cycle_coefficients.csv", index=False)
print("\nModel Coefficients:")
print(coeffs)

# Example Predictions
test_cases = np.array([
    [15, 1.0, 3, 2.35],
    [20, 1.5, 4, 5.3],
    [25, 2.0, 6, 12.56]
])
preds = np.exp(model.predict(test_cases))
print("\n===== Sample Predictions (Real Scale) =====")
for i, p in enumerate(preds):
    print(f"{test_cases[i]} → {p:.0f} cycles")

print("\n✅ Training completed successfully.")
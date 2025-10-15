import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor
import joblib

# Load and parse data
df = pd.read_excel("TSA 실험데이터_250923.xlsx", sheet_name="Sheet2", header=None)

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
                        try:
                            executions = float(df.iloc[data_row, col_block + ci])
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

# Train XGBoost model
X = data[["Weight", "Diameter", "NumWires", "Area"]]
y = np.log1p(data["Executions"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

xgb_model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42
)

xgb_model.fit(X_train, y_train)

# Evaluate
y_pred = xgb_model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

cross_r2 = cross_val_score(xgb_model, X, y, cv=5, scoring='r2').mean()

print("\n===== XGBoost Results =====")
print(f"R² (log scale): {r2:.4f}")
print(f"RMSE (log scale): {rmse:.4f}")
print(f"MAE (log scale): {mae:.4f}")
print(f"Cross-validated R² mean: {cross_r2:.4f}")

# Back-transform RMSE to real scale
real_rmse = np.expm1(rmse)  
print(f"RMSE (real scale): {real_rmse:.2f} cycles")

# Feature importance
importances = pd.DataFrame({
    "Feature": X.columns,
    "Importance": xgb_model.feature_importances_
}).sort_values(by="Importance", ascending=False)
print("\nFeature Importances:\n", importances)

# Save model
joblib.dump(xgb_model, "tsa_cycle_predictor_XGB.pkl")
print("\n✅ Model saved as tsa_cycle_predictor_XGB.pkl")

# Test predictions
sample_inputs = np.array([
    [15, 1.0, 3, 2.35],
    [20, 1.5, 4, 5.3],
    [25, 2.0, 6, 12.56]
])
preds = np.expm1(xgb_model.predict(sample_inputs))

print("\nSample Predictions (Real Scale):")
for x, p in zip(sample_inputs, preds):
    print(f"{x} → {p:.0f} cycles")

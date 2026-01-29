import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("gesture_data.csv", header=None)

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

joblib.dump(model, "gesture_model.pkl")

print("Gesture model trained successfully")

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv('data.csv')

# Define features and label
X = data[['ip_score', 'time_score', 'device_score', 'frequency', 'geo_score']]
y = data['label']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, 'behavior_model.pkl')
print("Model trained and saved as behavior_model.pkl")

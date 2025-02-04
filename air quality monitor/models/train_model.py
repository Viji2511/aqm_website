import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
import joblib

# Step 1: Load the dataset
data = pd.read_csv('revised_feed.csv')  # Replace with the correct path to your CSV file

# Step 2: Handle missing values (if any)
data = data.ffill()  # Forward fill missing values

# Step 3: Extract features (fields) and target variable (dust levels)
# Assuming 'field1' is mq7, 'field2' is mq135, and 'field3' is dust level
X = data[['field1', 'field2']]  # Features (MQ-7 and MQ-135)
y = data['field3']  # Target variable (dust levels)

# Step 4: Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Standardize the features (optional but often improves model performance)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 6: Train a simple linear regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Step 7: Make predictions and evaluate the model
y_pred = model.predict(X_test_scaled)

# Step 8: Print evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Step 9: Save the trained model and scaler for future use
joblib.dump(model, 'dust_level_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model and scaler saved successfully!")
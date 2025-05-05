import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

np.random.seed(42)

data = {
    'size': np.random.uniform(500, 5000, 100),
    'bedrooms': np.random.randint(1, 6, 100),
    'age': np.random.randint(0, 50, 100),
    'location': np.random.choice(['Urban', 'Suburban', 'Rural'], 100),
    'price': np.random.uniform(100000, 1000000, 100)
}
df = pd.DataFrame(data)

df = pd.get_dummies(df, columns=['location'], drop_first=True)
X = df.drop('price', axis=1)
y = df['price']
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_mse = []
cv_r2 = []
for train_idx, val_idx in kf.split(X_train):
    X_tr, X_val = X_train[train_idx], X_train[val_idx]
    y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_val)
    cv_mse.append(mean_squared_error(y_val, y_pred))
    cv_r2.append(r2_score(y_val, y_pred))
print("K-Fold CV Average MSE:", np.mean(cv_mse))
print("K-Fold CV Average R2:", np.mean(cv_r2))

y_pred_test = model.predict(X_test)
test_mse = mean_squared_error(y_test, y_pred_test)
test_r2 = r2_score(y_test, y_pred_test)
print("Test Set MSE:", test_mse)
print("Test Set R2:", test_r2)

X_columns = ['size', 'bedrooms', 'age', 'location_Suburban', 'location_Urban']
new_house = pd.DataFrame({
    'size': [3000],
    'bedrooms': [3],
    'age': [10],
    'location': ['Urban']
})
new_house = pd.get_dummies(new_house, columns=['location'], drop_first=True)
for col in X_columns:
    if col not in new_house.columns:
        new_house[col] = 0
new_house = new_house[X_columns]
new_house = scaler.transform(new_house)
predicted_price = model.predict(new_house)
print("Predicted Price for New House:", predicted_price[0])
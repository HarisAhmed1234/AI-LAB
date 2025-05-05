import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.tree import export_text

np.random.seed(42)

data = {
    'total_spending': np.random.uniform(100, 10000, 100),
    'age': np.random.randint(18, 80, 100),
    'visits': np.random.randint(1, 50, 100),
    'purchase_freq': np.random.uniform(0.1, 1.0, 100),
    'is_high_value': np.random.randint(0, 2, 100)
}
df = pd.DataFrame(data)

df['total_spending'] = np.clip(df['total_spending'], 100, 5000)
df['visits'] = np.clip(df['visits'], 1, 30)
X = df.drop('is_high_value', axis=1)
y = df['is_high_value']
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_accuracy = []
cv_precision = []
cv_recall = []
for train_idx, val_idx in kf.split(X_train):
    X_tr, X_val = X_train[train_idx], X_train[val_idx]
    y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_val)
    cv_accuracy.append(accuracy_score(y_val, y_pred))
    cv_precision.append(precision_score(y_val, y_pred))
    cv_recall.append(recall_score(y_val, y_pred))
print("K-Fold CV Average Accuracy:", np.mean(cv_accuracy))
print("K-Fold CV Average Precision:", np.mean(cv_precision))
print("K-Fold CV Average Recall:", np.mean(cv_recall))

y_pred_test = model.predict(X_test)
print("Test Set Accuracy:", accuracy_score(y_test, y_pred_test))
print("Test Set Precision:", precision_score(y_test, y_pred_test))
print("Test Set Recall:", recall_score(y_test, y_pred_test))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_test))

rules = export_text(model, feature_names=['total_spending', 'age', 'visits', 'purchase_freq'])
print("Decision Tree Rules:\n", rules)
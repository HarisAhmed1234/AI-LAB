import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

np.random.seed(42)

data = {
    'word_freq': np.random.uniform(0, 1, 100),
    'email_length': np.random.randint(50, 500, 100),
    'has_link': np.random.randint(0, 2, 100),
    'sender_domain': np.random.choice(['gmail.com', 'yahoo.com', 'outlook.com'], 100),
    'is_spam': np.random.randint(0, 2, 100)
}
df = pd.DataFrame(data)

le = LabelEncoder()
df['sender_domain'] = le.fit_transform(df['sender_domain'])
X = df.drop('is_spam', axis=1)
y = df['is_spam']
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_accuracy = []
cv_precision = []
cv_recall = []
cv_roc_auc = []
for train_idx, val_idx in kf.split(X_train):
    X_tr, X_val = X_train[train_idx], X_train[val_idx]
    y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]
    cv_accuracy.append(accuracy_score(y_val, y_pred))
    cv_precision.append(precision_score(y_val, y_pred))
    cv_recall.append(recall_score(y_val, y_pred))
    cv_roc_auc.append(roc_auc_score(y_val, y_proba))
print("K-Fold CV Average Accuracy:", np.mean(cv_accuracy))
print("K-Fold CV Average Precision:", np.mean(cv_precision))
print("K-Fold CV Average Recall:", np.mean(cv_recall))
print("K-Fold CV Average ROC-AUC:", np.mean(cv_roc_auc))

y_pred_test = model.predict(X_test)
y_proba_test = model.predict_proba(X_test)[:, 1]
print("Test Set Accuracy:", accuracy_score(y_test, y_pred_test))
print("Test Set Precision:", precision_score(y_test, y_pred_test))
print("Test Set Recall:", recall_score(y_test, y_pred_test))
print("Test Set ROC-AUC:", roc_auc_score(y_test, y_proba_test))

new_email = pd.DataFrame({
    'word_freq': [0.5],
    'email_length': [200],
    'has_link': [1],
    'sender_domain': ['gmail.com']
})
new_email['sender_domain'] = le.transform(new_email['sender_domain'])
new_email = scaler.transform(new_email)
prediction = model.predict(new_email)
print("New Email Classified as Spam (1) or Not Spam (0):", prediction[0])
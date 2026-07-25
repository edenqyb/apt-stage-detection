from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, StratifiedKFold
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def calculate_metrics(cm):
    TP = np.diag(cm)
    FP = cm.sum(axis=0) - TP
    FN = cm.sum(axis=1) - TP
    TN = cm.sum() - (FP + FN + TP)
    
    accuracy = (TP + TN).sum() / (TP + FP + FN + TN).sum()
    precision = np.mean(TP / (TP + FP + 1e-9))
    recall = np.mean(TP / (TP + FN + 1e-9))
    f1_score = 2 * (precision * recall) / (precision + recall + 1e-9)
    
    return TP, TN, FP, FN, accuracy, precision, recall, f1_score

# Load Data
dapt_data = 'dapt_data.csv'
dapt = pd.read_csv(dapt_data)

# Encode Labels
class_mapping = {
    'Benign': 0,
    'BENIGN': 0,
    'Reconnaissance': 1,
    'Establish Foothold': 2,
    'Lateral Movement': 3,
    'Data Exfiltration': 4
}
dapt['Label'] = dapt['Stage'].map(class_mapping)

# Prepare Features and Labels
X = dapt.drop(['Timestamp', 'Label', 'Stage', 'Activity'], axis=1)
y = dapt['Label']

# Normalize Features
scaler = MinMaxScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
# max_depth_values = [15, 20]
# n_estimators_values = [50, 75]

max_depth_values = [15]
n_estimators_values = [75]

results = {'max_depth': [], 'n_estimators': [], 'train_accuracy': [], 'test_accuracy': []}
metrics = {'max_depth': [], 'n_estimators': [], 'accuracy': [], 'precision': [], 'recall': [], 'f1_score': []}

kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_results = []

confusion_matrices = {}

# Loop through combinations of max_depth and n_estimators
for max_depth in max_depth_values:
    for n_estimators in n_estimators_values:
        rf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        rf.fit(X_train, y_train)
        
        train_acc = rf.score(X_train, y_train)
        test_acc = rf.score(X_test, y_test)

        y_pred = rf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)

        scores = cross_val_score(rf, X, y, cv=kf, scoring='accuracy')
        cv_results.append({
            'max_depth': max_depth,
            'n_estimators': n_estimators,
            'mean_accuracy': scores.mean(),
            'std_accuracy': scores.std()
        })

        TP, TN, FP, FN, acc, prec, rec, f1 = calculate_metrics(cm)
        confusion_matrices[(max_depth, n_estimators)] = cm
        
        metrics['max_depth'].append(max_depth)
        metrics['n_estimators'].append(n_estimators)
        metrics['accuracy'].append(acc)
        metrics['precision'].append(prec)
        metrics['recall'].append(rec)
        metrics['f1_score'].append(f1)

        results['max_depth'].append(max_depth)
        results['n_estimators'].append(n_estimators)
        results['train_accuracy'].append(train_acc)
        results['test_accuracy'].append(test_acc)

results_df = pd.DataFrame(results)
metrics_df = pd.DataFrame(metrics)
cv_results_df = pd.DataFrame(cv_results)

print(metrics_df)
print(cv_results_df)

plt.figure(figsize=(14, 6))

pivot_test = results_df.pivot(index="max_depth", columns="n_estimators", values="test_accuracy")
sns.heatmap(pivot_test, annot=True, fmt=".3f", cmap="YlGnBu")
plt.title("Test Accuracy Heatmap")
plt.xlabel("Number of Estimators")
plt.ylabel("Max Depth")
plt.show()

pivot_cv = cv_results_df.pivot(index="max_depth", columns="n_estimators", values="mean_accuracy")
sns.heatmap(pivot_cv, annot=True, fmt=".3f", cmap="YlGnBu")
plt.title("Cross-Validation Mean Accuracy Heatmap")
plt.xlabel("Number of Estimators")
plt.ylabel("Max Depth")
plt.show()

plt.figure(figsize=(14, 6))
pivot_train = results_df.pivot(index="max_depth", columns="n_estimators", values="train_accuracy")
sns.heatmap(pivot_train, annot=True, fmt=".3f", cmap="YlGnBu")
plt.title("Train Accuracy Heatmap")
plt.xlabel("Number of Estimators")
plt.ylabel("Max Depth")
plt.show()

for (max_depth, n_estimators), cm in confusion_matrices.items():
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title(f"Confusion Matrix (Max Depth={max_depth}, Estimators={n_estimators})")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()

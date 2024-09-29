import pandas as pd
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

# Load datasets
train_data = pd.read_csv('train1.csv')
test_data = pd.read_csv('test1.csv')

# Fill missing values
train_data.fillna({'sex': 'Unknown', 'username': 'Unknown', 'name': 'Unknown', 'mail': 'Unknown'}, inplace=True)
test_data.fillna({'sex': 'Unknown', 'username': 'Unknown', 'name': 'Unknown', 'mail': 'Unknown'}, inplace=True)
numeric_columns = [col for col in train_data.columns if col.startswith('F_')]
train_data[numeric_columns] = train_data[numeric_columns].fillna(train_data[numeric_columns].mean())
test_data[numeric_columns] = test_data[numeric_columns].fillna(test_data[numeric_columns].mean())

# Label encode 'sex' and 'Age Group'
le = LabelEncoder()
train_data['sex'] = le.fit_transform(train_data['sex'])
test_data['sex'] = le.transform(test_data['sex'])
train_data['Age Group'] = le.fit_transform(train_data['Age Group'])

# Feature selection
X = train_data[numeric_columns + ['sex']]
y = train_data['Age Group']

# Initialize individual classifiers with hyperparameter grids
rf_param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
gb_param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}
svc_param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': ['scale', 'auto']
}

# Create individual classifiers with GridSearchCV for hyperparameter tuning
rf_clf = GridSearchCV(RandomForestClassifier(random_state=42), rf_param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
gb_clf = GridSearchCV(GradientBoostingClassifier(random_state=42), gb_param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
svc_clf = GridSearchCV(SVC(probability=True, random_state=42), svc_param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)

# Create a VotingClassifier
ensemble_clf = VotingClassifier(estimators=[
    ('rf', rf_clf), ('gb', gb_clf), ('svc', svc_clf)], voting='hard')

# Apply 5-fold cross-validation
print("Starting cross-validation...")
scores = cross_val_score(ensemble_clf, X, y, cv=5)

# Print average cross-validation accuracy
print("Average cross-validation accuracy before fitting:", scores.mean())

# Fit the model on the entire dataset after cross-validation
print("Fitting the model on the entire dataset...")
ensemble_clf.fit(X, y)

# Make predictions on the test set
print("Making predictions on the test set...")
test_predictions = ensemble_clf.predict(test_data[numeric_columns + ['sex']])

# Prepare submission
submission = pd.DataFrame({'id': test_data['id'], 'Age Group': le.inverse_transform(test_predictions)})
submission.to_csv('submission.csv', index=False)

# Optionally, print the best parameters for each classifier
print("Best parameters for Random Forest:", rf_clf.best_params_)
print("Best parameters for Gradient Boosting:", gb_clf.best_params_)
print("Best parameters for SVC:", svc_clf.best_params_)

print("Submission file created: submission.csv")
import pandas as pd
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

train_data = pd.read_csv('train1.csv')
test_data = pd.read_csv('test1.csv')

train_data.fillna({'sex': 'Unknown', 'username': 'Unknown', 'name': 'Unknown', 'mail': 'Unknown'}, inplace=True)
test_data.fillna({'sex': 'Unknown', 'username': 'Unknown', 'name': 'Unknown', 'mail': 'Unknown'}, inplace=True)
numeric_columns = [col for col in train_data.columns if col.startswith('F_')]
train_data[numeric_columns] = train_data[numeric_columns].fillna(train_data[numeric_columns].mean())
test_data[numeric_columns] = test_data[numeric_columns].fillna(test_data[numeric_columns].mean())

le = LabelEncoder()
train_data['sex'] = le.fit_transform(train_data['sex'])
test_data['sex'] = le.transform(test_data['sex'])
train_data['Age Group'] = le.fit_transform(train_data['Age Group'])

X = train_data[numeric_columns + ['sex']]
y = train_data['Age Group']

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

rf_clf = GridSearchCV(RandomForestClassifier(random_state=42), rf_param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
gb_clf = GridSearchCV(GradientBoostingClassifier(random_state=42), gb_param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
svc_clf = GridSearchCV(SVC(probability=True, random_state=42), svc_param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)

ensemble_clf = VotingClassifier(estimators=[
    ('rf', rf_clf), ('gb', gb_clf), ('svc', svc_clf)], voting='hard')

print("Starting cross-validation...")
scores = cross_val_score(ensemble_clf, X, y, cv=5)

print("Average cross-validation accuracy before fitting:", scores.mean())

print("Fitting the model on the entire dataset...")
ensemble_clf.fit(X, y)

print("Making predictions on the test set...")
test_predictions = ensemble_clf.predict(test_data[numeric_columns + ['sex']])

submission = pd.DataFrame({'id': test_data['id'], 'Age Group': le.inverse_transform(test_predictions)})
submission.to_csv('outputdataset.csv', index=False)

# Optional...
# print("Best parameters for Random Forest:", rf_clf.best_params_)
# print("Best parameters for Gradient Boosting:", gb_clf.best_params_)
# print("Best parameters for SVC:", svc_clf.best_params_)

print("Submission file created: outputdataset.csv")

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = pd.DataFrame({
    'online_hours': [5, 7, 2, 1, 6, 9, 12, 4, 8, 3],
    'clicks': [50, 200, 10, 5, 80, 150, 250, 60, 100, 40],
    'purchase_frequency': [1, 3, 0, 0, 2, 4, 5, 1, 2, 1],
    'activity_level': [2, 3, 1, 1, 2, 3, 3, 2, 2, 1],
    'age_group': ['Teen', 'Young Adult', 'Adult', 'Senior', 'Young Adult', 
                  'Young Adult', 'Teen', 'Adult', 'Young Adult', 'Senior']
})

X = data[['online_hours', 'clicks', 'purchase_frequency', 'activity_level']]
y = data['age_group']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

# Example: Predict age group for new users
new_users = pd.DataFrame({
    'online_hours': [5, 5, 9],
    'clicks': [50, 50, 0],
    'purchase_frequency': [1, 1, 0],
    'activity_level': [2, 2, 3]
})

predicted_age_groups = clf.predict(new_users)
print("Predicted age groups:", predicted_age_groups)

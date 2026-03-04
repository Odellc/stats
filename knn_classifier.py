from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split



y = churn_df["churn"].values
X = churn_df[["account_length", "customer_service_calls"]].values


#Function for model complexity and over/underfitting

def test_model(model, num_range, X_train, y_train, X_test, y_test):
    train_accuracies = {}
    test_accuracies = {}
    neighbors = np.arange(num_range[0], num_range[1])

    for neighbor in neighbors:
        knn = KNeighborsClassifier(n_neighbors=neighbor)
        knn.fit(X_train, y_train)
        train_accuracies[neighbor] = knn.score(X_train, y_train)
        test_accuracies[neighbor] = knn.score(X_test, y_test)
    return train_accuracies, test_accuracies

#Create a KNN classifier with 6 neighbrs
# Create a KNN classifier with 6 neighbors
knn = KNeighborsClassifier(n_neighbors=6)

# Fit the classifier to the data
knn.fit(X, y)

# Predict the labels for the X_new
y_pred = knn.predict(X_new)

# Print the predictions
print("Predictions: {}".format(y_pred)) 

accuracies = test_model(knn, [1,13], X_train, y_train, X_test, y_test)

# Import the module
from sklearn.model_selection import train_test_split

X = churn_df.drop("churn", axis=1).values
y = churn_df["churn"].values

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.20, random_state=42, stratify=y)
knn = KNeighborsClassifier(n_neighbors=5)

# Fit the classifier to the training data
knn.fit(X_train, y_train)

# Print the accuracy
print(knn.score(X_test, y_test))

# Create neighbors
neighbors = np.arange(1, 13)
train_accuracies = {}
test_accuracies = {}

for neighbor in neighbors:
  
	# Set up a KNN Classifier
	knn = KNeighborsClassifier(n_neighbors=neighbor)
  
	# Fit the model
	knn.fit(X_train, y_train)
  
	# Compute accuracy
	train_accuracies[neighbor] = knn.score(X_train, y_train)
	test_accuracies[neighbor] = knn.score(X_test, y_test)
print(neighbors, '\n', train_accuracies, '\n', test_accuracies)
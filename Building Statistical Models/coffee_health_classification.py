import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt 
from sklearn.preprocessing import StandardScaler


def main():
    data = pd.read_csv('C:/Users/codel/Desktop/Projects for GIT/Data/synthetic_coffee_health_10000.csv')
    
    print(data.head(5))

    #create a classification model to predict stress_level based on caffeine_mg and sleep_hours

    X = data[['Caffeine_mg', 'Sleep_Hours']].values
    y = data['Stress_Level'].values

    X_train, X_test, y_train, y_test   = train_test_split(X, y, test_size=.20, stratify=y, random_state=42 )

    # print(X_train[:5])

    scaler = StandardScaler()

    scaler.fit(X_train)

    X_train_scaled = scaler.transform(X_train)
    # print(scaler.transform(X_train)[:5])

    X_test_scaled = scaler.transform(X_test)

    train_accuracies = {}
    test_accuracies = {}

    n_range = np.arange(1, 26)
    
    for neighbor in n_range:
        
        knn = KNeighborsClassifier(n_neighbors=neighbor)
        knn.fit(X_train_scaled, y_train)

        train_accuracies[neighbor] = knn.score(X_train_scaled, y_train)
        test_accuracies[neighbor] = knn.score(X_test_scaled, y_test)
    

    plt.figure(figsize=(8,6))
    plt.title('KNN varying number of neighbors')
    plt.plot(n_range, list(train_accuracies.values()), label='Train Accuracy')
    plt.plot(n_range, list(test_accuracies.values()), label='Test Accuracy')
    plt.legend()
    plt.xlabel("Number of Neighbors")
    plt.ylabel('Accuracy')
    plt.show()




    


if __name__ == '__main__':
    main()
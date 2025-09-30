import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt 
from sklearn.preprocessing import StandardScaler
import sys

#Shap imports
import shap 


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

    best_model = {
        'model': '',
        'fitted_model' : '',
        'test_accuracy' : 0,
        'gap' : 0
        }
    
    
    for neighbor in n_range:
        
        knn = KNeighborsClassifier(n_neighbors=neighbor)
        knn.fit(X_train_scaled, y_train)

        train_accuracies[neighbor] = knn.score(X_train_scaled, y_train)
        test_accuracies[neighbor] = knn.score(X_test_scaled, y_test)

        if best_model['model'] == '' or best_model['test_accuracy'] <= knn.score(X_test_scaled, y_test):
            if (best_model['test_accuracy'] == test_accuracies[neighbor]) and (train_accuracies[neighbor] - test_accuracies[neighbor] >= best_model['gap']):
                continue
            
            best_model['model'] = knn
            best_model['fitted_model'] = best_model['model'].fit(X_train_scaled, y_train)
            best_model['test_accuracy'] = knn.score(X_test_scaled, y_test)
            best_model['gap'] = train_accuracies[neighbor] - test_accuracies[neighbor]
    
    print(best_model)

    plt.figure(figsize=(8,6))
    plt.title('KNN varying number of neighbors')
    plt.plot(n_range, list(train_accuracies.values()), label='Train Accuracy')
    plt.plot(n_range, list(test_accuracies.values()), label='Test Accuracy')
    plt.legend()
    plt.xlabel("Number of Neighbors")
    plt.ylabel('Accuracy')
    plt.show()

    # sys.exit()

    #Run model to determine shap
    # knn = KNeighborsClassifier(n_neighbors=13)
    # knn.fit(X_train_scaled, y_train)

    # print(X_train_scaled)

    explainer = shap.KernelExplainer(best_model['model'].predict_proba, X_train_scaled)
    shap_values = explainer.shap_values(X_test_scaled)

    print(type(shap_values))
    print(len(shap_values))
    print(shap_values.shape)
    print(shap_values[0].shape)
    print(shap_values[1].shape)

    # Choose class index (e.g., class 1)
    class_index = 1

    # Extract SHAP values for class 1
    shap_values_class1 = shap_values[:, :, class_index]  # shape: (2000, 2)

    col = ['Caffeine_mg', 'Sleep_Hours']

    # Plot
    shap.summary_plot(shap_values_class1, pd.DataFrame(X_test_scaled, columns=col))

    # shap.initjs()

    # shap.force_plot(explainer.expected_value, shap_values_class1[0], X_test_scaled[0], feature_names=col)
    shap.plots.force(explainer.expected_value[0], shap_values_class1[0], X_test_scaled[0], feature_names=col, matplotlib=True, show=True)

    explanation = shap.Explanation(
    values=shap_values_class1[0],
    base_values=explainer.expected_value[0],
    data=X_test_scaled[0],
    feature_names=col
    )

    # Now plot
    shap.plots.bar(explanation)
    shap.plots.waterfall(explanation)


    # shap.plots.bar(explainer.expected_value[0], shap_values_class1[0], X_test_scaled[0])

    # shap.plots.waterfall(explainer.expected_value[0], shap_values_class1[0], X_test_scaled[0])



if __name__ == '__main__':
    main()
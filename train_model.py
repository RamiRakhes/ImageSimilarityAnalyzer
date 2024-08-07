import json
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.linear_model import LogisticRegression

def load_search_results():
    with open('search_results.json', 'r') as f:
        data = json.load(f)
    return data['class_distribution']

def train_model(class_distribution):
    labels = list(class_distribution.keys())
    counts = list(class_distribution.values())
    
    X = np.array(counts).reshape(-1, 1)
    y = np.array(labels)
    
    model = LogisticRegression()
    model.fit(X, y)
    
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    return model

def plot_class_distribution(class_distribution):
    labels = list(class_distribution.keys())
    counts = list(class_distribution.values())

    plt.bar(labels, counts)
    plt.xlabel('Classe')
    plt.ylabel('Nombre de photos similaires')
    plt.title('Distribution des classes des photos similaires')
    plt.show()

if __name__ == '__main__':
    class_distribution = load_search_results()
    model = train_model(class_distribution)
    plot_class_distribution(class_distribution)

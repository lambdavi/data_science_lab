from collections import Counter

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


# --- CLASSES AND FUNCTIONS SECTION --
def find_differences(test, prediction):
    """
    Returns a list with in position 0 the correct classifications and in position 1 the wrong ones.
    """
    result = [0,0]
    for i in range(0, len(test)):
        if test[i]==prediction[i]:
            result[0]+=1
        else:
            result[1]+=1
    print(result)
    print(f"Accuracy: {result[0]/len(test)}")

class KNearestNeighbors:
    def __init__(self, k, distance_metric="euclidean"):
        self.k = k
        self.distance_metric = distance_metric

    def fit(self, X, y):
        """
        Store the 'prior knowledge' of you model that will be used
        to predict new labels.
        :param X : input data points, ndarray, shape = (R,C).
        :param y : input labels, ndarray, shape = (R,).
        """
        self.X_t = X.values
        self.Y_t = y.values

    def predict(self, X):
        """Run the KNN classification on X.
        :param X: input data points, ndarray, shape = (N,C).
        :return: labels : ndarray, shape = (N,).
        """
        predicted_labels = []
        for x in X:
            if self.distance_metric == "euclidean":
                predicted_labels.append(self.compute_euclidean(x))
            elif self.distance_metric == "cosine":
                predicted_labels.append(self.compute_cosine(x))
            elif self.distance_metric == "manhattan":
                predicted_labels.append(self.compute_manhattan(x))
        return predicted_labels

    def take_k(self, support_list):
        support_list.sort(key=lambda x: x[1])
        support_list=support_list[:self.k]
        new_labels = [self.Y_t[s[0]] for s in support_list]
        c = Counter(new_labels)
        return c.most_common(1)[0][0]

    def compute_euclidean(self, v):
        support_list = []
        for i, w in enumerate(self.X_t):            
            sum_sq = np.sum(np.square(v - w))
            support_list.append([i, np.sqrt(sum_sq)])
        return self.take_k(support_list)

    def compute_cosine(self, v):
        support_list = []
        for i, w in enumerate(self.X_t):            
            num = np.sum(np.multiply(v,w))
            denom_v = np.sum(v**2)**(1/2)
            denom_w = np.sum(w**2)**(1/2)
            denom = denom_v*denom_w
            support_list.append([i, 1 - num/denom])
        return self.take_k(support_list)

    def compute_manhattan(self, v):
        support_list = []
        for i, w in enumerate(self.X_t):            
            sum = np.sum(np.absolute(v - w))
            support_list.append([i, sum])
        return self.take_k(support_list)

    
# -- MAIN SECTION -- 
if __name__=="__main__":
    # Reading the dataset

    # MNIST dataset
    df = pd.read_csv(
        "https://raw.githubusercontent.com/dbdmg/data-science-lab/master/datasets/mnist_test.csv",
        header=None,
    )

    print(f"DF {df.shape}")
    # Splitting train and test dataframes with sample function of Pandas
    train = df.sample(frac=0.8,random_state=0)
    print(f"Train {train.shape}")
    test = df.drop(train.index)
    print(f"Test {test.shape}")


    # Splitting into X and Y the test/train dataframe
    X_train = train.iloc[: , 1:]
    print(f"X train {X_train.shape}")
    y_train = train[0]
    print(f"y_train {y_train.shape}")
    X_test = test.iloc[: , 1:]
    print(f"X test {X_test.shape}")
    y_test = test[0]
    print(f"y test {y_test.shape}")

    k = 4
    K_n_e = KNearestNeighbors(k, "euclidean")
    K_n_c = KNearestNeighbors(k, "cosine")
    K_n_m = KNearestNeighbors(k, "manhattan")

    K_n_e.fit(X_train, y_train)   
    K_n_c.fit(X_train, y_train)
    K_n_m.fit(X_train, y_train)

    print("COSINE")
    prediction = K_n_c.predict(X_test.values)
    #print(confusion_matrix(y_test.values, prediction))
    find_differences(y_test.values, prediction)
    print("EUCLIDEAN")
    prediction = K_n_e.predict(X_test.values)
    #print(confusion_matrix(y_test.values, prediction))
    find_differences(y_test.values, prediction)
    print("MANHATTAN")
    prediction = K_n_m.predict(X_test.values)
    find_differences(y_test.values, prediction)
    
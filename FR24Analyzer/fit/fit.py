import psycopg2
from .. import FR24Analyzer
import pandas as pd
from io import StringIO
import numpy as np

class Fit(object):
    def __init__(self, postgres_ip=None, postgres_port=None):
        self.__postgres_instance = FR24Analyzer.store.PostGreSQL()

    def __del__(self):
        return

    def __getDataFromDB(self):
        rows = self.__postgres_instance.getFromDB()
        dataDBCon = " lat, lon, hdg, alt, speed, duration, distance" + "\n\r"
        for row in rows:
            dataDB = str(row[1:]).replace("(","").replace(")","") + "\n\r"
            dataDBCon += dataDB
            dataDBCon.replace("(","").replace(")","")
        dataDB = StringIO(dataDBCon)
        datasets = pd.read_csv(dataDB, sep=",")
        return datasets
    
    def splitDataSet(self):
        datasets = self.__getDataFromDB()
        features = {"lat","lon","hdg","alt","speed","distance"}
        X = datasets.iloc[:, [0,1,2,3,4,6]].values
        Y = datasets.iloc[:, 5].values
        
        from sklearn.model_selection import train_test_split
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size = 0.08, random_state = 0)
        print("X_Test" + str(X_Test))
        print("Y_Test" + str(Y_Test))

        from sklearn.preprocessing import StandardScaler
        sc_X = StandardScaler()
        X_Train = sc_X.fit_transform(X_Train)
        X_Test = sc_X.transform(X_Test)

        from sklearn.ensemble import RandomForestRegressor
        regressor = RandomForestRegressor(n_estimators = 1000, max_depth=30, random_state = 0)
        regressor.fit(X_Train,Y_Train)

        Y_Pred = regressor.predict(X_Test)
        print("Y_Predict" + str(Y_Pred))


# # Random Forest Classifier

# # Importing the libraries

# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from FR24Analyzer import FR24Analyzer

# # Importing the datasets

# datasets = pd.read_csv('dataToIST.csv')

# X = datasets.iloc[:, [1,2,3,4,5,6]].values
# Y = datasets.iloc[:, 7].values
# features = {"lat","lon","hdg","alt","speed","distance"}

# # Splitting the dataset into the Training set and Test set

# from sklearn.model_selection import train_test_split
# X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size = 0.08, random_state = 0)
# print("X_Test" + str(X_Test))
# print("Y_Test" + str(Y_Test))


# # Feature Scaling

# from sklearn.preprocessing import StandardScaler
# sc_X = StandardScaler()
# X_Train = sc_X.fit_transform(X_Train)
# X_Test = sc_X.transform(X_Test)

# # Fitting the classifier into the Training set

# from sklearn.ensemble import RandomForestRegressor
# regressor = RandomForestRegressor(n_estimators = 1000, max_depth=30, random_state = 0)
# regressor.fit(X_Train,Y_Train)

# # Predicting the test set results

# Y_Pred = regressor.predict(X_Test)
# print("Y_Predict" + str(Y_Pred))

# #Calculating Feature Importances
# import pandas as pd
# feature_importances = pd.DataFrame(regressor.feature_importances_,
#                                    index = len(X_Train),
#                                    columns=['importance']).sort_values('importance',ascending=False)

# # Making the Confusion Matrix 

# # from sklearn.metrics import confusion_matrix
# # cm = confusion_matrix(Y_Test, Y_Pred)

# # # Visualising the Training set results

# # from matplotlib.colors import ListedColormap
# # X_Set, Y_Set = X_Train, Y_Train
# # X1, X2 = np.meshgrid(np.arange(start = X_Set[:, 0].min() - 1, stop = X_Set[:, 0].max() + 1, step = 0.01),
# #                      np.arange(start = X_Set[:, 1].min() - 1, stop = X_Set[:, 1].max() + 1, step = 0.01))
# # plt.contourf(X1, X2, regressor.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
# #              alpha = 0.75, cmap = ListedColormap(('red', 'green')))
# # plt.xlim(X1.min(), X1.max())
# # plt.ylim(X2.min(), X2.max())
# # for i, j in enumerate(np.unique(Y_Set)):
# #     plt.scatter(X_Set[Y_Set == j, 0], X_Set[Y_Set == j, 1],
# #                 c = ListedColormap(('red', 'green'))(i), label = j)
# # plt.title('Random Forest Classifier (Training set)')
# # plt.xlabel('Age')
# # plt.ylabel('Estimated Salary')
# # plt.legend()
# # plt.show()

# # # Visualising the Test set results

# # from matplotlib.colors import ListedColormap
# # X_Set, Y_Set = X_Test, Y_Test
# # X1, X2 = np.meshgrid(np.arange(start = X_Set[:, 0].min() - 1, stop = X_Set[:, 0].max() + 1, step = 0.01),
# #                      np.arange(start = X_Set[:, 1].min() - 1, stop = X_Set[:, 1].max() + 1, step = 0.01))
# # plt.contourf(X1, X2, regressor.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
# #              alpha = 0.75, cmap = ListedColormap(('red', 'green')))
# # plt.xlim(X1.min(), X1.max())
# # plt.ylim(X2.min(), X2.max())
# # for i, j in enumerate(np.unique(Y_Set)):
# #     plt.scatter(X_Set[Y_Set == j, 0], X_Set[Y_Set == j, 1],
# #                 c = ListedColormap(('red', 'green'))(i), label = j)
# # plt.title('Random Forest Classifier (Test set)')
# # plt.xlabel('Age')
# # plt.ylabel('Estimated Salary')
# # plt.legend()
# # plt.show()

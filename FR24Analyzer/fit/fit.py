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
        self.rows = self.__postgres_instance.getFromDB()
        dataDBCon = " flight, lat, lon, hdg, alt, speed, duration, distance" + "\n\r"
        for row in self.rows:
            dataDB = str(row[0:]).replace("(","").replace(")","") + "\n\r"
            dataDBCon += dataDB
            dataDBCon.replace("(","").replace(")","")
        dataDB = StringIO(dataDBCon)
        datasets = pd.read_csv(dataDB, sep=",")
        return datasets
    
    def __splitDataSet(self):
        datasets = self.__getDataFromDB()
        features = {"lat","lon","hdg","alt","speed","distance"}
        self.X = datasets.iloc[:, [1,2,3,4,5,7]].values
        self.Y = datasets.iloc[:, 6].values
    
    def __selectTrainTestRows(self):
        from sklearn.model_selection import train_test_split
        self.__splitDataSet()
        self.X_Train, self.X_Test, self.Y_Train, self.Y_Test = train_test_split(self.X, self.Y, test_size = 0.08, random_state = 0)

    def __standardizateData(self):
        from sklearn.preprocessing import StandardScaler
        sc_X = StandardScaler()
        self.__selectTrainTestRows()
        self.X_Train_Standardized = sc_X.fit_transform(self.X_Train)
        self.X_Test_Standardized = sc_X.transform(self.X_Test)

    def __returnTestFlight(self):
        length = len(self.rows)
        for i in range(length):
            if self.Y_Test[0] == self.rows[i][6]:
                return self.rows[i][0], self.rows[i][6]
        return

    def fitData(self):
        from sklearn.ensemble import RandomForestRegressor
        self.__standardizateData()
        regressor = RandomForestRegressor(n_estimators = 1000, max_depth=30, random_state = 0)
        regressor.fit(self.X_Train_Standardized, self.Y_Train)
        Y_Pred = regressor.predict(self.X_Test_Standardized)
        return self.__returnTestFlight()[0], str(self.__returnTestFlight()[1]), str(Y_Pred[0])




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

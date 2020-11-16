import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization

rawdata = pd.read_csv("FinalGrid_All_NN.csv")
preddata = pd.read_csv("FinalGrid_All_predict.csv")

X = rawdata.iloc[:,2:].values #13481 values x 4 bands (R,G,B,IR)
Y = rawdata.iloc[:,1:2].values #13481 values x 2 outputs (1=burnable, 2=not)

#Set seed for consitency of train/test split output
np.random.seed(123)
X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size = 0.2)

#Clear memory to train new network
tensorflow.keras.backend.clear_session()
#Define Neural network architecture
burnModel = Sequential()
burnModel.add(Dense(32, input_dim=4, activation='relu'))
burnModel.add(Dropout(0.6))
burnModel.add(Dense(64, activation='relu'))
burnModel.add(Dropout(0.4))
burnModel.add(Dense(32, activation='relu'))
burnModel.add(Dropout(0.2))
burnModel.add(Dense(16, activation='relu'))
burnModel.add(Dense(1, activation='sigmoid'))

#Compile and Train
burnModel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = burnModel.fit(X_train, y_train, epochs=100)

#Evaluate Train Accuracy
_,accuracy = burnModel.evaluate(X_train, y_train)
print('Train Accuracy: %.2f' % (accuracy*100))

#Evaluate Test Accuracy
_, accuracy = burnModel.evaluate(X_test, y_test)
print('Test Accuracy: %.2f' % (accuracy*100))

#TODO get clean data set of all input values
burn_x_pred = preddata.iloc[:,1:].values #17205 values x 4 bands (R,G,B,IR)
burn_y_pred = burnModel.predict(burn_x_pred)
print(burn_y_pred)
pd.DataFrame(burn_y_pred).to_csv('burnPredictions_YVals.csv')
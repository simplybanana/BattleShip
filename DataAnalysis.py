import csv
import pandas as pd
import math
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
import joblib
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Softmax
from keras.utils import np_utils, to_categorical
from keras.models import model_from_json


def distance_formula(column1,column2,row1,row2):
    dis = math.sqrt((column1-column2)**2 + (row1-row2)**2)
    return dis


def add_to_csv(fileName, dataToAdd, ColumnName):
    file = pd.read_csv(fileName)
    file[ColumnName] = dataToAdd
    file.to_csv(fileName, index=False)


def distance_away_center(fileName):
    column = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    data = []
    refcolumn = 4
    refrow = 4
    file = pd.read_csv(fileName)
    for y in range(0,5):
        data1 = []
        for x in range(0, len(file)):
            topcolumn = column[file.iloc[x,y][0]]
            toprow = int(file.iloc[x,y][1])
            distop = distance_formula(topcolumn,refcolumn,toprow,refrow)
            bottomcolumn = column[file.iloc[x,y][-3]]
            bottomrow = int(file.iloc[x,y][-2])
            disbot = distance_formula(bottomcolumn,refcolumn,bottomrow,refrow)
            avgrow = (disbot + distop)/2
            data1.append(avgrow)
        data1.append(0)
        data.append(data1)
    return data


def distance_away_from_each_other(fileName):
    column = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    data = []
    file = pd.read_csv(fileName)
    for x in range(0, len(file)):
        totdis = 0
        for i in range(0,4):
            topcolumn1 = column[file.iloc[x,i][0]]
            toprow1 = int(file.iloc[x,i][1])
            bottomcolumn1 = column[file.iloc[x,i][-3]]
            bottomrow1 = int(file.iloc[x,i][-2])
            for j in range(i+1,5):
                topcolumn2 = column[file.iloc[x,j][0]]
                toprow2 = int(file.iloc[x,j][1])
                distop = distance_formula(topcolumn1,topcolumn2,toprow1,toprow2)
                bottomcolumn2 = column[file.iloc[x,j][-3]]
                bottomrow2 = int(file.iloc[x,j][-2])
                disbot = distance_formula(bottomcolumn1,bottomcolumn2,bottomrow2,bottomrow1)
                avg = (distop+disbot)/2
                totdis += avg
        totdis = totdis/10
        data.append(totdis)
    data.append(0)
    return data


def fiveAbovefiveBelow(fileNames):
    for index in fileNames:
        file = pd.read_csv(index)
        data = []
        average = 100
        if index == "Data_Easy.csv":
            average = 60.2
        elif index == "Data_Medium.csv":
            average = 51.2
        elif index == "Data_Master.csv":
            average = 47.1
        for i in range(0,len(file.iloc[:,5])):
            if int(file.iloc[i,5]) > average + 5:
                data.append("High")
            elif average + 5 >= int(file.iloc[i,5]) >= average - 5:
                data.append('Average')
            else:
                data.append('Low')
        add_to_csv(index, data, "Above Average Cat")


def fiveAboveAverage(fileNames):
    for index in fileNames:
        file = pd.read_csv(index)
        data = []
        average = 100
        if index == "Data_Easy.csv":
            average = 60.2
        elif index == "Data_Medium.csv":
            average = 51.2
        elif index == "Data_Master.csv":
            average = 47.1
        for i in range(0,len(file.iloc[:,5])):
            if int(file.iloc[i,5]) > average + 5:
                data.append(1)
            else:
                data.append(0)
        add_to_csv(index, data, "Above Average")


def average_turns(fileNames):
    for index in fileNames:
        file = pd.read_csv(index)
        data = sum(file.iloc[:,5])/len(file.iloc[:,5])
        datalist = [data]*len(file.iloc[:,5])
        add_to_csv(index,datalist,"Average Turns")


def baseline_error(filesNames):
    total_turn = 0
    for index in filesNames:
        file = pd.read_csv(index)
        total_turn += file.iloc[1,12]
    average_turn = total_turn/len(filesNames)
    return average_turn


def preprocess(x,y):
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=.2, random_state=2)
    labelencoder1 = LabelEncoder()
    labelencoder12 = LabelEncoder()
    ytrain = labelencoder1.fit_transform(ytrain)
    ytest = labelencoder1.transform(ytest)
    ytrain = ytrain.reshape(-1, 1)
    ytest = ytest.reshape(-1, 1)
    onehot = OneHotEncoder()
    ytrain = onehot.fit_transform(ytrain).toarray()
    ytest = onehot.transform(ytest).toarray()
    return xtrain, xtest, ytrain, ytest


def KNearest(xtrain_opt, xtest_opt, ytrain_opt, ytest_opt):
    classifier = KNeighborsClassifier(n_neighbors=3, metric='minkowski', p=2)
    classifier.fit(xtrain_opt, ytrain_opt)
    ypred = classifier.predict(xtest_opt)
    print(classification_report(ytest_opt,ypred))


def LRegression(xtrain_opt, xtest_opt, ytrain_opt, ytest_opt):
    classifier = LogisticRegression(random_state=0,solver='newton-cg',multi_class='multinomial')
    classifier.fit(xtrain_opt, ytrain_opt)
    ypred = classifier.predict(xtest_opt)
    print(classification_report(ytest_opt, ypred))


def ann(xtrain_opt, xtest_opt, ytrain_opt, ytest_opt):
    classifier = Sequential()
    classifier.add(Dense(activation='relu', input_dim=6, units=6, kernel_initializer='uniform'))
    classifier.add(Dense(activation='relu', units=6, kernel_initializer='uniform'))
    classifier.add(Dense(activation='relu', units=6, kernel_initializer='uniform'))
    classifier.add(Dense(activation='softmax', input_dim=6, units=3, kernel_initializer='uniform'))
    classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    classifier.fit(xtrain_opt, ytrain_opt, batch_size=60000, nb_epoch=400)
    ypred = classifier.predict(xtest_opt)
    ypred = np.argmax(ypred, axis=1)
    print(classification_report(ytest_opt,ypred))


def evaluate(ytest,ypred,baseline):
    baselineerrors = np.nanmean(abs(ytest - baseline))
    modelerrors = np.nanmean(abs(ytest - ypred))
    print("Average Baseline Error: ", baselineerrors)
    print("Average Model Error: ", modelerrors)


if __name__ == "__main__":
    files = ['Data_Easy.csv', 'Data_Medium.csv', 'Data_Master.csv']
    columnNames = ['5 Distance away', '4 Distance Away', '3 Distance Away', '3.1 Distance Away', '2 Distance Away', 'Distance from Others']
    file1 = pd.read_csv('Data_Easy.csv')
    file2 = pd.read_csv('Data_Medium.csv')
    file3 = pd.read_csv('Data_Master.csv')
    x1 = file1.iloc[:, [6, 7, 8, 9, 10, 11]].values
    x2 = file2.iloc[:, [6, 7, 8, 9, 10, 11]].values
    x = np.concatenate((x1, x2), axis=0)
    x3 = file3.iloc[:, [6, 7, 8, 9, 10, 11]].values
    x = np.concatenate((x, x3), axis=0)
    y1 = file1.iloc[:, 14].values
    y2 = file2.iloc[:, 14].values
    y = np.concatenate((y1, y2), axis=0)
    y3 = file3.iloc[:, 14].values
    y = np.concatenate((y, y3), axis=0)
    xtrain, xtest, ytrain, ytest = preprocess(x, y)
    ytest = np.argmax(ytest, axis=1)
    #KNearest(xtrain,xtest,ytrain,ytest)
    #LRegression(xtrain,xtest,ytrain,ytest)
    ann(xtrain,xtest,ytrain,ytest)
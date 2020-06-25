import pandas as pd
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.pipeline import make_pipeline
import joblib
import statsmodels.api as sm


file = pd.read_csv('TestCSV.csv')
x = file.iloc[:, [0, 1, 2, 3, 4, 5]].values
print(x)
x = preprocessing.scale(x)
print(x)

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1] * 100))

"""file = pd.read_csv('TestCSV.csv')
print(file.iloc[3,0][-1])"""
"""file = pd.read_csv('TestCSV.csv')
file.iloc[1,1] = 9
file.to_csv('TestCSV.csv',index=False)
print(file.iloc[1,1])"""
"""file = pd.read_csv('TestCSV.csv')
x = file.iloc[:, [0, 1, 2, 3, 4, 5]].values
y = file.iloc[:, 6].values
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=.2, random_state=0)
epsillon = np.array([1, 1])
i = 1
model = 0
while np.all(epsillon > .1) or i > 6:
    model = make_pipeline(PolynomialFeatures(i), linear_model.Ridge())
    model.fit(xtrain, ytrain)
    ypred = model.predict(xtest)
    epsillon = abs(ypred - ytest)
    i += 1"""

"""x1 = np.arange(100)
x2 = np.arange(100)
x3 = np.arange(100)
x4 = np.arange(100)
np.random.shuffle(x1)
np.random.shuffle(x2)
np.random.shuffle(x3)
np.random.shuffle(x4)
y = 3 + 2*x1 + 3*x2**3 + x3 + x4**2 + np.random.rand(100)
x = np.array([x1,x2,x3,x4]).T
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=.3,random_state=0)


sl = .05
poly_feats = PolynomialFeatures(degree=3)
s_poly = poly_feats.fit_transform(xtrain)
q = []
for i in range(0,np.shape(s_poly)[1]):
    q.append(i)
s_opt = s_poly[:, q]
regressor_ols = sm.OLS(endog=ytrain, exog=s_opt).fit()
ypred = regressor_ols.predict(s_opt)
if np.any(abs(ypred-ytrain) < .01):
    print('good enough')
else:
    print('too bad')
    
while True:
    regressor_ols = sm.OLS(endog=ytrain, exog=s_opt).fit()
    if np.all(regressor_ols.pvalues < sl):
        joblib_file = "test12.pkl"
        joblib.dump(regressor_ols, joblib_file)
        break
    else:
        q.pop(np.where(regressor_ols.pvalues == max(regressor_ols.pvalues))[0][0])
        s_opt = s_poly[:, q]



x9 = np.array([[1,2,3,4]])
y = 3 + 2*x9[0][0] + 3*x9[0][1]**3 + x9[0][2] + x9[0][3]**2 + np.random.rand(1)
print(y)
test_poly = poly_feats.fit_transform(x9)
test_opt = test_poly[:,q]
ypred = regressor_ols.predict(test_opt)
print(ypred)
print(regressor_ols.summary())
with open('test12.txt','w') as filehandle:
    filehandle.writelines("%s\n"%place for place in q)"""


"""
q = []
with open('test12.txt','r') as filehandle:
    filecontents = filehandle.readlines()
    for file in filecontents:
        current = int(file[:-1])
        q.append(current)

joblib_file = "test12.pkl"
joblib_model = joblib.load(joblib_file)
x9 = np.array([[1,2,3,4]])
poly_feats = PolynomialFeatures(degree=3)
s_poly = poly_feats.fit_transform(x9)
s_opt = s_poly[:,q]
ypred = joblib_model.predict(s_opt)
print(ypred)"""


#print(np.where(regressor_ols.pvalues == max(regressor_ols.pvalues)))
#print(np.where(regressor_ols.pvalues == max(regressor_ols.pvalues))[0])
#print(np.where(regressor_ols.pvalues == max(regressor_ols.pvalues))[0][0])



"""xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=.2,random_state=0)
model = make_pipeline(PolynomialFeatures(4),linear_model.Ridge())
model.fit(xtrain,ytrain)
ypred = model.predict(xtest)
#print(xtest)
print(ytest)
print(ypred)
print(sum(ytest-ypred)/len(ytest))"""
#print(linear_model.LinearRegression().fit(np.array([x1,x2,x3,x4]).T,y).coef_)



"""q = []
for i in range(0,file.shape[1]-1):
    q.append(i)
x = file.iloc[:, q].values
y = file.iloc[:, file.shape[1]-1].values
Xtrain, Xtest, ytrain, ytest = train_test_split(x, y, test_size=.2, random_state=0)
x = np.append(arr=np.ones((len(x),1)).astype(int),values=x, axis=1)
q.append(file.shape[1]-1)
xopt = x[:,q]
regressor_ols = sm.OLS(endog=y,exog=xopt).fit()
print(regressor_ols.summary())
print(type(regressor_ols.pvalues))
q.remove(np.where(regressor_ols.pvalues == max(regressor_ols.pvalues))[0])"""



"""xopt = x[:, q]
regressor_ols = sm.OLS(endog=y,exog=xopt).fit()
joblib_file = "testfile.pkl"
joblib.dump(regressor_ols,joblib_file)
print(regressor_ols.summary())
joblib_file = "testfile.pkl"
joblib_model = joblib.load(joblib_file)
#score = joblib_model.score(Xtest,ytest)
ypredict = joblib_model.predict([1,2,3])
print(ypredict)"""



"""regressor = LinearRegression()
regressor.fit(Xtrain, ytrain)
ypred = regressor.predict(Xtest)"""
#reg = linear_model.RidgeCV(alphas=np.linspace(.1, 1, 10))
#reg.fit(Xtest, ytest)
#ypred = reg.predict(Xtest)
"""epsillon = np.array([1,1])
i = 1
ypred = 0
while np.all(epsillon > .1):
    model = make_pipeline(PolynomialFeatures(i),linear_model.Ridge())
    model.fit(Xtrain,ytrain)
    ypred = model.predict(Xtest)
    epsillon = abs(ypred-ytest)
    i += 1"""


"""model = make_pipeline(PolynomialFeatures(1),linear_model.Ridge())
model.fit(Xtrain,ytrain)
ypred = model.predict(Xtest)
epsillon = abs(ypred-ytest)
if np.any(epsillon < .1):
    print('yeehaw')"""



"""print(Xtest)
print(ypred)
print(ytest)
print(epsillon)"""
#print(i)
#print(np.where(x == Xtest[1]))

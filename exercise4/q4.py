import sys
import numpy as np
from sklearn import preprocessing
from sklearn import cross_validation

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
 
 
if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print "error: use python ml.py x_train.np y_train.np x_test.np"
  
    x_train = np.loadtxt(sys.argv[1])
    y_train = np.loadtxt(sys.argv[2])
    x_test = np.loadtxt(sys.argv[3])



#Function for 10-fold Cross Validation
def KFold(X_data,X_target):
    kf = cross_validation.KFold(len(X_data), n_folds=10,shuffle=False)
    for train_index, test_index in kf:
        cv_xtrain,cv_xtest = X_data[train_index], X_data[test_index]
        cv_ytrain,cv_ytest = X_target[train_index],X_target[test_index]
        return cv_xtrain,cv_ytrain,cv_xtest,cv_ytest

#Performing 10-fold CV
cv_xtrain, cv_ytrain, cv_xtest, cv_ytest = KFold(x_train, y_train)
#Pipeline with preprocessing and Random Forest
pipeline = Pipeline([
                    ("Scale", preprocessing.MinMaxScaler()),
                    ("RD", RandomForestClassifier(n_estimators=100,
                                                  max_depth=20,
                                                 class_weight = {0:1,1:2}
                                                 ))
                    ]
                   )

predictions_train = pipeline.fit_transform(cv_xtrain,cv_ytrain)#.predict(X)
predictions_train = pipeline.predict(cv_xtrain)
predictions = pipeline.predict(cv_xtest)
np.savetxt("y_test.np",predictions,"%d")
print "Output written to \"y_test.np\""
#score = pipeline.score(cv_xtest, cv_ytest)
#print score


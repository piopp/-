import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm
import pandas as pd

file_path = 'dongyangyisheng03012final1.xlsx'

df = pd.read_excel(file_path)
n = 59
it = [4,5,6,7,11,17,25,33,38,44,47,54,57]
X = df.iloc[:, it]
y = df.iloc[:, n]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=17, shuffle=True)

clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)

print(clf.score(X_test, y_test))
#17
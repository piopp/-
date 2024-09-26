import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from joblib import dump, load

db_config = {
    'host': 'localhost',  # 数据库主机地址
    'user': 'root',  # 数据库用户名
    'password': 'chenyufeng',  # 数据库密码
    'database': 'hospital',  # 数据库名
    'charset': 'utf8mb4'  # 字符编码
}

conn = pymysql.connect(**db_config)

try:
    with conn.cursor() as cursor:
        sql = "SELECT * FROM sample"
        cursor.execute(sql)
        result = cursor.fetchall()

        columns = [i[0] for i in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        n = df.shape[1]
        X = df.iloc[:, 1:n - 2]
        y = df.iloc[:, n-1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=17, shuffle=True)

        clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)

        dump(clf, '../predict.joblib')
        print(clf.score(X_test, y_test))
finally:
    conn.close()
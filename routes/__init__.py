import secrets

from flask import *
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__,template_folder='../templates',static_folder='../static')
CORS(app)
# 配置数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chenyufeng'
app.config['MYSQL_DB'] = 'hospital'
mysql = MySQL(app)
app.secret_key = secrets.token_hex(16)

from routes import login_route
from routes import register_route
from routes import home_route
from routes import user_route
from routes import patient_route
from routes import role_route
from routes import sample_route
from routes import predict_route
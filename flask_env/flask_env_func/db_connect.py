from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql

from io import BytesIO



db = SQLAlchemy()

conn = pymysql.connect(host='127.0.0.1', user='root',
        password='ekdldksk', database='testdb',
        port=3306,charset='utf8')

cursor = conn.cursor()

buffer = BytesIO()
engine = create_engine('mysql+pymysql://root:ekdldksk@localhost:3306/testdb', echo=False)

def db_connector():
    sql = '''SELECT * FROM testdb.member'''

    cursor.execute(sql)
    result = cursor.fetchall()

    conn.close()
    return str(result)

def Mask_CSV():
    mask = '''SELECT * FROM testdb.mask'''

    cursor.execute(mask)
    r = cursor.fetchall()

    conn.close()
    return r

from flask_sqlalchemy import SQLAlchemy
import pymysql
from io import BytesIO
from sqlalchemy import create_engine

db = SQLAlchemy()

conn = pymysql.connect(host='0.0.0.0', user='root', password='3-[z>g9UNk[f-X&EKdW&',
                       database='try_mysql', port=3306, charset='utf8')
cursor = conn.cursor()

# 이미지 저장하기
buffer = BytesIO()

# 이미지 불러오기
engine = create_engine(
    'mysql+pymysql://root:3-[z>g9UNk[f-X&EKdW&@localhost:3306/try_mysql', echo=False)

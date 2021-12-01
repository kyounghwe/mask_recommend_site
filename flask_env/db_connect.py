from flask_sqlalchemy import SQLAlchemy
import pymysql
from io import BytesIO
from sqlalchemy import create_engine

db = SQLAlchemy()

conn = pymysql.connect(host='ec2-54-180-30-125.ap-northeast-2.compute.amazonaws.com', user='root', password='5452tulahyo12!A', database='try_mysql', port=3306, charset='utf8')
cursor = conn.cursor()

# 이미지 저장하기
buffer = BytesIO()

# 이미지 불러오기
engine = create_engine('mysql+pymysql://root:5452tulahyo12!A@localhost:3306/try_mysql', echo=False)

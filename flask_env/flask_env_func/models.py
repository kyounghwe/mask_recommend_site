from db_connect import db

#이미지 저장
class review(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100),nullable=False)
    goods_id = db.Column(db.String(800),nullable=False)
    star = db.Column(db.Float,nullable=False)
    r_data = db.Column(db.Text,nullable=False)
    r_op1 = db.Column(db.String(100),nullable=False)
    r_op2 = db.Column(db.String(100),nullable=False)
    r_op3 = db.Column(db.String(100),nullable=False)
    r_op4 =db.Column(db.String(100),nullable=False)
    img_data = db.Column(db.String(800),nullable=False)
    def __init__(self, user_id, goods_id,star,r_data,r_op1,r_op2,r_op3,r_op4,img_data):
        self.user_id = user_id
        self.goods_id = goods_id
        self.star = star
        self.r_data = r_data
        self.r_op1 = r_op1
        self.r_op2 = r_op2
        self.r_op3 = r_op3
        self.r_op4 = r_op4
        self.img_data = img_data

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    user_pw = db.Column(db.String(80), nullable=False)
    user_gender = db.Column(db.String(80), nullable=False)
    user_age = db.Column(db.String(80), nullable=False)
    user_job = db.Column(db.String(80), nullable=False)


    def __init__(self, user_id, user_pw,user_gender,user_age,user_job):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_gender = user_gender
        self.user_age = user_age
        self.user_job = user_job

class Zzim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    goods_id = db.Column(db.String(80), nullable=False)

    def __init__(self, user_id, goods_id):
        self.user_id = user_id
        self.goods_id = goods_id

''''''




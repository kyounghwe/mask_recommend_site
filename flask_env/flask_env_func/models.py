from db_connect import db





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

class mask(db.Model):
    m_id = db.Column(db.Integer, primary_key=True)
    m_name = db.Column(db.String(100), nullable=False)
    m_riv = db.Column(db.Integer, nullable=False)
    m_rat = db.Column(db.Float, nullable=False)
    m_pri = db.Column(db.Integer, nullable=False)
    m_cate = db.Column(db.String(80), nullable=False)
    m_img = db.Column(db.String(300), nullable=False)

    def __init__(self, m_name, m_riv,m_rat,m_pri,m_cate,m_img):
        self.m_name = m_name
        self.m_riv = m_riv
        self.m_rat = m_rat
        self.m_pri = m_pri
        self.m_cate = m_cate
        self.m_img = m_img

class Review(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_user = db.Column(db.String(20), nullable=False)
    r_goods = db.Column(db.String(100), nullable=False)
    r_star = db.Column(db.Float, nullable=False)
    r_op1 = db.Column(db.String(90), nullable=False)
    r_op2 = db.Column(db.String(90), nullable=False)
    r_op3 = db.Column(db.String(90), nullable=False)
    r_op4 = db.Column(db.String(90), nullable=False)

    def __init__(self, r_user, r_goods,r_star,r_op1,r_op2,r_op3,r_op4):
        self.r_user = r_user
        self.r_goods = r_goods
        self.r_star = r_star
        self.r_op1 = r_op1
        self.r_op2 = r_op2
        self.r_op3 = r_op3
        self.r_op4 = r_op4






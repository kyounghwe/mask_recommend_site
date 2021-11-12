from db_connect import db

class tb_user_info(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False, unique=True)
    user_pw = db.Column(db.String(20), nullable=False)
    user_gender = db.Column(db.String(20), nullable=False)
    user_age = db.Column(db.String(20), nullable=False)
    user_job = db.Column(db.String(20), nullable=False)
    
    def __init__(self, user_id, user_pw, user_gender, user_age, user_job):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_gender = user_gender
        self.user_age = user_age
        self.user_job = user_job
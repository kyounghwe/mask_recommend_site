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

class tb_mask_info(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True)
    mask_name = db.Column(db.String(50), nullable=False)
    mask_review_num = db.Column(db.Integer, nullable=False)
    mask_star_rating = db.Column(db.Float, nullable=False)
    mask_price = db.Column(db.Integer, nullable=False)
    mask_category = db.Column(db.String(20), nullable=False)
    mask_blocking_grade = db.Column(db.String(20), nullable=False)
    mask_function = db.Column(db.String(80))
    mask_img = db.Column(db.String(100))

    def __init__(self, mask_name, mask_review_num, mask_star_rating, mask_price, mask_category, mask_blocking_grade, mask_function, mask_img):
        self.mask_name = mask_name
        self.mask_review_num = mask_review_num
        self.mask_star_rating = mask_star_rating
        self.mask_price = mask_price
        self.mask_category = mask_category
        self.mask_blocking_grade = mask_blocking_grade
        self.mask_function = mask_function
        self.mask_img = mask_img
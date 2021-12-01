from db_connect import db

class tb_user_info(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

class tb_admin_info(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.String(20), nullable=False, unique=True)
    admin_pw = db.Column(db.String(20), nullable=False)
    
    def __init__(self, admin_id, admin_pw):
        self.admin_id = admin_id
        self.admin_pw = admin_pw

class tb_mask_data(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mask_name = db.Column(db.String(50), nullable=False)
    mask_review_num = db.Column(db.Integer, nullable=False)
    mask_star_rating = db.Column(db.Float, nullable=False)
    mask_price = db.Column(db.Integer, nullable=False)
    mask_category = db.Column(db.String(20), nullable=False)
    mask_blocking_grade = db.Column(db.String(20), nullable=False)
    mask_function = db.Column(db.String(80), nullable=False)
    mask_img_link = db.Column(db.String(300), nullable=False)
    mask_purchase_link = db.Column(db.String(2000), nullable=False)

    def __init__(self, mask_name, mask_review_num, mask_star_rating, mask_price, mask_category, mask_blocking_grade, mask_function, mask_img_link, mask_purchase_link):
        self.mask_name = mask_name
        self.mask_review_num = mask_review_num
        self.mask_star_rating = mask_star_rating
        self.mask_price = mask_price
        self.mask_category = mask_category
        self.mask_blocking_grade = mask_blocking_grade
        self.mask_function = mask_function
        self.mask_img_link = mask_img_link
        self.mask_purchase_link = mask_purchase_link

class tb_review(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mask_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    star_rating = db.Column(db.Float, nullable=False)
    review_text = db.Column(db.String, nullable=False)
    option1 = db.Column(db.Integer, nullable=False)
    option2 = db.Column(db.Integer, nullable=False)
    option3 = db.Column(db.Integer, nullable=False)
    option4 = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(800), nullable=False)

    def __init__(self, mask_id, user_id, star_rating, review_text, option1, option2, option3, option4, img):
        self.mask_id = mask_id
        self.user_id = user_id
        self.star_rating = star_rating
        self.review_text = review_text
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.img = img

class tb_zzim(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mask_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, mask_id, user_id):
        self.mask_id = mask_id
        self.user_id = user_id

class tb_review_keyword(db.Model):
    pk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option1 = db.Column(db.Float, nullable=False)
    option2 = db.Column(db.Float, nullable=False)
    option3 = db.Column(db.Float, nullable=False)
    option4 = db.Column(db.Float, nullable=False)
    option5 = db.Column(db.Float, nullable=False)

    def __init__(self, option1, option2, option3, option4, option5):
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.option5 = option5
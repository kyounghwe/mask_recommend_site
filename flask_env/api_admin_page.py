''' api_admin_page.py
관리자 관련 페이지
관리자로그인페이지, 관리자페이지 '''
from flask import Blueprint, render_template, request, redirect, url_for, session
from read_mysql_for_admin import order_by_review_num, order_by_star_rating_review_num
from models import tb_admin_info, tb_user_info
from db_connect import db

admin_page = Blueprint('admin_page', __name__)

@admin_page.route('/admin_login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login_admin.html')
    else:  # 로그인 정보 입력
        admin_id = request.form['admin_id']
        admin_pw = request.form['admin_pw']
        session['logged_in'] = False
        if admin_id == None or admin_pw == None:
            errMsg_admin = '아이디와 비밀번호를 입력해주세요'
        try:
            admin = tb_admin_info.query.filter(tb_admin_info.admin_id == admin_id).all()  # 아이디 비교
            if admin:  # 아이디 존재할 때
                admin = tb_admin_info.query.filter(tb_admin_info.admin_pw == admin_pw).first()  # 비밀번호 비교
                if admin:  # 아이디, 비밀번호 일치 -> 로그인 성공
                    session['logged_in'] = True
                    # session['admin_id'] = admin_id
                    session['check'] = 2
                    return redirect(url_for('user.home'))
                else:  # 아이디, 비밀번호 불일치
                    errMsg_admin = '아이디 또는 비밀번호가 틀렸습니다'
            else: # 아이디 없을 때
                errMsg_admin = '아이디 또는 비밀번호가 틀렸습니다'
        except:
            errMsg_admin = '로그인에 실패하였습니다'
        return render_template('login_admin.html', errMsg_admin=errMsg_admin)

@admin_page.route("/admin_page")
def page():
    # 리뷰수 내림차순 10개
    order_by_review_num_list = order_by_review_num()
    review_num_list = []
    for i in order_by_review_num_list:
        review_num_list.append(i[2])
    
    # 평점 + 리뷰수(x0.00005) 내림차순 20개
    order_by_star_rating_review_num_list = order_by_star_rating_review_num()
    sr_star_rating_list = []
    sr_review_num_list = []
    for i in order_by_star_rating_review_num_list:
        sr_star_rating_list.append(i[2])
        sr_review_num_list.append(i[3])
    
    # 유저 분포 (성별, 연령대, 직업)
    user_gender_count = [
            len(tb_user_info.query.filter(tb_user_info.user_gender == 'female').all()),
            len(tb_user_info.query.filter(tb_user_info.user_gender == 'male').all())
        ]
    
    user_age_count = [
            len(tb_user_info.query.filter(tb_user_info.user_age == '00s').all()),
            len(tb_user_info.query.filter(tb_user_info.user_age == '10s').all()),
            len(tb_user_info.query.filter(tb_user_info.user_age == '20s').all()),
            len(tb_user_info.query.filter(tb_user_info.user_age == '30s').all()),
            len(tb_user_info.query.filter(tb_user_info.user_age == '40s').all()),
            len(tb_user_info.query.filter(tb_user_info.user_age == '50s').all()),
            len(tb_user_info.query.filter(tb_user_info.user_age == '60s').all()),
            len(tb_user_info.query.filter(tb_user_info.user_age == '70s').all())
        ]
    
    user_job_count = [
            len(tb_user_info.query.filter(tb_user_info.user_job == 'salaryman').all()),
            len(tb_user_info.query.filter(tb_user_info.user_job == 'housewife').all()),
            len(tb_user_info.query.filter(tb_user_info.user_job == 'student').all()),
            len(tb_user_info.query.filter(tb_user_info.user_job == 'self-employed').all()),
            len(tb_user_info.query.filter(tb_user_info.user_job == 'public officials').all()),
            len(tb_user_info.query.filter(tb_user_info.user_job == 'specialized').all()),
            len(tb_user_info.query.filter(tb_user_info.user_job == 'No-Job').all()),
            len(tb_user_info.query.filter(tb_user_info.user_job == 'etc').all())
        ]
    return render_template('admin_page.html', 
            order_by_review_num_list=order_by_review_num_list, review_num_list=review_num_list, 
            order_by_star_rating_review_num_list=order_by_star_rating_review_num_list, sr_star_rating_list=sr_star_rating_list, sr_review_num_list=sr_review_num_list,
            user_gender_count=user_gender_count, user_age_count=user_age_count, user_job_count=user_job_count
        )
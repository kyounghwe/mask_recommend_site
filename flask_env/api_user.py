''' api_user.py

메인 / 회원가입 / 로그인 / 로그아웃 '''
from flask import Blueprint, render_template, request, redirect, url_for, session
from models import tb_user_info
from db_connect import db
from read_mysql import read_mask_data
from read_mysql_select import select_category, save_selected_category, get_selected_category
import json

user = Blueprint('user', __name__)

# 메인 페이지
@user.route('/', methods=["GET", "POST"])
def home():
    # 로그인 여부 확인
    if not session.get('logged_in'): session['check'] = 0
    # else: check = 1  # 로그인 된 신호를 프론트에 줘야 함 -> 로그인 해야 리뷰, 별점, 찜 등의 기능 이용 가능

    data = get_selected_category()
    if data == ():
        mask_category = ''
        mask_blocking_grade = ''
        mask_function = ['','','','','','','','']
        mask_price = ['','']
    else:
        mask_category = data[0][0]
        mask_blocking_grade = data[0][1]
        mask_function = [data[0][2],data[0][3],data[0][4],data[0][5],data[0][6],data[0][7],data[0][8],data[0][9]]
        try: 
            mask_price = list(map(int, data[0][10].split(":")))
        except:
            mask_price = ['','']

    # 선택한 카테고리가 있는 경우
    checked_list = [mask_category, mask_blocking_grade, mask_function, mask_price]
    if checked_list != ['', '', ['','','','','','','',''], ['','']]:
        mask_list = select_category(checked_list)
        checked_list_for_html = []
        for i in checked_list[:-1]:
            if not i:
                continue
            if type(i) is list:
                for j in i:
                    if j:
                        checked_list_for_html.append(j)
            else:
                checked_list_for_html.append(i)
        if checked_list[-1] != ['','']:
            checked_list_for_html += checked_list[-1]
            if checked_list_for_html[-1] == '999999999':
                temp = "20000원 이상"
            else:
                temp = " ~ ".join(list(map(str, checked_list_for_html[-2:]))) + '원'
            checked_list_for_html = checked_list_for_html[:-2]
            checked_list_for_html.append(temp)
    else:  # 없는 경우
        checked_list = None
        checked_list_for_html = None
        mask_list = read_mask_data()
    
    # 페이징
    page = request.args.get('page')
    if page != None:
        page = int(page)
        if session['page_num'] - page == 1 and session['page_num'] > 0:  # prev페이지로 갈 때
            session['page_num'] -= 1
        elif session['page_num'] - page == -1 and session['page_num'] < len(mask_list)//16:  # next페이지로 갈 때
            session['page_num'] += 1
    else:
        session['page_num'] = 0
    mask_list = mask_list[session['page_num']*16:session['page_num']*16 + 16]
    
    return render_template("main.html", check=session['check'], mask_list=mask_list, page_num=session['page_num'], checked_list=checked_list_for_html)

# 카테고리 선택
@user.route('/category', methods=["GET","POST"])
def category():
    if request.method == "POST":
        try:
            category_data = request.get_json("server_data")
            mask_category = ['' if category_data['mask_category'] == 'None' else category_data['mask_category']][0]
            mask_blocking_grade = ['' if category_data['mask_blocking_grade'] == 'None' else category_data['mask_blocking_grade']][0]
            mask_function = [['','','','','','','',''] if category_data['mask_function'] == ['None','None','None','None','None','None','None','None'] else category_data['mask_function']][0]
            for i in range(8):
                if mask_function[i] == 'None':
                    mask_function[i] = ''
            mask_price = ['' if category_data['mask_price'] == 'None' else category_data['mask_price']][0]
        except:
            mask_category = ''
            mask_blocking_grade = ''
            mask_function = ['', '', '', '', '', '', '', '']
            mask_price = ''
        data = [mask_category, mask_blocking_grade, mask_function, mask_price]
        save_selected_category(data)
        return json.dumps({"mask_category":mask_category, "mask_blocking_grade":mask_blocking_grade, "mask_function":mask_function, "mask_price":mask_price})
    else:
        return 'hello'

# 회원가입 페이지
### 아이디와 비밀번호 조건 추가해야 함 -> 조건에 맞지 않으면 alert
### 비밀번호 저장할 때 암호화해서 집어넣기
@user.route('/join', methods=["GET", "POST"])
def join():
    if request.method == "POST":  # 회원가입 정보 기입 후 확인 -> 데이터베이스에 정보 저장
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_gender = request.form['gender']
        user_age = request.form['age-group']
        user_job = request.form['occupation']
        member = tb_user_info(user_id, user_pw, user_gender, user_age, user_job)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('user.login'))  # 회원가입 후 로그인 창으로 바로 이동
    else:
        return render_template('join.html')  # 회원가입 페이지

# 로그인 페이지
@user.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:  # 로그인 정보 입력
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        session['logged_in'] = False
        if user_id == None or user_pw == None:
            errMsg = '아이디와 비밀번호를 입력해주세요'
        try:
            user = tb_user_info.query.filter(tb_user_info.user_id == user_id).all()  # 아이디 비교
            if user:  # 아이디 존재할 때
                user = tb_user_info.query.filter(tb_user_info.user_pw == user_pw).first()  # 비밀번호 비교
                if user:  # 아이디, 비밀번호 일치 -> 로그인 성공
                    session['logged_in'] = True
                    session['user_id'] = user_id
                    session['check'] = 1
                    return redirect(url_for('user.home'))
                else:  # 아이디, 비밀번호 불일치
                    errMsg = '아이디 또는 비밀번호가 틀렸습니다'
            else: # 아이디 없을 때
                errMsg = '아이디 또는 비밀번호가 틀렸습니다'
        except:
            errMsg = '로그인에 실패하였습니다'
        return render_template('login.html', errMsg=errMsg)

### 로그인 한 상태로 창만 닫으면 다시 flask run 했을 때 로그인 된 상태로 접속된다.
### 로그아웃 기능을 이용해야만 로그아웃상태가 된다.
### 창을 닫으면 자동적으로 session 데이터가 제거되도록 할 수는 없을까? - 일단 패스하고 다른 기능부터 만든다.
@user.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    session['admin_id'] = None
    # errMsg = None
    session['check'] = 0
    # mask_list = read_mask_data()
    # return render_template('main.html', check=session['check'], mask_list=mask_list, page_num=session['page_num'])
    return redirect(url_for('user.home'))
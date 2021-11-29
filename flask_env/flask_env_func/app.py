
from flask import Flask, render_template,request,session

#테스트용 임폿
from flask import redirect,url_for
from pymysql import NULL

#데이터베이스에서 불러와서 현 데이터와 비교하기 
from db_connect import db, engine,buffer,conn,cursor
import pandas as pd
import base64
from PIL import Image
''''''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ekdldksk@localhost:3306/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)
''''''

@app.route("/",methods=["GET","POST"])
def join():#
    # if request.method == 'POST':
    #     user_id = request.form['user_id']
    #     user_pw = request.form['user_pw']
    #     user_gender = request.form['gender']
    #     user_age = request.form['age-group']
    #     user_job = request.form['occupation']

    #     member = Member(user_id, user_pw,user_gender,user_age,user_job)
    #     db.session.add(member)
    #     db.session.commit()
    #     #테스트용
    #     return redirect(url_for('login'))
    # else:
       return render_template('join.html')

''''''
@app.route("/login",methods=["GET","POST"])
def login():

    user_info = pd.read_sql(sql='SELECT * FROM member',con=engine)
    user_check_id = user_info['user_id'].values
    user_check_pw = user_info['user_pw'].values
    print(user_check_id)
    if request.method == 'POST':
        ui = request.form['user_id']
        up = request.form['user_pw']
        try:
            if ui in user_check_id:
                if up in user_check_pw:
                    session['logged_in'] = True
                    session['user'] = ui
                    return redirect(url_for('Mlist'))
                else:
                    return '비밀번호가 틀립니다.'
            return '아이디가 없습니다.'
        except:
            return f'{user_info}'
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('user',None)
    return render_template('login.html')

#마이페이지
@app.route('/list',methods=["GET","POST"])
def Mlist():
    if 'user' in session:
        u = session['user']
        user_info = pd.read_sql(sql='SELECT * FROM review where user_id="%s"'%u,con=engine)
        if request.method == "POST":
            if 'modify' in request.form:
                return redirect(url_for('Modify',r_id=request.form['r_data']))
        return render_template('my_page.html',text=user_info)
    return redirect(url_for('login'))

#수정기능
@app.route('/modify',methods=["GET","POST"])
def Modify(): 
    if request.method == 'POST':
        r_id = request.form['r_id']
        if 'modi' in request.form:
            print(r_id)
            if not request.files.get('img_data'):
                img_data = NULL
            else:
                tmp_img_data = request.files['img_data']
                im= Image.open(tmp_img_data)
                im.save(buffer,format='png')
                img_data = base64.b64encode(buffer.getvalue())
                img_update = '''UPDATE review SET img_data=%s where r_id=%s'''
                cursor.execute(img_update,[img_data,r_id])
         
            star = request.form['star']
            r_data = request.form['r_data']
            r_op1 = request.form['r_op1']
            r_op2 = request.form['r_op2']
            r_op3 = request.form['r_op3']
            r_op4 = request.form['r_op4']

            update = '''UPDATE review 
                    SET star = %s,
                        r_data = %s,
                        r_op1 = %s,
                        r_op2 =%s,
                        r_op3 = %s,
                        r_op4 = %s
                    WHERE r_id = %s'''
            cursor.execute(update,[star,r_data,r_op1,r_op2,r_op3,r_op4,r_id])
            conn.commit()
            conn.close()
            return "수정되었습니다"
    if request.method == 'GET':
        #사용자 상품이름 고정 
        r_id = request.args.get('r_id')
        u = session['user']
        r = r_id
        goods_info = pd.read_sql(sql='SELECT * FROM review where r_id=%s'%r,con=engine)
        goods = str(goods_info['goods_id'].values[0])
        
        return render_template('modify.html', user_id = u, goods = goods, r_id=r_id)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)
 
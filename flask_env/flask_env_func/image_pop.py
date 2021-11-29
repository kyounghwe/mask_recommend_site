
from flask import Flask, render_template,request,session,redirect,url_for

from db_connect import db, buffer,engine,cursor,conn
import cgi

#이미지 데이터베이스에 저장
from models import review,Zzim
import base64
import pandas as pd
from PIL import Image

form = cgi.FieldStorage()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ekdldksk@localhost:3306/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)

@app.route("/",methods=["GET","POST"])
def reviews():
    if request.method == 'POST':
        #삭제기능 
        if 'delete' in request.form:
            in_id = request.form.getlist('r_data')
            del_data = '''DELETE FROM review where r_id=%s'''
            cursor.execute(del_data, [in_id[1]])
            conn.commit()
            conn.close()
            return redirect(url_for('reviews'))

        #찜기능
        elif 'zzim' in request.form:
            r_id = request.form.getlist('r_data')
            pk_id = r_id[1]            
            review_data = pd.read_sql(sql='SELECT * FROM review where r_id="%s"'%pk_id,con=engine)
            zzim_goods = review_data['goods_id'].values[0]
            zzim_user = review_data['user_id'].values[0]
            
            check_zzim = pd.read_sql(sql='SELECT user_id FROM zzim where goods_id="%s"'%zzim_goods,con=engine)
            if zzim_user in list(check_zzim['user_id']):
                del_zzim = '''DELETE FROM zzim where user_id=%s and goods_id=%s'''
                cursor.execute(del_zzim,[zzim_user,zzim_goods])
                conn.commit()
                conn.close()
                return "찜삭제"
            else:
                zzim = Zzim(zzim_user,zzim_goods)
                db.session.add(zzim)
                db.session.commit()
                session['zzim']=True
                return "찜추가"

        elif 'upload' in request.form:
            tmp_img_data = request.files['img_data']

            im= Image.open(tmp_img_data)
            im.save(buffer,format='png')
            img_data = base64.b64encode(buffer.getvalue())
            user_id = request.form['user_id']
            goods_id = request.form['goods_id']
            star = request.form['star']
            r_data = request.form['r_data']
            r_op1 = request.form['r_op1']
            r_op2 = request.form['r_op2']
            r_op3 = request.form['r_op3']
            r_op4 = request.form['r_op4']

            member = review(user_id,goods_id,star,r_data,r_op1,r_op2,r_op3,r_op4,img_data )
            db.session.add(member)
            db.session.commit()
            db.session.close()
            return redirect(url_for('reviews'))
        else:
            return "name 확인이 안됨"
    else:
        #아래 코드는 이미지를 잘 갖고 오는지 테스트하는 코드 
        img=[]
        show = review.query.all()
        img_df = pd.read_sql(sql='SELECT * FROM review',con=engine)
        for i in range(len(show)):
            img_str = img_df['img_data'].values[i]
            stage2 = img_str.decode('utf-8')
            img.append(stage2)
        
        return render_template('Mlist.html',show=img,text = img_df)   

#조회수 판별 기능
@app.route('/hits/<r_id_num>')
def hits_num(r_id_num):
    hits = '''UPDATE review SET hits = hits + 1 WHERE r_id = %s'''
    cursor.execute(hits, [r_id_num])
    conn.commit()
    conn.close()
    return "여기는 조회수 판별"

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)

    
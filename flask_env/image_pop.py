# from io import BytesIO
# from flask import Flask, render_template,request,session,redirect,url_for,Response

# from db_connect import db, buffer,engine
# import cgi

# #이미지 데이터베이스에 저장
# from models import tb_review
# import base64
# import pandas as pd
# from PIL import Image

# form = cgi.FieldStorage()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:5452tulahyo12!A@localhost:3306/try_mysql'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
# app.secret_key = 'super secret key'
# # app.config['SESSION_TYPE'] = 'filesystem'

# db.init_app(app)

# @app.route("/",methods=["GET","POST"])
# def reviews():
#     if request.method == 'POST':
        
#         tmp_img_data = request.files['img_data']

#         im= Image.open(tmp_img_data)
#         im.save(buffer,format='png')
#         img_data = base64.b64encode(buffer.getvalue())

#         user_id = request.form['user_id']
#         goods_id = request.form['goods_id']
#         star = request.form['star']
#         r_data = request.form['r_data']
#         r_op1 = request.form['r_op1']
#         r_op2 = request.form['r_op2']
#         r_op3 = request.form['r_op3']
#         r_op4 = request.form['r_op4']

#         member = tb_review(user_id,goods_id,star,r_data,r_op1,r_op2,r_op3,r_op4,img_data )
#         db.session.add(member)
#         db.session.commit()
#         return redirect(url_for('reviews'))
#     else:
#         #아래 코드는 이미지를 잘 갖고 오는지 테스트하는 코드 
#         img=[]
#         show = tb_review.query.all()
#         img_df = pd.read_sql(sql='SELECT * FROM review',con=engine)
#         for i in range(len(show)):
#             img_str = img_df['img_data'].values[i]
#             stage2 = img_str.decode('utf-8')
#             img.append(stage2)
#         return render_template('Mlist.html',show=img,text = show)

# if __name__ == '__main__':
#     app.run(host='127.0.0.1',port=5000, debug=True)

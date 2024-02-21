from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    ho = db.Column(db.String(50))
    ten = db.Column(db.String(50))
    email = db.Column(db.String(100))
    sdt = db.Column(db.String(20))
    img = db.Column(db.String(100))


@app.route('/save', methods=['POST'])
def create_user():
    data = request.json
    
    info = data.get('info', {})
    print(info)
    new_user = User(
        user = data.get('user', ''),
        password = data.get('password', ''),
        ho = info.get('ho', ''),
        ten = info.get('ten', ''),
        email = info.get('email', ''),
        sdt = info.get('sdt',''),
        img = info.get('img','')
    )
    db.session.add(new_user)
    db.session.commit()
    
    all_users = User.query.all()

    # # Tạo một danh sách để lưu trữ thông tin của tất cả người dùng
    users_list = []

    # # Lặp qua từng người dùng và chuyển đổi thông tin của họ thành đối tượng JSON
    for user in all_users:
        user_data = {
            'id': user.id,
            'user': user.user,
            'password': user.password,
            'info': {
                'ho': user.ho,
                'ten': user.ten,
                'email': user.email,
                'sdt': user.sdt,
                'img': user.img
            }
        }
        users_list.append(user_data)

    # Trả về một mảng JSON chứa thông tin của tất cả người dùng
    print(users_list)
    return jsonify(users_list)

@app.route('/')
def hello():
    return render_template("index.html")


if __name__ == '__main__':
   
    db.create_all()
    app.run(debug=True)

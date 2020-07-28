from flask import Flask, render_template
from flask_mail import Mail, Message
import webbrowser
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
mail = Mail(app)

# DBについて
engine = create_engine('sqlite:///users.db')
base = declarative_base()

class User(base):
    __tablename__ = "users"
    number = Column(Integer, primary_key=True, unique=True)
    id = Column(String)
    old_password = Column(String)
    new_password = Column(String)

    def __repr__(self):
        return "Users<id:{},old_password:{},new_password:{}>".format(self.id, self.old_password, self.new_password)


base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
session = session_maker()

# フィッシングメール詐欺
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['NAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''  # 送信者(送信用のgmailのアドレスを入力する) <=セキュリティレベルを低くする必要あり
app.config['MAIL_PASSWORD'] = '' #送信者のアドレスのパスワードを入力する
mail = Mail(app)

# スタート画面
@app.route("/")
def index():
    return render_template('start.html')

# (1-1)Gmailが届く画面
@app.route('/mail', methods=['POST'])
def send_mail():
    msg = Message('[ひがし銀行]不正ログインについて',
                  sender='',  # 送信者(先ほどの送信用のアドレスを入力)
                  recipients=[''])  # 受信者(先ほどとは、別の受信者用のgmailアドレスを入力する)
    msg.html = render_template('mail.html')
    mail.send(msg)
    url = "https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox"
    webbrowser.open(url)
    return render_template('start.html')


# (1-2)IDとパスワードを入力する画面
@app.route('/signin')
def sign():
    return render_template('signin.html')


# (1-3)パスワード変更後の画面
@app.route('/login', methods=['POST'])
def login():
    """msg_id = request.form["id"]
    msg_old_password = request.form["old_password"]
    msg_new_password = request.form["new_password"]

    # 入力されたかどうかをチェックする
    if (check_str(msg_id) != "not strings" and check_str(msg_old_password) != "not strings" and check_str(
            msg_new_password) != "not strings"):
        print("IDについて " + msg_id)
        print("現在のパスワード " + msg_old_password)
        print("新しいパスワード" + msg_new_password)

        # DBにデータを格納する
        user = User(id=msg_id, old_password=msg_old_password, new_password=msg_new_password)
        session.add(user)
        session.commit()

        # DBからデータを入手する
        user_information = session.query(User).get(1)
        print(user_information)"""
    return render_template('password_change.html')

# (1-4)解説用の画面
@app.route('/end', methods=['POST'])
def end():
    return render_template('end.html')

# (2-1)広告表示サイト
@app.route('/advertisement', methods=['POST'])
def advertisement():
    return render_template('advertisement.html')

# (2-1)アンケート詐欺のページ
@app.route('/questionnaire_page', methods=['POST'])
def questionnaire_page():
    return render_template('questionnaire_page.html')

# (2-2)個人情報入力ページに移動
@app.route('/input_page', methods=['GET'])
def sign2():
    return render_template('input_page.html')

# (2-3)個人情報入力ページに移動2
@app.route('/input_card_page', methods=['POST'])
def enter_information():
    return render_template('input_card_page.html')

# (2-4)エラーページに移動
@app.route('/credit_information', methods=['POST'])
def enter_credit():
    return render_template("error_page.html")

# (2-5)解説用の画面
@app.route('/end2', methods=['POST'])
def end2():
    return render_template("end2.html")

# (3)解説用の画面
@app.route('/start', methods=['POST'])
def start():
    return render_template("start.html")

# この関数で文字が入力されたかをチェックする
def check_str(s):
    if s:
        message = s
        return message
    else:
        message = "not strings"
        return message


if __name__ == '__main__':
    app.run(debug=True)

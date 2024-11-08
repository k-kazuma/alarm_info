from flask import Flask, redirect, request, jsonify, json
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import text
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


app = Flask(__name__)

# flaskmail

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "alarm.scheduler@gmail.com"
app.config["MAIL_PASSWORD"] = "guuf oebg oolg ruvx"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = (
    "alarm.scheduler@gmail.com"  # これがるとsender設定が不要になる
)
mail = Mail(app)


####################################


# sqlAlchemy


db = SQLAlchemy(model_class=Base)
cors = CORS(app, resources={r"/*": {"origins": ["https://alarmscheduler.com"]}})

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Inquiry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, default=datetime.now(timezone.utc), comment="作成日時"
    )
    content: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()


with app.app_context():
    db.create_all()
######################################################################


@app.route("/")
def hello():
    inquiries = Inquiry.query.all()

    # データをリスト形式でJSONに変換
    inquiries_list = [
        {
            "id": inquiry.id,
            "created": inquiry.created_at,
            "comment": inquiry.comment,
            "content": inquiry.content,
        }
        for inquiry in inquiries
    ]
    response = app.response_class(
        response=json.dumps(inquiries_list, ensure_ascii=False),
        mimetype="application/json",
    )
    print(response.data)
    # JSONレスポンスとして返す
    return response.data


@app.route("/post/", methods=["POST", "OPTIONS"])
def info_post():
    if request.method == "OPTIONS":
        # CORSのプリフライトリクエストに対する適切なレスポンスを返す
        return "", 204
    elif request.method == "POST":
        data = request.get_json()
        comment = data.get("comment")
        content = data.get("content")

        # サーバーが用意できるまではメールで問い合わせ内容送信
        msg = Message("【問い合わせ】", recipients=["alarm.scheduler@gmail.com"])
        msg.body = "タイトル：" + content + "\n" "本文：" + comment
        mail.send(msg)

        # 新しいInquiryオブジェクトを作成
        new_inquiry = Inquiry(comment=comment, content=content)

        # データベースに追加
        db.session.add(new_inquiry)
        db.session.commit()
        print(data)
        return data


@app.route("/inquiry/edit/asdfghjkl11/", methods=["GET", "POST"])
def inquiry_edit():
    if request.method == "GET":
        inquiries = Inquiry.query.all()
        inquiries_list = [
            {"id": inquiry.id, "comment": inquiry.comment, "content": inquiry.content}
            for inquiry in inquiries
        ]
        response = app.response_class(
            response=json.dumps(inquiries_list, ensure_ascii=False),
            mimetype="application/json",
        )
        return response

    if request.method == "POST":
        return "inquiry_post"


if __name__ == "__main__":
    app.run(debug=True)


# http://127.0.0.1:5000/inquiry/edit/asdfghjkl11/

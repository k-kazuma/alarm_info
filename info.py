from flask import Flask, redirect, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import text
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
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

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Inquiry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()


with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return "<p>Hello, World!</p>"


@app.route("/post")
def info_post():
    a = ""
    print("post")
    return redirect("http://127.0.0.1:5000/")


if __name__ == "__main__":
    app.run(debug=True)

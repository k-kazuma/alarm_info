from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)


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

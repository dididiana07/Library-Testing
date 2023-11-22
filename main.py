import os, datetime
import sqlalchemy.exc
import werkzeug.exceptions
from flask import Flask, render_template,redirect, url_for, request, flash
from SignInRegisterForm import SignIn, Register
from AddBookForms import AddBook
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_manager, login_user, logout_user, UserMixin, current_user

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"  + os.path.join(basedir, "data.sqlite")
current_year = datetime.datetime.now().year

db = SQLAlchemy(app)
loginManager = login_manager.LoginManager(app=app)
loginManager.login_view = "login"


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=False)
    author = db.Column(db.String, nullable=False, unique=False)
    user = db.Column(db.String, nullable=False)
    rate = db.Column(db.Integer)



@loginManager.user_loader
def get_user(user_id):
    return db.session.query(Users).get(user_id)


@app.route("/")
def index():
    try:
        if current_user:
            return redirect(url_for("books", username=current_user.username))
    except AttributeError:
        pass
    return render_template("index.html", year=current_year)

@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        if current_user:
            return redirect(url_for("books", username=current_user.username))
    except AttributeError:
        pass
    forms = SignIn()
    if forms.validate_on_submit():
        try:
            username = forms.username.data
            password = forms.password.data
            session = forms.session.data
            user = Users.query.filter_by(username=username).first()
            if check_password_hash(pwhash=user.password, password=password):
                login_user(user=user, remember=session)
                return redirect(url_for("books", username=username))
        except AttributeError:
            pass
    return render_template("login.html", forms=forms, year=current_year)

@app.route("/register", methods=["POST", "GET"])
def register():
    try:
        if current_user:
            return redirect(url_for("books", username=current_user.username))
    except AttributeError:
        pass
    forms = Register()
    if forms.validate_on_submit():
        username = forms.username.data
        email = forms.email.data
        password = generate_password_hash(forms.password.data, method="pbkdf2:sha1", salt_length=8)
        new_user = Users(username=username, password=password, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user)
            return redirect(url_for("books", username=username))
        except sqlalchemy.exc.IntegrityError:
            flash("User already in use.")
    return render_template("register.html", year=current_year, forms=forms)


@app.route("/my-library", methods=["GET", "POST"])
@login_required
def books():
    user = request.args["username"]
    forms = AddBook()
    all_user_books = Books.query.filter_by(user=current_user.username).all()
    if forms.validate_on_submit():
        title = forms.title.data
        author = forms.author.data
        rate = forms.rate.data
        user = current_user.username
        new_book = Books(title=title, author=author, rate=rate, user=user)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("books", username=current_user.username))
    return render_template("books.html", username=user, forms=forms, user_books=all_user_books,
                           total=len(all_user_books))


@app.route("/delete")
def delete_book():
    id_book = request.args["id_book"]
    delete = Books.query.filter_by(id=id_book).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for("books", username=current_user.username))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
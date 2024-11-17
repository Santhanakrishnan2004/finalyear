# from flask import Flask, render_template, request, redirect, url_for, flash

# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Replace with a strong key

# # Dummy data for users
# users = {"test@example.com": "password123"}


# @app.route("/")
# def home():
#     return render_template("home.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         if email in users and users[email] == password:
#             flash("Login successful!", "success")
#             return redirect(url_for("home"))
#         else:
#             flash("Invalid credentials. Please try again.", "danger")
#     return render_template("login.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         if email in users:
#             flash("Email already registered.", "warning")
#         else:
#             users[email] = password
#             flash("Registration successful! You can now log in.", "success")
#             return redirect(url_for("login"))
#     return render_template("register.html")


# @app.route("/prediction")
# def prediction():
#     return redirect("https://sakhi-asd-prediction-system.streamlit.app/")


# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "asd-prediction-system-sakhi"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


# Routes
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/prediction")
def prediction():
    return redirect("https://sakhi-asd-prediction-system.streamlit.app/")


if __name__ == "__main__":
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)

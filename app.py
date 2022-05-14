from flask import Flask, redirect, request, render_template, url_for
from flask_mysqldb import MySQL
from flask_login import login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bcrypt import Bcrypt
from time import sleep

app = Flask(__name__)
app.secret_key = "mlask"
mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route("/")
def home():
    # Configure Home page
    return render_template("index.html")

# ----------------------LOGIN--------------------------------
class LoginForm(FlaskForm):
    user_name  = StringField('UserName', validators=[DataRequired(), Length(min=4, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    user_name  = StringField('UserName', validators=[DataRequired(), Length(min=4, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Register')

# Set values to your configurating for it to work
# Also this needs a database 'reservation system' and table named 'users' with columns 'username' and 'password' to work properly
# Adjust the code should you have other names for them
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Bootable10"
app.config["MYSQL_DB"] = "reservation system"

@app.route("/user/logout")
@login_required
def logout():
    logout_user()
    redirect("/")

@app.route("/user/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT username FROM users WHERE username = '" + form.user_name.data + "'")
            data = cursor.fetchall()
            text = ""
            
            for each in data:
                text += str(each)
            if text != "":
                cursor.close()
                # NEEDS SOME TWEAKING, it is an alpha version after all
                return "<script>alert('Username already exists. Try a different one.'); window.location.replace('register')</script>"
            
            psd_hash = bcrypt.generate_password_hash(form.password.data)
            cursor.execute("INSERT INTO users (username, psd) VALUES (%s, %s)", (form.user_name.data, psd_hash))
            mysql.connection.commit()
            cursor.close()
            return "<h2>New user [" + form.user_name.data + "] has been registered.</h2><a href='/'>Go to HOME page</a>" # NEEDS SOME TWEAKING, it is an alpha version after all
    return render_template("register.html", form=form)

@app.route("/user/login")
def login():
    # bcrypt.check_password_hash(hash, password) Returns True/False
    pass

# ---------------END LOGIN-------------------------

if __name__ == "__main__":
    app.run(debug=True)
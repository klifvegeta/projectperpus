from flask import flash, redirect, render_template, request, session, abort
from random import randint
from app import app, db
from .forms import SignupForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import redirect, url_for, session
from models import Users

app.config['WTF_CSRF_ENABLE'] = True
app.config['SECRET_KEY'] = "mantan-terindah"

@app.route('/')
def home():
    quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
               "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
               "'To understand recursion you must first understand recursion..' -- Unknown",
               "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
               "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
               "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]
    randomNumber = randint(0,len(quotes)-1)
    quote = quotes[randomNumber]
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('hello.html', **locals())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username') != None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = Users.query.filter_by(username=username).first()

        if user:
            if password == user.pwdhash:
                session['username'] = username
                loguser = Users(user.uid)
                login_user(loguser)
                return redirect(request.args.get("next"))
            else:
                return "Password Salah"
        else:
            return "user {} tidak ditemukan!".format(username)
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
@app.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate():
            user = Users()
            form.populate_obj(user)

            user_exist = Users.query.filter_by(username=form.username.data).first()
            email_exist = Users.query.filter_by(email=form.email.data).first()

            if user_exist:
                form.username.errors.append('Username already taken')

            if email_exist:
                form.email.errors.append('Email already use')

            if user_exist or email_exist:
                return render_template('signup2.html',
                                       form = form,
                                       page_title = 'Daftar')

            else:
                user.firstname = "Firstname"
                user.lastname = "Lastname"
                db.session.add(user)
                db.session.commit()
                return render_template('signup-success.html', user = user, page_title = 'Sign Up Success!')

        else:
            return render_template('signup2.html', form = form, page_title = 'Daftar')
     return render_template('signup2.html', form = SignupForm(), page_title = 'Daftar')

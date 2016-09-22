from flask import render_template, request,flash, abort
from flask import redirect, url_for, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from main import app
from forms import *
from models import *
from datetime import datetime
from config import Config
from random import randint
import os

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

@login_manager.user_loader
def load_user(userid):
    return User(userid)

"""
  @login_manager.user_loader
  def user_loader(user):
    user = User.query.filter_by(username=user).first()
    if user != True:
        return "User tidak ditemukan"
    user = User()
    #user.id = email
    return user


  @login_manager.request_loader
  def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return "Gagal"

    user = User()
    #user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == user.password

    return user
"""

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
       user = User.query.filter_by(username=username).first()

       if user:
          if password == user.password:
            #set session
            session['username'] = username
            loguser = User(user.uid)
            login_user(loguser)
            return redirect(request.args.get("next"))
          else:
            return "Password Salah"
       else:
          return "{} belum terdaftar".format(username)
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
            user = User()
            form.populate_obj(user)

            user_exist = User.query.filter_by(username=form.username.data).first()
            email_exist = User.query.filter_by(email=form.email.data).first()

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
                return "berhasil"

        else:
            return render_template('signup2.html', form = form, page_title = 'Daftar')
     return render_template('signup2.html', form = SignupForm(), page_title = 'Daftar')
@app.route('/pinjam/', methods=['GET','POST'])
@login_required
def transaksi():
    # Cek Session login
    #if session.get('username') != None:
        # Cek method
        if request.method == "POST":
            bukupinjam = request.form['bukupinjam']
            buku = Buku.query.filter_by(idbuku=bukupinjam).first()
            # Jika buku di temukan
            if buku:
                usernya = User.query.filter_by(username=session['username']).first()
                idusernya = usernya.uid

                # Cek jika dia sedang pinjam buku tersebut
                cekpinjaman = Transaksi.query.filter_by(iduser=idusernya).all()
                for cek in cekpinjaman:
                    if cek.idbuku == buku.idbuku:
                        return "Anda lagi minjam buku ini gan."


                # Jika durasi pinjam di antara 1-4 Hari
                if durasi >= 1 and durasi <= 4:
                    # Insert ke tabel pinjam

                    #idusernya sama idbuku adalah foreign key
                    pinjam = Transaksi(idusernya,buku.idbuku,datetime.now(),durasi)

                    #kurangin qty buku yang di pinjam
                    buku.qty_buku -= 1
                    db.session.add(pinjam)
                    db.session.commit()

                    return "Sukses Pinjam , Jangan telat baikin ya"
                else:
                    return "Ngak bisa pinjam lebih dari 4 hari gan."
            else:
                return "Buku yang di pinjam tidak di temukan"
        else:
            return render_template("hello.html",bukus=Buku.query.all())

    #else:
    #   return redirect(url_for('login'))

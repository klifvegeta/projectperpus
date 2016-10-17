from flask import render_template, request, flash, abort
from flask import redirect, url_for, session
from main import app
from forms import *
from sqlalchemy.orm import sessionmaker
from models import *
from flask_login import LoginManager, login_required, login_user, logout_user
from datetime import datetime
from config import Config
from random import randint
import os
import md5

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
def hash_string(string):
    """
    Return the md5 hash of a (string+salt)
    """
    salted_hash = string + app.config['SECRET_KEY']
    return md5.new(salted_hash).hexdigest()

@app.route('/', methods=['GET','POST'] )
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
#percobaan git gnome

@app.route('/login', methods=['GET', 'POST'])
def login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/logout')
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
                flash("berhasil")


        else:
            return render_template('signup2.html', form = form, page_title = 'Daftar')
     return render_template('signup2.html', form = SignupForm(), page_title = 'Daftar')

@app.route('/pinjam/', methods=['GET','POST'])
def pinjam():
    # Cek Session login
    #if session.get('username') != None:
        # Cek method
        if request.method == "POST":
            bukupinjam = request.form['bukupinjam']
            durasi = int(request.form['durasi'])
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


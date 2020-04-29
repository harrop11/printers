from flask import redirect, url_for, flash, render_template
from flask import session, request, url_for, redirect, render_template
from flask_login import login_user, logout_user, current_user
from app import app, db
from werkzeug.utils import secure_filename
from app.models import Users, Pjasa, Orders, Product
import re
import os

app.config['UPLOAD_FOLDER'] = 'app/uplouds/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#login admin/pjasa
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        pjasa = Pjasa.query.filter_by(username=username, password=password).first()
        # If account exists in accounts table in out database
        if pjasa:
            # Create session data, we can access this data in other routes
            session['admin_loggedin'] = True
            session['pid'] = pjasa.pid
            session['username'] = pjasa.username
            # Redirect to home page
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template("admin/login.html")

    return render_template('admin/login.html')


#regis admin/pjasa
@app.route('/admin_regis', methods=['GET', 'POST'])
def admin_regis():

    if request.method == "POST" and 'email' in request.form and 'mobile' in request.form and 'alamat' in request.form and 'username' in request.form and 'password' in request.form:
        print('cek')
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        alamat = request.form.get("alamat")
        username = request.form.get("username")
        password = request.form.get("password")
        # Check if account exists using MySQL
        pjasa = Pjasa.query.filter_by(email=email).first()
        # If account exists show error and validation checks
        if pjasa:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', email):
            msg = 'Username must contain only characters and numbers!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            pjasa = Pjasa(email=email, mobile=mobile, alamat=alamat, username=username, password=password)
            db.session.add(pjasa)
            db.session.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('admin_login'))
    return render_template('admin/register.html')


@app.route('/index')
def index():
    orders = Orders.query.all()
    return render_template("admin/index.html", orders=orders)


@app.route('/add')
def add_product():
    if request.method=="POST":
        toko = request.form.get("toko")
        unit = request.form.get("unit")
        bw = request.form.get("bw")
        berwarna = request.form.get("berwarna")
        kertas = request.form.get("kertas")
        deskripsi = request.form.get("deskripsi")
        alamat = request.form.get('alamat')
        jam = request.form.get("jam")
        files = request.files['picture']
        if files:
            filename = secure_filename(files.filename)
            files.save(os.path.join(app.config['UPLOAD_FOLDER'] + "gambar" , filename))
            product = Product(toko=toko, unit=unit, bw=bw, berwarna=berwarna, kertas=kertas, deskripsi=deskripsi, alamat=alamat, jam=jam, picture=filename)
            db.session.add(product)
            db.session.commit()
    return render_template("admin/tables.html")



#login user
@app.route('/login', methods=['GET', 'POST'])
def login():

    #jika tombol button di klik -> request POST
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        users = Users.query.filter_by(username=username, password=password).first()
        # If account exists in accounts table in out database
        if users:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['uid'] = users.uid
            session['username'] = users.username
            # Redirect to home page
            return redirect(url_for('sukses_reg'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template("index.html")


@app.route("/")
def sukses_reg():
    product = Product.query.all()
    kalimat = "anda berhasil login"
    return render_template("home.html", kalimat=kalimat, product=product)


#regis user
@app.route("/register", methods=["POST", "GET"])
def register():
    
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        nama = request.form.get("nama")
        username = request.form.get("username")
        email = request.form.get("email")
        notlp = request.form.get("notlp")
        alamat = request.form.get("alamat")
        password = request.form.get("password")
        # Check if account exists using MySQL
        users = Users.query.filter_by(username=username).first()
        # If account exists show error and validation checks
        if users:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            users = Users(nama=nama, username=username, email=email, notlp=notlp, alamat=alamat, password=password)
            db.session.add(users)
            db.session.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))

     
    return render_template("register.html")



@app.route("/redirect-register")
def redirect_regis():
    return redirect(url_for("register"))


@app.route("/status")
def status():
    #jika dia sedang login
    if "username" in session:
        orders=Orders.query.all()
        return render_template("status.html", orders=orders)
    else:
        #jika dia tidak sedang login
        return redirect(url_for('login'))

@app.route("/redirect-status")
def ayo_redirect_status():
    return redirect(url_for("status"))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route("/pemesanan", methods=["POST", "GET"])
def pemesanan():
    if "username" in session:
        product = Product.query.filter_by(id=idp).first()
    else:
        return redirect(url_for('login'))
        if request.method=="POST":
            nama = request.form.get("nama")
            warna = request.form.get("warna")
            kertas = request.form.get("kertas")
            catatan = request.form.get("catatan")
            files = request.files['file']
            if files:
                filename = secure_filename(files.filename)
                files.save(os.path.join(app.config['UPLOAD_FOLDER'] + "files" , filename))
                orders = Orders(nama=nama, warna=warna, kertas=kertas, catatan=catatan, file=filename)
                db.session.add(orders)
                db.session.commit()
        return render_template("pemesanan.html", product=product)

@app.route("/redirect-pemesanan")
def redirect_pemesanan():
    return redirect(url_for("pemesanan"))


@app.route("/logout")
def logout_akun():
    if "username" in session:
        session['loggedin'] = False
        session.pop("username")
        return redirect(url_for('sukses_reg'))
    else:
        return redirect(url_for('sukses_reg'))


    if __name__ == "__main__":
        app.run(debug=True, port=5000)
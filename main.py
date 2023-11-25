from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'bebasapasaja'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotelpython'
mysql = MySQL(app)

@app.route('/')
def home():
    if session.get('user_id'):
        session.get('user_level')
        return render_template('index.html')
    else:
        session.pop('user_id', None)
        session.pop('user_level', None)
        return render_template('index.html')

@app.route('/admin')
def customertampildata():
    if session.get('user_id'):
        level = session.get('user_level') 
        if level == 'admin':
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM customer ORDER BY id DESC")
            datatampil = cur.fetchall()
            cur.close()
            return render_template('admin.html', datapemesan=datatampil)
        else:
            return 'Anda tidak memiliki izin untuk mengakses halaman ini.'
    else:
        session.pop('user_id', None)
        session.pop('user_level', None)
        return render_template('index.html')

@app.route('/userregister', methods=['POST'])
def userregister():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        pincode = request.form['pincode']
        dateofbirth = request.form['dateofbirth']
        password = request.form['password']
        confirmpassword = request.form["confirmpassword"]
        level = request.form["level"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        users = cur.fetchall()
        cur.close()
        if len(users) > 0:
            return "Email already used"
        else:
            if password == confirmpassword:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (firstname, lastname, email, phone, address, pincode, dateofbirth, password, level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (firstname, lastname, email, phone, address, pincode, dateofbirth, password, level))  # Memperbaiki query untuk memasukkan level yang didapat dari form
                mysql.connection.commit()
                flash("Data Berhasil di kirim")
                return redirect(url_for('home'))
            else:
                return "Passwords do not match"

@app.route('/login', methods=['POST'])  # Memperbaiki rute login agar tidak bertabrakan dengan rute lainnya
def userlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        users = cur.fetchall()
        cur.close()

        if len(users) > 0:
            session['user_id'] = users[0]['id']
            session['user_level'] = users[0]['level']
            return redirect('/')
        else:
            return 'Email atau password salah'
#proses insert into customer
@app.route('/', methods=['POST'])
def customerinsert():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['phone']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jml = request.form['jml']
        ket = request.form['ket']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer (nama, email, phone, tipe, checkin, checkout, jml, ket) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nama, email, phone, tipe, checkin, checkout, jml, ket))
        mysql.connection.commit()
        flash("Data Berhasil di kirim")
        return redirect(url_for('home'))

#proses update into customer
@app.route('/customerupdate', methods=['POST'])
def customerupdate():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['phone']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jml = request.form['jml']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE customer SET nama=%s, email=%s, phone=%s, tipe=%s, checkin=%s, checkout=%s, jml=%s, status=%s WHERE id=%s", (nama, email, phone, tipe, checkin, checkout, jml, status, id))
        mysql.connection.commit()
        flash("Data Berhasil di Update")
        return redirect(url_for('customertampildata'))

#delete data customer
@app.route('/customerhapus/<int:id>', methods=["GET"])
def customerhapus(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customer WHERE id=%s", (id,))
    mysql.connection.commit()
    flash("data Berhasil di Hapus")
    return redirect( url_for('customertampildata'))

#session logout
@app.route('/logout')
def logout():
  session.pop('user_id', None)
  session.pop('user_level', None)


if __name__ == '__main__':
    app.run(debug=True)

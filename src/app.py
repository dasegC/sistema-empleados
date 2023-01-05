from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '15211730'
app.config['MYSQL_DATABASE_DB'] = 'empleados'
#
app.config['TMP_DIR'] = './src/uploads'

mysql.init_app(app)


@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)

    empleados = cursor.fetchall()

    conn.commit()

    return render_template('/empleados/index.html', empleados=empleados)


@app.route('/create')
def create():

    return render_template('empleados/create.html')


@app.route('/store', methods=['POST'])
def method_name():

    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    # Cambiar el nombre de la foto
    now = datetime.now()
    print(now)
    tiempo = now.strftime('%Y%H%M%S')
    print(tiempo)

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '-' + _foto.filename
        tmp_folder= app.config['TMP_DIR'] 
        file_path = os.path.join(tmp_folder, nuevoNombreFoto)
        _foto.save(file_path)
        #_foto.save('./uploads' + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s,%s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

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
# Se crea configuracion para carpeta de archivos de fotos
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
        tmp_folder = app.config['TMP_DIR']  # Se crea carpeta temporal
        file_path = os.path.join(
        tmp_folder, nuevoNombreFoto)  # Se crea el path
        # Se guarda el archivo en directorio especificado
        _foto.save(file_path)
        # _foto.save('./uploads' + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s,%s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    sql = 'DELETE FROM empleados WHERE id=%s'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()

    return redirect('/')


@app.route('/modify/<int:id>')
def modify(id):
    sql = 'SELECT * FROM empleados WHERE id=%s'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    empleado = cursor.fetchone()
    conn.commit()

    return render_template('empleados/edit.html', empleado=empleado)


@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    #datos = (_nombre, _correo, id)
    
    conn = mysql.connect()
    cursor= conn.cursor()

    if _foto.filename != '':
        #now = datetime.now()
        #tiempo = now.strftime('%Y%H%M%S')
        #nuevoNombreFoto = tiempo + '-' + _foto.filename
        tmp_folder = app.config['TMP_DIR']  # Se crea carpeta temporal
        #file_path = os.path.join(tmp_folder, nuevoNombreFoto)  # Se crea el path
        # Se guarda el archivo en directorio especificado
        #_foto.save(file_path)
        # _foto.save('./uploads' + nuevoNombreFoto)

        sql = f"SELECT foto FROM empleados WHERE id={id};"
        print(sql)
        cursor.execute(sql)
        
        nombreFoto = cursor.fetchone()[0]
        print(nombreFoto)
        
        file_path = os.path.join(tmp_folder, nombreFoto)
        os.remove(file_path)
    

    conn = mysql.connect()
    cursor = conn.cursor()
    
    
    sql = f'UPDATE empleados SET nombre={_nombre}, correo={_correo} WHERE id={id};'
    print('------------------------------')
    print(sql)
    cursor.execute(sql)
    conn.commit()    


if __name__ == '__main__':
    app.run(debug=True)

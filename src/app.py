from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

if __name__ == '__main__':
    app.run(debug=True)

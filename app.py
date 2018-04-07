from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
con = sqlite3.connect('main.db')


@app.route('/')
def index():
    sites = con.execute("SELECT * FROM site").fetchall()
    return render_template('index.html', sites=sites)


@app.route('/site/<int:id_site>')
def site(id_site):
    one_site = con.execute("SELECT * FROM site WHERE id=" + str(id_site)).fetchone()
    return render_template('site.html', one_site=one_site)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run()

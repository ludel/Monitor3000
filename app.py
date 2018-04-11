from flask import Flask, render_template, request, session, redirect, url_for, flash
from secret_config import SECRET_KEY
import sqlite3
from passlib.hash import argon2

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    query = "SELECT s.id, s.url, r.number FROM site s" \
            " JOIN requests r ON s.id = r.siteId" \
            " GROUP BY r.siteId"
    sites = exec_sql(query).fetchall()
    return render_template('index.html', sites=sites)


@app.route('/site/<int:id_site>')
def one_site(id_site):
    query = "SELECT s.url, r.number, r.date FROM site s" \
            " JOIN requests r ON s.id = r.siteId" \
            " WHERE r.siteId = {}".format(id_site)
    all_request = exec_sql(query).fetchall()
    return render_template('one_site.html', all_request=all_request)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form:
        username = request.form['username']
        password = request.form['password']

        try:
            true_password = exec_sql("SELECT password FROM user WHERE pseudo like '{}'".format(username)).fetchone()[0]
        except TypeError:
            flash('Error: Bad username or password')
            return redirect(url_for('login'))

        if argon2.verify(password, true_password):
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('admin'))

    if session.get('logged_in'):
        return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You were successfully log out')
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    check_login()

    sites = exec_sql("SELECT * FROM site").fetchall()
    return render_template('admin.html', sites=sites)


@app.route('/admin/newSite', methods=['GET', 'POST'])
def new_site():
    check_login()

    if request.form:
        url = request.form['url']
        exec_sql("INSERT INTO site (url) VALUES ('{}')".format(url), True)
        return redirect(url_for('admin'))

    return render_template('new_site.html')


@app.route('/admin/site/<int:id_site>/change', methods=['GET', 'POST'])
def manager_site(id_site):
    check_login()

    site = exec_sql("SELECT url FROM site WHERE id == {}".format(id_site)).fetchone()

    if request.form:
        url = request.form['url']
        exec_sql("UPDATE site SET url = '{}' WHERE id = '{}'".format(url, id_site), True)
        return redirect(url_for('admin'))

    return render_template('manage_site.html', site=site)


@app.route('/admin/site/<int:id_site>/delete')
def delete_site(id_site):
    check_login()

    exec_sql("DELETE FROM 'site' WHERE id = {}".format(id_site), True)

    return redirect(url_for("admin"))


def exec_sql(query, commit=False):
    req = sqlite3.connect('main.db').execute(query)
    if commit:
        req.execute("COMMIT ")
    return req


def check_login():
    if not session.get('logged_in'):
        flash('Error: Login first')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, session, redirect, url_for, flash
from secret_config import SECRET_KEY
import sqlite3

app = Flask(__name__)
con = sqlite3.connect('main.db')
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    query = "SELECT s.url, r.number, r.date FROM site s" \
            " JOIN requests r ON s.id = r.siteId" \
            " GROUP BY r.siteId"
    sites = con.execute(query).fetchall()
    return render_template('index.html', sites=sites)


@app.route('/site/<int:id_site>')
def one_site(id_site):
    query = "SELECT s.id, s.url, r.number, r.date FROM site s" \
            " JOIN requests r ON s.id = {}".format(id_site)
    all_request = con.execute(query).fetchall()
    return render_template('one_site.html', all_request=all_request)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form:
        username = request.form['username']
        password = request.form['password']
        true_password = con.execute("SELECT password FROM user WHERE pseudo like '{}'".format(username)).fetchone()[0]

        if password == true_password:
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('admin'))

    if session['logged_in']:
        return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You were successfully log out')
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        flash('Login first')
        return redirect(url_for('login'))

    sites = con.execute("SELECT * FROM site").fetchall()
    return render_template('admin.html', sites=sites)


@app.route('/admin/newSite', methods=['GET', 'POST'])
def new_site():
    if not session.get('logged_in'):
        flash('Login first')
        return redirect(url_for('login'))

    if request.form:
        url = request.form['url']
        con.execute("INSERT INTO site (url) VALUES ('{}')".format(url))
        return redirect(url_for('admin'))

    return render_template('new_site.html')


@app.route('/admin/site/<int:id_site>/change', methods=['GET', 'POST'])
def manager_site(id_site):
    if not session.get('logged_in'):
        flash('Login first')
        return redirect(url_for('login'))

    site = con.execute("SELECT url FROM site WHERE id == {}".format(id_site)).fetchone()

    if request.form:
        url = request.form['url']
        con.execute("UPDATE site SET url = '{}' WHERE id = '{}'".format(url, id_site))
        return redirect(url_for('admin'))

    return render_template('manage_site.html', site=site)


@app.route('/admin/site/<int:id_site>/delete')
def delete_site(id_site):
    if not session.get('logged_in'):
        flash('Login first')
        return redirect(url_for('login'))

    con.execute("DELETE FROM 'site' WHERE id = {}".format(id_site))

    return redirect(url_for("admin"))


if __name__ == '__main__':
    app.run()

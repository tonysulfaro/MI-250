from flask import Flask, session, redirect, url_for, escape, request

#database stuff
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

engine = create_engine('sqlite:///music-data.db', echo=True)
Base = declarative_base()
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            username:
            <p><input type=text name=username>
            <br>
            password:
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/albums', methods=['GET', 'POST'])
def get_albums():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)

import re

from flask import Flask, render_template, request, redirect
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# write your code here
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()

class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)
    regex = Column(String(50))
    text = Column(String(1024))
    result = Column(Boolean())

Base.metadata.create_all(engine)

def save_data(reg, text, res):
    rec = Record(regex=reg, text=text, result=res)
    session.add(rec)
    rec_id = session.query(Record).all()[-1].id
    session.commit()
    return rec_id

@app.route('/history/')
def view_history():
    recs = reversed(session.query(Record).all())
    return render_template('history.html', recs=recs)

@app.route('/result/<id>/')
def view_result(id):
    query = session.query(Record)
    rec = query.filter(Record.id == id)[0]
    res = str(bool(rec.result))
    return render_template('result.html',
                           regex=rec.regex,
                           text=rec.text,
                           result=res)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        regex = request.form['regex']
        text = request.form['text']
        result = re.match(regex, text) is not None
        id = save_data(regex, text, result)
        return redirect(f'/result/{id}/')

# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

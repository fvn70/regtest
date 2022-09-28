import re

from flask import Flask, render_template, request
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# write your code here
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')
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
    session.commit()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        regex = request.form['regex']
        text = request.form['text']
        result = re.match(regex, text) is not None
        save_data(regex, text, result)
        return 'True' if result else 'False'

# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

from flask import Flask, render_template
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

@app.route('/')
def index():
    return render_template('home.html')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

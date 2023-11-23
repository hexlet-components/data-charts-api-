from flask import Flask, request
from datetime import datetime
import os
import psycopg

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


def get_db():
    return psycopg.connect(app.config['DATABASE_URL'])


@app.route('/')
def index():
    return 'It Works'


@app.get('/visits')
def get_visits():
    query = request.args
    print(app.config['DATABASE_URL'])
    begin_date = datetime.fromisoformat(query['begin'])
    end_date = datetime.fromisoformat(query['end'])
    query = '''
        SELECT *
        FROM visits
        WHERE visits.datetime BETWEEN (%s) AND (%s);'''
    conn = get_db()
    with conn.cursor() as c:
        c.execute(query, [begin_date, end_date])
        res = c.fetchall()
    return res


@app.get('/registrations')
def get_registrations():
    query = request.args
    begin_date = datetime.fromisoformat(query['begin'])
    end_date = datetime.fromisoformat(query['end'])
    query = '''
        SELECT *
        FROM registrations
        WHERE registrations.datetime BETWEEN (%s) AND (%s);'''
    conn = get_db()
    with conn.cursor() as c:
        c.execute(query, [begin_date, end_date])
        res = c.fetchall()
    return res

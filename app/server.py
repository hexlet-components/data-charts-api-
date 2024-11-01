import logging
import os
import traceback
from datetime import datetime

import psycopg
from dotenv import load_dotenv
from flask import Flask, request
from psycopg.rows import dict_row

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
    try:
        begin_date = datetime.fromisoformat(query['begin'])
        end_date = datetime.fromisoformat(query['end'])
    except ValueError as e:
        logging.error(traceback.format_exc(2, chain=False))
        return 'Invalid date. Please check your input', 400
    query = '''
        SELECT *
        FROM visits
        WHERE visits.datetime BETWEEN (%s) AND (%s);'''
    conn = get_db()
    with conn.cursor(row_factory=dict_row) as c:
        c.execute(query, [begin_date, end_date])
        res = c.fetchall()
    return res


@app.get('/registrations')
def get_registrations():
    query = request.args
    try:
        begin_date = datetime.fromisoformat(query['begin'])
        end_date = datetime.fromisoformat(query['end'])
    except ValueError as e:
        logging.error(traceback.format_exc(2, chain=False))
        return 'Invalid date. Please check your input', 400
    query = '''
        SELECT *
        FROM registrations
        WHERE registrations.datetime BETWEEN (%s) AND (%s);'''
    conn = get_db()
    with conn.cursor(row_factory=dict_row) as c:
        c.execute(query, [begin_date, end_date])
        res = c.fetchall()
    return res

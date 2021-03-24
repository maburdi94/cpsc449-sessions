#!/usr/bin/env python3

import sys
import logging.config

import bottle
from bottle import get, post, request, response, template, redirect

import uuid
import requests

# Set up app and logging
app = bottle.default_app()
app.config.load_config('./etc/app.ini')

logging.config.fileConfig(app.config['logging.config'])

KV_URL = app.config['sessions.kv_url']

# Disable Resource warnings produced by Bottle 0.12.19 when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore', ResourceWarning)


@get('/')
def show_form():

    # Get the session_id from a cookie
    sessionId = request.get_cookie('session-id', default=str(uuid.uuid4()) )

    # Get session data for session_id
    r = requests.get(f'{KV_URL}/{sessionId}').json()
    sessionData = r.get(sessionId) or {}

    count1 = sessionData.get('count1') or 0
    count2 = sessionData.get('count2') or 0

    count1 = int(count1) + 1

    sessionData['count1'] = count1
    sessionData['count2'] = count2

    requests.put(f'{KV_URL}/', json={sessionId: sessionData})

    response.set_cookie('session-id', sessionId)

    return template('counter.tpl', counter1=count1, counter2=count2)


@post('/increment')
def increment_count2():

    # Get the session_id from a cookie
    sessionId = request.get_cookie('session-id')

    # Get session data for session_id
    r = requests.get(f'{KV_URL}/{sessionId}').json()
    sessionData = r.get(sessionId) or {}

    count2 = sessionData.get('count2') or 0
    count2 = int(count2) + 1
    sessionData['count2'] = count2

    requests.put(f'{KV_URL}/', json={sessionId: sessionData})

    return redirect('/')


@post('/reset')
def reset_counts():
    
    # Get the session_id from a cookie
    sessionId = request.get_cookie('session-id')

    r = requests.delete(f'{KV_URL}/{sessionId}').json()

    return redirect('/')

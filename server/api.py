# -*- coding: utf-8 -*-

import validators
from flask import Blueprint, current_app, jsonify, request
from flask import redirect
from flask import abort, render_template
from urlparse import urlparse
from server.db import connect_db
from server.db import close_db

api = Blueprint('api', __name__)

@api.route('/_ah/search', methods=['GET'])
def search():
    link = request.args.get('link', "", str)

    if not bool(urlparse(link).scheme):
        link = "http://" + link

    if validators.url(link, require_tld = True):
        print request.host_url
        url = "{}{}/".format(request.host_url,
                         current_app.word.find_word(link))
        return jsonify({'url' : url})
    else:
        return jsonify({'error' : 
               "Unable to shorten that link. It is not a valid url."})

@api.route('/<shorten>/', methods=['GET'])
def redirect_request(shorten):
    url = current_app.word.find_url(shorten)
    if bool(url):
        return redirect(url, code=302)
    else:
        abort(404)

@api.before_request
def before_request():
    connect_db()

@api.teardown_request
def teardown_request(exception):
    close_db()

#!/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker ( ospalh@gmail.com )
# Original: 2012 Nicolas Perriault,
# https://nicolas.perriault.net/code/2012/dead-easy-yet-powerful-static-website-generator-with-flask/
# License: Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) 

import sys
from flask import Flask, render_template, send_file
from flaskext.flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True
app.config['SERVER_PORT'] = 8080
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    addons_pages = [p for p in pages if 'addon' in p.meta.get('type', [])]
    return render_template('index.html', pages=addons_pages)


@app.route('/<path:path>.html')
def page(path):
    page = pages.get_or_404(path)
    return render_template('addon.html', page=page)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/images/<fname>.png')
def get_png(fname):
    filename = 'images/' + fname + '.png'
    return send_file(filename, mimetype='image/png')

@app.route('/images/<fname>.jpg')
def get_jpg(fname):
    filename = 'images/' + fname + '.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.route('/scripts/<fname>.js')
def get_js(fname):
    filename = 'scripts/' + fname + '.js'
    return send_file(filename, mimetype='application/javascript')

@app.route('/css/<fname>.css')
def get_css(fname):
    filename = 'css/' + fname + '.css'
    return send_file(filename, mimetype='text/css')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=app.config.get('SERVER_PORT'))

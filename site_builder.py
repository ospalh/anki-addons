#!/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker ( ospalh@gmail.com )
# Original: 2012 Nicolas Perriault,
# HTTPS://nicolas.perriault.net/code/2012/\
# dead-easy-yet-powerful-static-website-generator-with-flask/
# License: Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)

import sys
from flask import Flask, render_template, send_file
from flask_flatpages import FlatPages
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


@app.route('/anki-addons/')
def index():
    addons = [p for p in pages if 'addon' in p.meta.get('type', [])]
    addons = sorted(addons, reverse=True, key=lambda p: p.meta['date'])
    green_addons = [p for p in addons if
                    'green' in p.meta.get('status_color', [])]
    yellow_addons = [p for p in addons if
                     'yellow' in p.meta.get('status_color', [])]
    red_addons = [p for p in addons if
                  'red' in p.meta.get('status_color', [])]
    return render_template('index.html', green=green_addons,
                           yellow=yellow_addons, red=red_addons)


@app.route('/anki-addons/<path:path>.html')
def page(path):
    page = pages.get_or_404(path)
    if 'addon' in page.meta.get('type', []):
        return render_template('addon.html', page=page)
    elif 'subpage' in page.meta.get('type', []):
        return render_template('subpage.html', page=page)
    elif 'other_page' in page.meta.get('type', []):
        return render_template('other.html', page=page)


# Generate URLs for all the sub-page md files
@freezer.register_generator
def page():
    for sub_page in pages:
        if 'subpage' in sub_page.meta.get('type', []):
            yield {'path': sub_page.path}


@app.route('/anki-addons/images/<fname>.png')
def get_png(fname):
    filename = 'images/' + fname + '.png'
    return send_file(filename, mimetype='image/png')


@app.route('/anki-addons/images/<fname>.jpg')
def get_jpg(fname):
    filename = 'images/' + fname + '.jpg'
    return send_file(filename, mimetype='image/jpg')


@app.route('/anki-addons/scripts/<fname>.js')
def get_js(fname):
    filename = 'scripts/' + fname + '.js'
    return send_file(filename, mimetype='application/javascript')


@app.route('/anki-addons/css/<fname>.css')
def get_css(fname):
    filename = 'css/' + fname + '.css'
    return send_file(filename, mimetype='text/css')


@app.route('/anki-addons/css/<fname>.less')
def get_less(fname):
    filename = 'css/' + fname + '.less'
    return send_file(filename, mimetype='text/css')


#@freezer.register_generator
#def css():
#    for script_file in css.all():
#        yield script_file


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        # freezer.run(debug=True)
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=app.config.get('SERVER_PORT'))

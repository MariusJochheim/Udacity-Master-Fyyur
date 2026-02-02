#----------------------------------------------------------------------------#
# Main routes
#----------------------------------------------------------------------------#

from flask import render_template

from extensions import app


@app.route('/')
def index():
    return render_template('pages/home.html')

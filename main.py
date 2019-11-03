import os
import json
import requests
import random
import fireo
import lib.google_auth as google_auth
from flask import Flask, render_template, request, url_for, redirect, session, flash

from lib.db.ghost_record import GhostRecord
from lib.db.user import User
from forms.user_info_input import UserInfoInput

# init Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.register_blueprint(google_auth.app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def home():
    rec = []
    result = GhostRecord.get_allocated_ghost()
    for r in result:
        rec.append({'ghost': r.name,
                    'user': r.user_ghost_name,
                    'email': r.user_email})

    if google_auth.is_logged_in():
        login = True
        email = session['user_email']
        if not GhostRecord.has_record(email):
            message = "Get a Phantom name"
        else:
            message = "Change your phantom name"
    else:
        message = "Get a Phantom name"
        login = False
        email = None

    # set this as global variable for all templates
    app.jinja_env.globals['login'] = login
    app.jinja_env.globals['email'] = email

    return render_template('home.html', record=rec, btn=message)

@app.route('/ghost_name_form', methods=['GET', 'POST'])
def ghost_name_form():
    if google_auth.is_logged_in():
        input_form = UserInfoInput(request.form)

        if request.method == 'POST':
            val = {'first_name': request.form['first_name'],
                   'last_name': request.form['last_name']}

            session['user_input'] = val

            if input_form.validate():
                return redirect(url_for("ghost_name_recommendation"))
            else:
                flash('All the form fields are required.')

        return render_template('form.html', form=input_form)

    else:
        return redirect(url_for("google_auth.login"))

@app.route('/ghost_name_recommendation', methods=['GET', 'POST'])
def ghost_name_recommendation():
    user_input = session.get('user_input', None)

    if user_input is None:
        return redirect(url_for("ghost_name_form"))

    result = GhostRecord.get_unallocated_ghost()
    rand = random.sample([record.name for record in result], 3)

    end_result = [user_input.get('first_name') + " '" + choice + "' " + user_input.get('last_name') for choice in rand]
    print(rand)
    print(end_result)
    mapping = zip(rand, end_result)

    if request.method == 'POST':
        ghost_name = request.form['ghost_name']
        user_ghost_name = request.form['ghost_user_name']

        print(ghost_name, "->", user_ghost_name)
        # reset the current used ghostname
        GhostRecord.reset(session['user_email'])

        ghost = GhostRecord.get_single_ghost(ghost_name)
        ghost.picked = True
        ghost.user_email = session['user_email']
        ghost.user_first_name = user_input.get('first_name')
        ghost.user_last_name = user_input.get('last_name')
        ghost.user_ghost_name = user_ghost_name
        ghost.update()
        session['ghost_name'] = [ghost_name]

        return redirect(url_for("home"))

    return render_template('suggestions.html', recommendation=mapping)

if __name__ == '__main__':
    app.run(debug=True)

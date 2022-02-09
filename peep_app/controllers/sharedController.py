from flask import Flask, redirect, render_template, session
from peep_app import app
from peep_app.models import userModel, countryModel, postModel

@app.route('/dashboard', methods=['GET'])
def dashboard():
    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

        currentUser = userModel.User.findUserById({'userId': userId})

        # Si hay userId pero no encuentra un usuario, hace logout
        if currentUser == None:
            return redirect('/logout')

        # posts = postModel.Post.get_all({'userId': userId})

        return render_template(
            'dashboard.html',
            currentUser = currentUser,
            isLogged = isLogged,
            # posts = posts
        )
    else:
        return redirect('/')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def index():
    isLogged = False

    if 'userId' in session:
        isLogged = True
        return redirect('/dashboard')

    countries = countryModel.Country.get_all()

    return render_template(
        "index.html",
        isLogged = isLogged,
        countries = countries
    )


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/blocked', methods=['GET'])
def blocked():
    return render_template('blocked.html')

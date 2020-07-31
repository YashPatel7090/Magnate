from flask import Flask, render_template, url_for, redirect, request, abort
import sys
sys.path.insert(1, 'services')
from compute import User


Magnate = Flask(__name__)
temp_login_user_objects = {}
temp_signup_user_objects = {}


@Magnate.route('/')
def home():
    return render_template('home.html')


@Magnate.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        login_user = User(username, email, password)
        hashed_email_url = login_user.hashed_email_url

        global temp_login_user_objects
        temp_login_user_objects[f'{hashed_email_url}'] = login_user

        return redirect(url_for('login_active', user_id_url = hashed_email_url), code=307)


@Magnate.route('/login/active/<user_id_url>', methods=['POST'])
def login_active(user_id_url):
    login_user = temp_login_user_objects[f'{user_id_url}']
    if login_user.is_verified():
        if login_user.secure_login():
            return redirect(url_for('user_data', user_id_url = user_id_url), code=307)
        else:
            return render_template('login.html', incorrect_credentials = True)
    elif login_user.is_unverified():
        return render_template('login.html', email_already_sent = True, user_email = login_user.email)
    elif login_user.is_verified() == False and login_user.is_unverified() == False:
        return render_template('login.html', click_signup = True)


@Magnate.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    signup_user = User(username, email, password)
    hashed_email_url = signup_user.hashed_email_url

    global temp_signup_user_objects
    temp_signup_user_objects[f'{hashed_email_url}'] = signup_user

    return redirect(url_for('signup_active', user_id_url = hashed_email_url), code=307)


@Magnate.route('/signup/active/<user_id_url>', methods=['POST'])
def signup_active(user_id_url):
    signup_user = temp_signup_user_objects[f'{user_id_url}']
    if signup_user.is_verified():
        return render_template('login.html', account_already_exists = True, user_email = signup_user.email)
    elif signup_user.is_unverified():
        return render_template('login.html', email_already_sent = True, user_email = signup_user.email)
    elif signup_user.is_verified() == False and signup_user.is_unverified() == False:
        if signup_user.send_verification_email():
            return render_template('signup.html', username = signup_user.username, email = signup_user.email)
        else:
            return render_template('login.html', send_failure = True, user_email = signup_user.email)


@Magnate.route('/signup/verified/<url>')
def verify_account(url):
    if User.url_is_unverified(url):
        User.verify_user(url)
        return render_template('login.html', verified = True)
    else:
        return redirect(url_for('login'))


@Magnate.route('/account/user/data/<user_id_url>', methods=['POST'])
def user_data(user_id_url):
    user = temp_login_user_objects[f'{user_id_url}']
    data = user.extract_data()
    return render_template('user_data.html', data = data)


@Magnate.route('/clear/temp/user/objects/<user_id_url>', methods=['POST'])
def clear_temp_user_objects(user_id_url):
    global temp_login_user_objects
    global temp_signup_user_objects
    if request.form.get('NAME') == 'LOGIN' or request.data.decode('utf-8') == 'LOGIN':
        if user_id_url in temp_login_user_objects:
            temp_login_user_objects.pop(f'{user_id_url}')
            return redirect(url_for('login'))
        return redirect(url_for('login'))
    elif request.form.get('NAME') == 'SIGNUP' or request.data.decode('utf-8') == 'SIGNUP':
        if user_id_url in temp_signup_user_objects:
            temp_signup_user_objects.pop(f'{user_id_url}')
            return redirect(url_for('login'))
        return redirect(url_for('login'))
    elif request.data.decode('utf-8') == 'EITHER':
        if user_id_url in temp_login_user_objects:
            temp_login_user_objects.pop(f'{user_id_url}')
            return redirect(url_for('login'))
        elif user_id_url in temp_signup_user_objects:
            temp_signup_user_objects.pop(f'{user_id_url}')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))


@Magnate.errorhandler(404)
def handle_404(error):
    return render_template('handle_404.html')


@Magnate.errorhandler(405)
def handle_405(error):
    return redirect(url_for('home'))


@Magnate.errorhandler(KeyError)
def handle_KeyError(error):
    return redirect(url_for('login'))


if __name__ == "__main__":
    Magnate.run(debug=True)


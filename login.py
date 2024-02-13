from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import qrcode
import io
from base64 import b64encode

import play_store_reviews
import app_store_reviews
from find_app_id import AppFinder

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = pyotp.random_base32()

logged_in = False


# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return b64encode(img_io.getvalue()).decode()


@app.route('/', methods=['POST', 'GET'])
def login():
    global logged_in

    # Ensure that the TOTP secret is consistent for the session
    if 'totp_secret' not in session:
        session['totp_secret'] = pyotp.random_base32()

    totp_secret = session['totp_secret']
    totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name='user', issuer_name='Reviews App')
    qr_code = generate_qr_code(totp_uri)

    if request.method == 'POST':
        totp_code = request.form['totp_code']
        totp = pyotp.TOTP(totp_secret)
        if totp.verify(totp_code):
            print("verified")
            logged_in = True
            return redirect('/welcome')
        else:
            return render_template('login.html', qr_code=qr_code, error="Incorrect password")

    return render_template('login.html', qr_code=qr_code)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/welcome', methods=['POST', 'GET'])
def landing_page():
    if not logged_in:
        print("NOT LOGGED IN")
        return redirect('/')
    if request.method == 'POST':
        app_name = request.form.get('app_name')
        search_period = request.form.get('search_period')
        return show_review_report(app_name, search_period)

    return show_landing_page()


def show_landing_page():
    return render_template('landing.html')


def show_review_report(app_name, search_period):
    app_search = AppFinder()
    app_search.find_app(app_name)

    days = {
        'month': 30,
        'quarter': 91,
        'half-year': 182,
        'year': 365,
        'whole-period': -1
    }[search_period]

    df_google_reviews = play_store_reviews.get_reviews(days, app_search.google_id)

    df_appsto_reviews = app_store_reviews.get_reviews(days, app_search.apple_id)

    if len(df_google_reviews) > 0:
        google_reviews = [df_google_reviews.to_html(classes="data", header=True)]
    else:
        google_reviews = []

    if len(df_appsto_reviews) > 0:
        appstore_reviews = [df_appsto_reviews.to_html(classes="data", header=True)]
    else:
        appstore_reviews = []

    return render_template('forumreport.html',
                           google_reviews=google_reviews,
                           appstore_reviews=appstore_reviews)


if __name__ == '__main__':
    app.run(debug=True)


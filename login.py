from flask import Flask, render_template, request, redirect, session
import pyotp
import qrcode
import io
from base64 import b64encode

from qrcode.main import QRCode

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = pyotp.random_base32()


def generate_qr_code(data):
    """
        Function to generate a QR code from the provided data.

        Parameters:
        data (str): The data to be encoded into the QR code.

        Returns:
        str: The generated QR code as a base64 encoded string.
    """

    qr = QRCode(
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


def login():
    """
        Function to generate a QR code from the provided data.

        Parameters:
        data (str): The data to be encoded into the QR code.

        Returns:
        str: The generated QR code as a base64 encoded string.
    """

    if 'totp_secret' not in session:
        session['totp_secret'] = pyotp.random_base32()

    totp_secret = session['totp_secret']
    totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name='user', issuer_name='Reviews App')
    qr_code = generate_qr_code(totp_uri)

    if request.method == 'POST':
        totp_code = request.form['totp_code']
        totp = pyotp.TOTP(totp_secret)
        if totp.verify(totp_code):
            session['logged_in'] = True
            print("verified")
            return redirect('/')
        else:
            return render_template('login.html', qr_code=qr_code, error="Incorrect password")

    return render_template('login.html', qr_code=qr_code)


def logout():
    """
        Function to handle user logout.

        The user's login status is removed from the session and the user is redirected to the home page.

        Returns:
        str: The redirect response to the home page.
    """
    session.pop('logged_in', None)
    return redirect('/')

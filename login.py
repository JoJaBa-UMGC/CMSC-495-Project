from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import qrcode
import io
from base64 import b64encode

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = pyotp.random_base32()


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
            return render_template('landing.html')
        else:
            return render_template('login.html', qr_code=qr_code, error="Incorrect password")

    return render_template('login.html', qr_code=qr_code)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

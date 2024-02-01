import io
import app_store_reviews
import find_app_id
import play_store_reviews
from flask import Flask, render_template, send_file
from pandas.core.interchange import dataframe


app = Flask(__name__, template_folder='templates', static_folder='static')


APP_NAME = 'mighty doom'
DAYS = 30
google_id = ""
apple_id = ""


@app.route('/')
def csv_test():
    global google_id, apple_id
    app_ids = find_app_id.AppFinder()
    app_ids.find_app(APP_NAME)
    google_id = app_ids.google_id
    apple_id = app_ids.apple_id
    return render_template('csv_test.html')


@app.post("/google")
def google_csv():
    global google_id
    generate_csv_zip(play_store_reviews.get_reviews(DAYS, google_id), "Google Reviews")
    return render_template('csv_test.html')


@app.post("/apple")
def apple_csv():
    global apple_id
    generate_csv_zip(app_store_reviews.get_reviews(DAYS, apple_id), "Apple Reviews")
    return render_template('csv_test.html')


def generate_csv_zip(reviews_dataframe: dataframe, file_name: str):
    file_name += '.csv'
    file_buffer = io.BytesIO()
    file_buffer.name = file_name
    reviews_dataframe.to_csv(file_buffer)
    file_buffer.seek(0)
    print(file_name + ' should have been generated!')
    return send_file(file_buffer, mimetype="text/csv", download_name=file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

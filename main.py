import os

from ExtractTable import ExtractTable
from flask import Flask, send_file
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField
from wtforms.validators import InputRequired
from flask_cors import CORS


app = Flask(__name__)
API_KEY = os.getenv("ET_API")
CORS(app)


app.config["SECRET_KEY"] = "secret"
app.config["UPLOAD_FOLDER"] = "static/files"


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])


@app.route("/")
@app.route("/hello")
def hello_world():
    return "Hello World!"


@app.route("/check-usage")
def check_usage():
    et_sess = ExtractTable(api_key=API_KEY)
    et_usage = et_sess.check_usage()

    return et_usage


@app.route("/process-image", methods=["POST"])
def process_image():
    form = UploadFileForm()

    file = form.file.data

    file_name = secure_filename(file.filename)
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], file_name)

    # TODO: Delete file later
    file.save(file_path)

    # TODO: Handle PDFs
    et_sess = ExtractTable(api_key=API_KEY)
    csv_file = et_sess.process_file(filepath=file_path, output_format="csv")[0]

    return {"file": csv_file}


@app.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    path = filename

    return send_file(f"/{path}", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

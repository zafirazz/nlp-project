from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField
from wtforms.fields.simple import SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import csv
import fitz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired(), FileAllowed(ALLOWED_EXTENSIONS, "Only .pdf, txt, doc, docx are allowed")])
    submit = SubmitField("Upload")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_pdf(file, output_folder='data'):
    csv_filepath = os.path.join(output_folder, 'test_data.csv')

    txt_data = []

    with fitz.open(file) as pdf:
        for num, page in enumerate(pdf, start=1):
            page_text = page.get_text()
            txt_data.append([f"Page {num}", page_text])

    with open(csv_filepath, 'w', encoding="utf-8", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Page Number", "Content"])
        csv_writer.writerows(txt_data)

    print(f"Extracted {csv_filepath}")
    return csv_filepath

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)
            csv_filepath = extract_text_pdf(file_path, output_folder='data')
            return "File has been uploaded"
    return render_template("index.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
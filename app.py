import csv
import os
import fitz
import streamlit as st

st.set_page_config(page_title="PDF Text Extractor", layout="wide")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
OUTPUT_FOLDER = "data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

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

st.title("PDF Text Extractor")
st.write("Upload a PDF file to extract its text into a CSV format.")

uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt', 'doc', 'docx'])

if uploaded_file is not None:
    if allowed_file(uploaded_file.name):
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded successfully: {uploaded_file.name}")

        csv_filepath = extract_text_pdf(file_path, OUTPUT_FOLDER)
        st.success(f"Text extracted successfully to: {csv_filepath}")

        with open(csv_filepath, "rb") as f:
            csv_data = f.read()
        st.download_button(
            label="Download Extracted CSV",
            data=csv_data,
            file_name="extracted_data.csv",
            mime="text/csv"
        )
    else:
        st.error("Unsupported file type. Please upload a valid file.")
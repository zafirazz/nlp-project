import csv
import os
import fitz
import streamlit as st

st.set_page_config(page_title="Notes organizer", layout="wide")

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

st.title("Notes Organizer")
st.write("Upload your Note.")

uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt', 'doc', 'docx'])

if uploaded_file is not None:
    if allowed_file(uploaded_file.name):
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded successfully: {uploaded_file.name}")

        csv_filepath = extract_text_pdf(file_path, OUTPUT_FOLDER)

        with open(csv_filepath, "rb") as f:
            csv_data = f.read()
    else:
        st.error("Unsupported file type. Please upload a valid file.")

st.divider()
st.subheader("Your Notes")
st.caption("All your uploaded files are considered as notes and classified with tags.")
files = os.listdir(UPLOAD_FOLDER)

if files:
    for i in range(0, len(files), 4):
        cols = st.columns(4)
        for col, file_name in zip(cols, files[i:i+6]):
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            csv_filepath = os.path.join(OUTPUT_FOLDER, file_name)

            with col:
                st.image("/Users/zafiraibraeva/Code/uni coding/nlp-project/static/note_logo.png", width=40)
                st.write(file_name)

                with st.expander("•••", expanded=False):
                    if st.button(f"Download {file_name}", key=f"download_{file_name}"):
                        st.download_button(label=f"Download",
                                           data=open(file_path, "rb").read(),
                                           file_name=f"{file_name}")
                    if st.button(f"Delete {file_name}", key=f"delete_{file_name}"):
                        os.remove(file_path)
                        if os.path.exists(csv_filepath):
                            os.remove(csv_filepath)
else:
    st.info("No files uploaded")

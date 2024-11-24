import csv
import os
import fitz
import streamlit as st
from nlp_task import process_file_and_generate_tags

st.set_page_config(page_title="Notes organizer", layout="wide")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
OUTPUT_FOLDER = "data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
TAGS_FILE = os.path.join(OUTPUT_FOLDER, 'tags.csv')

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

def load_tags():
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return {rows[0]: rows[1] for rows in reader}
    return {}

def save_tags(tags_dict):
    with open(TAGS_FILE, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        for file, tags in tags_dict.items():
            writer.writerow([file, tags])

st.title("Notes Organizer")
st.write("Upload your Note.")

existing_tags = load_tags()

uploaded_file = st.file_uploader("Choose a file", type=ALLOWED_EXTENSIONS)

if uploaded_file is not None:
    if allowed_file(uploaded_file.name):
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded successfully: {uploaded_file.name}")

        csv_filepath = extract_text_pdf(file_path)

        output_csv_path = os.path.join(OUTPUT_FOLDER, 'processed_' + uploaded_file.name.replace('.pdf', '.csv'))
        tags_dict = process_file_and_generate_tags(csv_filepath, output_csv_path)
        existing_tags = load_tags()
        existing_tags[uploaded_file.name] = ", ".join(tags_dict.keys())
        save_tags(existing_tags)

        st.subheader(f"File: {uploaded_file.name}")
        st.write(f"Tags: {existing_tags[uploaded_file.name]}")
    else:
        st.error("Unsupported file type. Please upload a valid file.")

st.divider()
st.subheader("Your Notes")
st.caption("All your uploaded files are considered as notes and classified with tags.")
files = os.listdir(UPLOAD_FOLDER)
existing_tags = load_tags()

if files:
    for i in range(0, len(files), 4):
        cols = st.columns(4)
        for col, file_name in zip(cols, files[i:i+4]):
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            with col:
                st.image("static/note_logo.png", width=40)
                st.write(file_name)

                with st.expander("•••", expanded=False):
                    st.write(f"Tags: {existing_tags.get(file_name, 'No tags yet')}")
                    new_tags = st.text_input(f"Edit tags for {file_name}", value=existing_tags.get(file_name, ""))
                    if st.button(f"Save tags for {file_name}", key=f"save_{file_name}"):
                        existing_tags[file_name] = new_tags
                        save_tags(existing_tags)
                        st.success(f"Tags for {file_name} updated!")

                    if st.button(f"Download {file_name}", key=f"download_{file_name}"):
                        st.download_button(label=f"Download {file_name}",
                                           data=open(file_path, "rb").read(),
                                           file_name=f"{file_name}")

                    if st.button(f"Delete {file_name}", key=f"delete_{file_name}"):
                        os.remove(file_path)
                        if os.path.exists(os.path.join(OUTPUT_FOLDER, 'processed_' + file_name.replace('.pdf', '.csv'))):
                            os.remove(os.path.join(OUTPUT_FOLDER, 'processed_' + file_name.replace('.pdf', '.csv')))
                        st.success(f"{file_name} deleted!")
else:
    st.info("No files uploaded yet.")
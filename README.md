# Lecture notes organizer

Following project was developed as an exam for Introduction to Natural Language Processing class. Notes organizer is a simple web application that organizes uploaded notes by tags. Tags are identiefied using NLP techniques. 

# Tech stack
- Python 3.8+
- Streamlit

# Overview
<img width="1483" alt="image" src="https://github.com/user-attachments/assets/5ec26414-2e12-4c4f-8dd6-8fa5ed41392f">

<img width="738" alt="Screenshot 2024-11-24 at 17 20 10" src="https://github.com/user-attachments/assets/20221577-e391-4b14-b1c8-867cadc8e9ec">

In order to use this application: Upload file (it accepts .pdf, .doc, .docx only) As soon as file was uploaded, below in "Your Notes" section you can check for the file with generated tags and feature to download the file or delete it instead. 

During the Natural Language Processing Class, we covered techniques that I also used in the project:
- Preprocesses text by:
    - Removing punctuation, numbers, and stopwords.
    - Lemmatizing content for normalization.
- Generates meaningful tags using KeyBERT with a transformer-based language model.

In order to run the application on your device, install required packages and run app.py using command **streamlit run app.py**


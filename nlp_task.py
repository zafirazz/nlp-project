import os
import pandas as pd
from tqdm import tqdm
from collections import Counter
from keybert import KeyBERT
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


def preprocess_text(df: pd.DataFrame) -> pd.DataFrame:
    def remove_punctuation(text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def remove_numbers(text):
        return ''.join([i for i in text if not i.isdigit()])

    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        return ' '.join([w for w in word_tokens if w.lower() not in stop_words])

    def lemmatize_text(text):
        lemmatizer = WordNetLemmatizer()
        word_tokens = word_tokenize(text)
        return ' '.join([lemmatizer.lemmatize(w) for w in word_tokens])

    tqdm.pandas()
    df['Content'] = df['Content'].str.lower()
    df['Content'] = df['Content'].progress_apply(remove_punctuation)
    df['Content'] = df['Content'].progress_apply(remove_numbers)
    df['Content'] = df['Content'].progress_apply(remove_stopwords)
    df['Content'] = df['Content'].progress_apply(lemmatize_text)

    return df


def generate_tags(df: pd.DataFrame, num_tags_per_page: int = 3) -> (pd.DataFrame, dict):
    kw_model = KeyBERT('sentence-transformers/all-MiniLM-L6-v2')

    def extract_tags(text):
        try:
            keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num_tags_per_page)
            return [kw[0] for kw in keywords]
        except Exception:
            return []

    tqdm.pandas()
    df['Tags'] = df['Content'].progress_apply(extract_tags)

    all_tags = [tag for tags in df['Tags'] for tag in tags]
    top_tags_dict = {tag: count for tag, count in Counter(all_tags).most_common(num_tags_per_page)}

    return df, top_tags_dict


def process_file_and_generate_tags(csv_path: str, output_csv_path: str, num_tags: int = 3) -> dict:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Input CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    df = preprocess_text(df)
    df.to_csv(output_csv_path, index=False)

    df, top_tags_dict = generate_tags(df, num_tags_per_page=num_tags)

    df.to_csv(output_csv_path, index=False)

    return top_tags_dict

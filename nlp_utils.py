# nlp_utils.py
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import re


def predict_difficulty_level(question_text, solution_text):

    combined_text = (question_text or "") + " " + (solution_text or "")

    length = len(combined_text)
    if length < 200:
        difficulty = "Easy"
    elif length < 500:
        difficulty = "Medium"
    else:
        difficulty = "Hard"

    combined_text_lower = combined_text.lower()

    if "complex" in combined_text_lower or "advanced" in combined_text_lower:
        difficulty = "Hard"
    elif "basic" in combined_text_lower or "fundamental" in combined_text_lower:
        difficulty = "Easy"

    return difficulty


def assess_option_confusingness(options):

    option_texts = [option['description'] or "" for option in options]
    num_options = len(option_texts)

    if num_options < 2:
        return 0

    avg_length = np.mean([len(text) for text in option_texts])

    total_common_words = 0

    for i in range(num_options):
        for j in range(i + 1, num_options):

            words1 = set(re.findall(r'\b\w+\b', option_texts[i].lower()))
            words2 = set(re.findall(r'\b\w+\b', option_texts[j].lower()))

            stop_words = set(stopwords.words('english'))
            words1 -= stop_words
            words2 -= stop_words

            common_words = words1.intersection(words2)
            total_common_words += len(common_words)

    avg_common_words = total_common_words / \
        (num_options * (num_options - 1) / 2) if num_options > 1 else 0

    confusingness = avg_common_words * avg_length / 100

    return confusingness

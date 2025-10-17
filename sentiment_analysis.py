from utils.neutral_words import neutral_words
from utils.positive_words import positive_words
from utils.negative_words import negative_words
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client.get_database("textminer")
sentences_collection = database.get_collection("sentences")
words_collection = database.get_collection("words")
analysis_collection = database.get_collection("analysis")
analysis_doc_id = "default"


analysis_collection.delete_many({})
analysis_collection.insert_one({"id": analysis_doc_id})


# TEXT FILE -> Paragraphs -> Sentences -> Words (negative word / positive word / neutral word)

def is_empty(text):
    text = text.strip()
    return len(text) == 0


def score_paragraph(paragraph):
    if is_empty(paragraph):
        pass
    paragraph_score = 0
    sentences = paragraph.split(".")
    analysis_collection.update_one(
        {"id": analysis_doc_id},
        {"$inc": {
            "total_paras": 1,
        }}
    )
    total_number_of_sentences = len(sentences)
    analysis_collection.update_one(
        {"id": analysis_doc_id},
        {"$inc": {
            "total_number_of_sentences": total_number_of_sentences,
        }}
    )
    for i, sentence in enumerate(sentences):
        sentence_score = score_sentence(sentence)
        sentiment = "Negative"
        if sentence_score > 0:
            analysis_collection.update_one(
                {"id": analysis_doc_id},
                {"$inc": {
                    "total_positive_sentences": 1,
                }}
            )
            sentiment = "Positive"
        if sentence_score == 0:
            sentiment = "Neutral"
        if sentiment == "Negative":
            analysis_collection.update_one(
                {"id": analysis_doc_id},
                {"$inc": {
                    "total_negative_sentences": 1,
                }}
            )
        mydict = {"sentence": sentence, "score": sentence_score, "sentiment": sentiment}
        sentences_collection.insert_one(mydict)
        paragraph_score += sentence_score
    analysis_collection.update_one(
        {"id": analysis_doc_id},
        {"$inc": {
            "total_score": paragraph_score,
        }}
    )
    return paragraph_score


def score_sentence(sentence: str):
    """
    Analyze score for given sentence.
    :param sentence: Sentence to be analyzed
    :return: sentiment score for the sentence
    """
    if is_empty(sentence):
        pass
    res = 0
    words = sentence.split()
    total_number_of_words = len(words)
    analysis_collection.update_one(
        {"id": analysis_doc_id},
        {"$inc": {
            "total_number_of_words": total_number_of_words,
        }}
    )
    for i, word in enumerate(words):
        word_score = analyze_word(word)
        available_in_dict = is_available_in_dict(word)
        if available_in_dict:
            analysis_collection.update_one(
                {"id": analysis_doc_id},
                {"$inc": {
                    "total_dict_hits": 1,
                }}
            )
        else:
            analysis_collection.update_one(
                {"id": analysis_doc_id},
                {"$inc": {
                    "total_dict_miss": 1,
                }}
            )
        word_dict = {"word": word, "score": word_score, "is_available_in_dict": available_in_dict}
        words_collection.insert_one(word_dict)
        res += word_score
    return res


def analyze_word(word):
    if is_empty(word):
        pass
    """
    Analyze score for given word.
    :param word: word to be analyzed
    :return: sentiment score for the word
    """
    is_positive = positive_check(word)
    is_negative = negative_check(word)
    if is_positive:
        analysis_collection.update_one(
            {"id": analysis_doc_id},
            {"$inc": {
                "total_positive_words": 1,
            }}
        )
        return 1
    if is_negative:
        analysis_collection.update_one(
            {"id": analysis_doc_id},
            {"$inc": {
                "total_negative_words": 1,
            }}
        )
        return - 1
    return 0  # if neutral


def positive_check(word):
    return word in positive_words


def negative_check(word):
    return word in negative_words


def neutral_check(word):
    return word in neutral_words


def is_available_in_dict(word):
    is_in_positive = positive_check(word)
    is_in_negative = negative_check(word)
    is_in_neutral = neutral_check(word)
    return is_in_positive or is_in_negative or is_in_neutral

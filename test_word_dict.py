from utils.positive_words import positive_words
from utils.negative_words import negative_words
from utils.neutral_words import neutral_words

sample_sentences = [
'The sun is shining brightly today',
'I love reading interesting books',
'She is practicing the piano every evening',
'They went to the park for a picnic',
'We are planning a trip to the mountains',
'He does not like waking up early',
'The weather is not very pleasant today'
"The weather was terrible and ruined our plans",
"She felt hopeless after receiving the bad news",
"The movie was boring and completely disappointing",
"He spoke in a rude and disrespectful manner",
"The food tasted awful and made everyone sick"
]


def positive_check(word):
    return word in positive_words


def negative_check(word):
    return word in negative_words


def neutral_check(word):
    return word in neutral_words

for sentence in sample_sentences:
    sentence_score = 0
    words = sentence.split()
    for test_word in words:
        score = 0
        is_positive = positive_check(test_word)
        is_negative = negative_check(test_word)
        is_neutral = neutral_check(test_word)
        if is_positive:
            score = score + 1
        if is_negative:
            score = score - 1
        sentence_score += score
    print(f"{sentence} ===> {sentence_score}")

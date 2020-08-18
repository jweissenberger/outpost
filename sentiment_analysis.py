import flair
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from common import sentence_tokenizer


def flair_sentiment_analysis(text):
    """
    Measures how positive or negative the sentiment of the article is

    Seems to rate neutral sentences as positive

    :param text:
    :return:
    pos_or_neg: string 'POSITIVE' or 'NEGATIVE'
    score: value from 0.0 to 1 on how positive or negative
    """
    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

    s = flair.data.Sentence(text)
    flair_sentiment.predict(s)
    total_sentiment = s.labels
    pos_or_neg = total_sentiment[0].value  # either the string 'POSITIVE' or 'NEGATIVE'
    score = total_sentiment[0].score
    return pos_or_neg, score


def flair_sentence_by_sentence_sentiment_analysis(text):

    sentences = sentence_tokenizer(text)

    positive_sentences = []
    negative_sentences = []

    for sentence in sentences:
        positive_or_negative, score = flair_sentiment_analysis(sentence)

        if positive_or_negative == 'POSITIVE':
            positive_sentences.append((score, sentence))
        else:
            negative_sentences.append((score, sentence))

    positive_sentences = sorted(positive_sentences, key=lambda x: x[0])
    negative_sentences = sorted(negative_sentences, key=lambda x: x[0])

    return positive_sentences, negative_sentences


def flair_average_sentiment(text):
    positive_sentences, negative_sentences = flair_sentence_by_sentence_sentiment_analysis(text)

    pos = 0
    neg = 0
    for i in positive_sentences:
        pos += i[0]
    pos = pos/len(positive_sentences)

    for j in negative_sentences:
        neg += j[0]
    neg = neg/len(negative_sentences)

    output = pos - neg

    print("This will be on a scale from 1 (very positive) to -1 (very negative)")
    return output


def flair_topn_sentiment(text, num_sentences=3):
    pos_sentences, neg_sentences = flair_sentence_by_sentence_sentiment_analysis(text)

    top_positive = pos_sentences[-num_sentences:]
    top_negative = neg_sentences[-num_sentences:]

    return top_positive, top_negative


def textblob_sentiment_analysis(text):
    """
    Measures the Polarity of text
    The polarity is a float within the range [-1.0, 1.0] where -1.0 is a very negative sentiment and 1.0 is very
    positive sentiment

    Seems to do better on neutral sentences

    :param text:
    :return:
    sentiment: float in range [-1.0, 1.0] where -1.0 is a very negative sentiment and 1.0 is very positive sentiment
    """
    return TextBlob(text).sentiment.polarity


def textblob_sentence_by_sentence_sentiment_analysis(text):

    sentences = sentence_tokenizer(text)

    output = []
    for sent in sentences:
        score = textblob_sentiment_analysis(sent)

        output.append((score, sent))

    output = sorted(output, key=lambda x: x[0])

    return output


def textblob_topn_sentiment(text, num_sentences=3):

    sentence_sentiment = textblob_sentence_by_sentence_sentiment_analysis(text)

    positive_sentences = sentence_sentiment[-num_sentences:]
    negative_sentences = sentence_sentiment[:num_sentences]

    return positive_sentences, negative_sentences


def nltk_sentiment_analysis(text):
    """

    :param text:
    :return: dict with keys 'neg'(negative), 'neu'(neutral), 'pos'(positive) and 'compound'
    Assume all are on a scale of 0-1
    compound is 0 negative to 1 positive
    """

    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)


def nltk_sentence_by_sentence_sentiment_analysis(text):

    sentences = sentence_tokenizer(text)

    output = []
    for sent in sentences:
        score = nltk_sentiment_analysis(sent)

        output.append((score, sent))

    return output


def nltk_topn_sentiment(text):







if __name__ == '__main__':

    # file = open("cnn.txt", "r")
    # cnn = file.read()
    # file.close()
    #
    file = open("fox.txt", "r")
    fox = file.read()
    file.close()


    top_p, top_n = flair_topn_sentiment(fox)
    print("\n\npositive:\n", top_p)
    print("\n\n\nnegative\n", top_n)

    # print('\n\nPositive example:')
    # sent = 'The night was filled with dozens of standing ovations and cheers from Republican supporters of Trump' #fox.split('/n')[0]
    # print(sent)
    # out = nltk_sentiment_analysis(sent)
    # print(out)
    #
    # print('\n\nNegative example:')
    # sent = "In one final gesture of division between Democrats and Republicans, Pelosi stood at the end of Trump's address and tore up the transcript of his speech"
    # print(sent)
    # out = nltk_sentiment_analysis(sent)
    # print(out)
    #
    # print('\n\nNeutral example:')
    # sent = "This is a neutral sentence and this is a statement of fact"
    # print(sent)
    # out = nltk_sentiment_analysis(sent)
    # print(out)



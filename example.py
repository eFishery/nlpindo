from nlpindo.worder import Worder
from nlpindo.sentencer import Sentencer

worder = Worder()
sentencer = Sentencer(worder)

worder.add_stopwords([ 'samsul' ])
worder.remove_stopwords([ 'saya', 'satu', 'dua', 'tiga' ])
worder.stemmer.add_basic_words([ 'melangkah' ])
worder.stemmer.remove_basic_words([ 'maju' ])

wc = worder.word_count('saya samsul beranak melangkah kemajuan tiga')
print(wc)

sentences = []
scored_sentences = sentencer.score_popular(sentences, False)
for score, sentence, words in scored_sentences:
    print(score)
    print(sentence)

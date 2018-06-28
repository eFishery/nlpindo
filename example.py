from nlpindo.worder import Worder

worder = Worder()

worder.add_stopwords([ 'samsul' ])
worder.remove_stopwords([ 'saya', 'satu', 'dua', 'tiga' ])
worder.stemmer.add_basic_words([ 'melangkah' ])
worder.stemmer.remove_basic_words([ 'maju' ])

wc = worder.word_count('saya samsul beranak melangkah kemajuan tiga')
print(wc)

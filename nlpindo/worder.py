from .stemmer import Stemmer
from .resource.stopwords import stopwords

class Worder:
    def tokenize(self, text):
        text = text.replace('.', ' ').replace(',', ' ')
        words = text.split()
        return words

    def word_count(self, text, remove_stopwords=True):
        word_count = {}
        words = self.tokenize(text)

        stemmer = Stemmer()

        for word in words:
            if remove_stopwords and word in stopwords:
                continue

            word = stemmer.stem(word)

            if remove_stopwords and word in stopwords:
                continue

            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1

        return word_count

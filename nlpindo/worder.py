import re

from .stemmer import Stemmer
from .resource.stopwords import stopwords


class Worder:
    def __init__(self):
        self.added_stopwords = []
        self.removed_stopwords = []
        self.stemmer = Stemmer()

    def add_stopwords(self, stopwords):
        if type(stopwords) == list:
            self.added_stopwords.extend(stopwords)
        else:
            self.added_stopwords.append(stopwords)

    def remove_stopwords(self, stopwords):
        if type(stopwords) == list:
            self.removed_stopwords.extend(stopwords)
        else:
            self.removed_stopwords.append(stopwords)

    def get_all_stopwords(self):
        all_stopwords = []
        for word in stopwords:
            if word not in self.removed_stopwords:
                all_stopwords.append(word)
        for word in self.added_stopwords:
            if word not in self.removed_stopwords:
                all_stopwords.append(word)
        return all_stopwords

    def is_stopword(self, word):
        if word not in self.removed_stopwords:
            if word in stopwords or word in self.added_stopwords:
                return True
        return False

    def tokenize(self, text, include_symbols=False):
        spaceds = text.split()
        re_separator = re.compile(r'([^a-zA-Z0-9])')

        separateds = []
        for spaced in spaceds:
            separated = re_separator.split(spaced)
            separateds.extend(separated)

        tokens = []
        for separated in separateds:
            separated = separated.strip()
            if separated:
                if include_symbols:
                    tokens.append(separated)
                else:
                    if re.match(r'[a-zA-Z]', separated):
                        tokens.append(separated)

        return tokens

    def stem(self, text, remove_stopwords=True):
        tokens = self.tokenize(text)
        words = []
        for word in tokens:
            word = word.lower()
            if remove_stopwords and self.is_stopword(word):
                continue
            word = self.stemmer.stem(word)
            if remove_stopwords and self.is_stopword(word):
                continue
            words.append(word)
        return words

    def word_count(self, text, remove_stopwords=True):
        word_count = {}
        words = self.tokenize(text)

        for word in words:
            word = word.lower()

            if remove_stopwords and self.is_stopword(word):
                continue

            word = self.stemmer.stem(word)

            if remove_stopwords and self.is_stopword(word):
                continue

            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1

        return word_count

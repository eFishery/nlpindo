import re

from .stemmer import Stemmer
from .resource.stopwords import stopwords


class Worder:
    def __init__(self):
        self.stopwords = stopwords
        self.stemmer = Stemmer()

    def add_stopwords(self, words):
        if type(words) is not set:
            words = set(words)
        self.stopwords = self.stopwords.union(words)

    def remove_stopwords(self, words):
        if type(words) is not set:
            words = set(words)
        self.stopwords = self.stopwords - words

    def is_stopword(self, word):
        return word in self.stopwords

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

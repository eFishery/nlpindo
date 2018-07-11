import math
import numpy as np

class Sentencer:
    def __init__(self, worder):
        self.worder = worder

    def score_popular(self, sentences, remove_stopwords=True):
        scores = [0 for sentence in sentences]
        words = [self.worder.stem(sentence, remove_stopwords) for sentence in sentences]

        for idx in range(len(words)):
            for idx_walk in range(len(words)):
                if idx_walk == idx:
                    continue

                acuan = words[idx]
                korban = words[idx_walk]

                score = 0
                for word in korban:
                    if word in acuan:
                        score += 1

                dividen = len(acuan) + len(korban)
                if dividen > 0:
                    scores[idx] += score / dividen

        result = []
        for idx in range(len(sentences)):
            result.append((scores[idx], sentences[idx], words[idx]))

        result = sorted(result, key=lambda item: item[0], reverse=True)
        return result

    def summarize(self, sentences, n_sentence):
        # stem words and calculate their occurence
        words_list = []
        word_scores = {}
        for sentence in sentences:
            words = self.worder.stem(sentence)
            for word in words:
                if word not in word_scores:
                    word_scores[word] = 0
                word_scores[word] += 1
            words_list.append(words)

        # L2 norm
        keys = []
        values = []
        for word, score in word_scores.items():
            keys.append(word)
            values.append(score)
        values = np.array(values, dtype=np.float)
        norms = np.linalg.norm(values)
        values[:] = values / norms
        for idx, key in enumerate(keys):
            word_scores[key] = values[idx]

        # score sentence
        scores = []
        for words in words_list:
            score = 0
            for word in words:
                score += word_scores[word]
            scores.append(score)

        # exclude identical sentences
        wordchains = set()
        result = []
        for idx in range(len(sentences)):
            wordchain = ' '.join(words_list[idx])
            if wordchain not in wordchains:
                wordchains.add(wordchain)
                result.append((idx, scores[idx], sentences[idx]))

        # rank and choose n_sentence
        result = sorted(result, key=lambda item: item[1], reverse=True)
        result = result[:n_sentence]
        result = sorted(result, key=lambda item: item[0])

        return result

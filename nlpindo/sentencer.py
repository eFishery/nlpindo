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

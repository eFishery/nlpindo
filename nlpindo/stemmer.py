import copy
from .resource.dictionary import dictionary

class Stemmer:
    def __init__(self):
        self.added_basic_words = []
        self.removed_basic_words = []

    def add_basic_words(self, words):
        if type(words) == list:
            self.added_basic_words.extend(words)
        else:
            self.added_basic_words.append(words)

    def remove_basic_words(self, words):
        if type(words) == list:
            self.removed_basic_words.extend(words)
        else:
            self.removed_basic_words.append(words)

    def is_basic_word(self, word):
        if word in self.removed_basic_words:
            return False
        return word in dictionary or word in self.added_basic_words

    def process_word(self, word):
        word = word.lower()
        queue = [(word, {
            'prefix': None,
            'suffix': None,
        })]

        if self.is_basic_word(word):
            return queue[-1]

        # particle
        len_queue = len(queue)
        for i in range(len_queue):
            new_word = self.check_particle(queue, queue[i])
            if new_word:
                return queue[-1]

        # print('particles')
        # for my_word, my_confix in queue:
        #     print(' ', my_word, my_confix)

        # possessive
        len_queue = len(queue)
        for i in range(len_queue):
            new_word = self.check_possessive(queue, queue[i])
            if new_word:
                return queue[-1]

        # print('possessive')
        # for my_word, my_confix in queue:
        #     print(' ', my_word, my_confix)

        # suffix-1
        len_queue = len(queue)
        for i in range(len_queue):
            new_word = self.check_suffix(queue, queue[i], True)
            if new_word:
                return queue[-1]

        # print('suffix-1')
        # for my_word, my_confix in queue:
        #     print(' ', my_word, my_confix)

        # suffix-2
        old_len_queue = len_queue
        len_queue = len(queue)
        for i in range(old_len_queue, len_queue):
            new_word = self.check_suffix(queue, queue[i], False)
            if new_word:
                return queue[-1]

        # print('suffix-2')
        # for my_word, my_confix in queue:
        #     print(' ', my_word, my_confix)

        # prefix-1
        len_queue = len(queue)
        for i in range(len_queue):
            new_word = self.check_prefix(queue, queue[i], True)
            if new_word:
                return queue[-1]

        # print('prefix-1')
        # for my_word, my_confix in queue:
        #     print(' ', my_word, my_confix)

        # prefix-2
        old_len_queue = len_queue
        len_queue = len(queue)
        for i in range(old_len_queue, len_queue):
            new_word = self.check_prefix(queue, queue[i], False)
            if new_word:
                return queue[-1]

        # print('prefix-2')
        # for my_word, my_confix in queue:
        #     print(' ', my_word, my_confix)

        # print('oov', queue[-1])
        return queue[0]

    def append_queue(self, queue, new_word, old_confix, is_true, spec={}):
        new_confix = copy.deepcopy(old_confix)
        if is_true:
            for key in spec:
                new_confix[key] = spec[key]
        queue.append((new_word, new_confix))
        if self.is_basic_word(new_word):
            return new_word

    def check_particle(self, queue, old):
        old_word, old_confix = old

        for morpheme in ['lah', 'kah', 'tah', 'pun']:
            if old_word.endswith(morpheme):
                new_word = old_word[:-len(morpheme)]
                if self.append_queue(queue, new_word, old_confix, False):
                    return new_word

    def check_possessive(self, queue, old):
        old_word, old_confix = old

        for morpheme in ['ku', 'mu', 'nya']:
            if old_word.endswith(morpheme):
                new_word = old_word[:-len(morpheme)]
                if self.append_queue(queue, new_word, old_confix, False):
                    return new_word

        morpheme = 'ku'
        if old_word.startswith(morpheme):
            new_word = old_word[len(morpheme):]
            if self.append_queue(queue, new_word, old_confix, False):
                return new_word

    def check_suffix(self, queue, old, is_first_suffix):
        old_word, old_confix = old

        for morpheme in ['kan', 'an', 'isasi', 'i', 'isme']:
            spec = {'suffix': morpheme}
            if old_word.endswith(morpheme):
                new_word = old_word[:-len(morpheme)]
                if self.append_queue(queue, new_word, old_confix, is_first_suffix, spec):
                    return new_word

    def check_prefix(self, queue, old, is_first_prefix):
        new_word = self.check_prefix_me(queue, old, is_first_prefix)
        if new_word:
            return new_word
        new_word = self.check_prefix_di(queue, old, is_first_prefix)
        if new_word:
            return new_word
        new_word = self.check_prefix_be(queue, old, is_first_prefix)
        if new_word:
            return new_word
        new_word = self.check_prefix_pe(queue, old, is_first_prefix)
        if new_word:
            return new_word
        new_word = self.check_prefix_ke(queue, old, is_first_prefix)
        if new_word:
            return new_word
        new_word = self.check_prefix_te(queue, old, is_first_prefix)
        if new_word:
            return new_word
        new_word = self.check_prefix_se(queue, old, is_first_prefix)
        if new_word:
            return new_word

    def check_prefix_me(self, queue, old, is_first_prefix):
        morpheme = 'me'
        old_word, old_confix = old
        prefix = morpheme if old_confix['prefix'] is None else old_confix['prefix']
        spec = {'prefix': morpheme}

        if prefix != morpheme or ('an' != old_confix['suffix']):
            if old_word.startswith('meny'):
                new_word_s = 's' + old_word[4:]
                if self.append_queue(queue, new_word_s, old_confix, is_first_prefix, spec):
                    return new_word_s

                new_word_se = new_word_s[2:]
                if self.append_queue(queue, new_word_se, old_confix, is_first_prefix, spec):
                    return new_word_se

                new_word_ny = old_word[2:]
                if self.append_queue(queue, new_word_ny, old_confix, is_first_prefix, spec):
                    return new_word_ny

            elif old_word.startswith('meng'):
                new_word_k = 'k' + old_word[4:]
                if self.append_queue(queue, new_word_k, old_confix, is_first_prefix, spec):
                    return new_word_k

                new_word_ng = old_word[2:]
                if self.append_queue(queue, new_word_ng, old_confix, is_first_prefix, spec):
                    return new_word_ng

                new_word = old_word[4:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            elif old_word.startswith('mem'):
                new_word_p = 'p' + old_word[3:]
                if self.append_queue(queue, new_word_p, old_confix, is_first_prefix, spec):
                    return new_word_p

                new_word_m = old_word[2:]
                if self.append_queue(queue, new_word_m, old_confix, is_first_prefix, spec):
                    return new_word_m

                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            elif old_word.startswith('men'):
                new_word_t = 't' + old_word[3:]
                if self.append_queue(queue, new_word_t, old_confix, is_first_prefix, spec):
                    return new_word_t

                new_word_n = old_word[2:]
                if self.append_queue(queue, new_word_n, old_confix, is_first_prefix, spec):
                    return new_word_n

                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            if old_word.startswith(morpheme):
                new_word = old_word[len(morpheme):]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

    def check_prefix_di(self, queue, old, is_first_prefix):
        morpheme = 'di'
        old_word, old_confix = old
        prefix = morpheme if old_confix['prefix'] is None else old_confix['prefix']
        spec = {'prefix': morpheme}

        if prefix != morpheme or ('an' != old_confix['suffix']):
            if old_word.startswith(morpheme):
                new_word = old_word[len(morpheme):]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

    def check_prefix_be(self, queue, old, is_first_prefix):
        morpheme = 'be'
        old_word, old_confix = old
        prefix = morpheme if old_confix['prefix'] is None else old_confix['prefix']
        spec = {'prefix': morpheme}

        if prefix != morpheme or ('i' != old_confix['suffix']):
            if old_word.startswith('ber'):
                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            elif old_word.startswith('bel'):
                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            if old_word.startswith(morpheme):
                new_word = old_word[len(morpheme):]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

    def check_prefix_pe(self, queue, old, is_first_prefix):
        morpheme = 'pe'
        old_word, old_confix = old
        prefix = morpheme if old_confix['prefix'] is None else old_confix['prefix']
        spec = {'prefix': morpheme}

        if prefix != morpheme or ('i' != old_confix['suffix'] and 'kan' != old_confix['suffix']):
            if old_word.startswith('per'):
                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            elif old_word.startswith('pel'):
                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            elif old_word.startswith('peny'):
                new_word_s = 's' + old_word[4:]
                if self.append_queue(queue, new_word_s, old_confix, is_first_prefix, spec):
                    return new_word_s

                new_word_se = new_word_s[2:]
                if self.append_queue(queue, new_word_se, old_confix, is_first_prefix, spec):
                    return new_word_se

                new_word_ny = old_word[2:]
                if self.append_queue(queue, new_word_ny, old_confix, is_first_prefix, spec):
                    return new_word_ny

            elif old_word.startswith('peng'):
                new_word_k = 'k' + old_word[4:]
                if self.append_queue(queue, new_word_k, old_confix, is_first_prefix, spec):
                    return new_word_k

                new_word_ng = old_word[2:]
                if self.append_queue(queue, new_word_ng, old_confix, is_first_prefix, spec):
                    return new_word_ng

                new_word = old_word[4:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            elif old_word.startswith('pem'):
                new_word_p = 'p' + old_word[3:]
                if self.append_queue(queue, new_word_p, old_confix, is_first_prefix, spec):
                    return new_word_p

                new_word_m = old_word[2:]
                if self.append_queue(queue, new_word_m, old_confix, is_first_prefix, spec):
                    return new_word_m

                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            elif old_word.startswith('pen'):
                new_word_t = 't' + old_word[3:]
                if self.append_queue(queue, new_word_t, old_confix, is_first_prefix, spec):
                    return new_word_t

                new_word_n = old_word[2:]
                if self.append_queue(queue, new_word_n, old_confix, is_first_prefix, spec):
                    return new_word_n

                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            if old_word.startswith(morpheme):
                new_word = old_word[len(morpheme):]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

    def check_prefix_ke(self, queue, old, is_first_prefix):
        morpheme = 'ke'
        old_word, old_confix = old
        prefix = morpheme if old_confix['prefix'] is None else old_confix['prefix']
        spec = {'prefix': morpheme}

        if prefix != morpheme or ('i' != old_confix['suffix'] and 'kan' != old_confix['suffix']):
            if old_word.startswith(morpheme):
                new_word = old_word[len(morpheme):]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

    def check_prefix_te(self, queue, old, is_first_prefix):
        morpheme = 'te'
        old_word, old_confix = old
        prefix = morpheme if old_confix['prefix'] is None else old_confix['prefix']
        spec = {'prefix': morpheme}

        if prefix != morpheme or ('an' != old_confix['suffix']):
            if old_word.startswith('ter'):
                new_word = old_word[3:]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

            if old_word.startswith(morpheme):
                new_word = old_word[len(morpheme):]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

    def check_prefix_se(self, queue, old, is_first_prefix):
        morpheme = 'se'
        old_word, old_confix = old
        prefix = morpheme if old_confix['prefix'] is None else old_confix['prefix']
        spec = {'prefix': morpheme}

        if prefix != morpheme or ('i' != old_confix['suffix'] and 'kan' != old_confix['suffix']):
            if old_word.startswith(morpheme):
                new_word = old_word[len(morpheme):]
                if self.append_queue(queue, new_word, old_confix, is_first_prefix, spec):
                    return new_word

    def stem_word(self, word):
        if word.find('-') == -1:
            new_word, new_confix = self.process_word(word)
            return new_word

        words = word.split('-')
        word0, word1 = words[0], words[1]

        if word0 == word1:
            new_word, new_confix = self.process_word(word0)
            return new_word

        if word0.find(word1) > -1:
            new_word, new_confix = self.process_word(word0)
            return new_word

        if word1.find(word0) > -1:
            new_word, new_confix = self.process_word(word1)
            return new_word

        word_left, confix_left = self.process_word(word0)
        word_right, confix_right = self.process_word(word1)

        if word_left == word_right:
            return word_left

        return word_left + '-' + word_right

    def stem(self, text):
        words = text.split()
        if len(words) == 1:
            return self.stem_word(text)
        elif len(words) > 1:
            return ' '.join([self.stem_word(word) for word in words])
        return text

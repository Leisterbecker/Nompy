import collections


class Analyzer:
    def __init__(self, depth):
        self.depth = depth
        self.m_init = {}
        self.m_tail = {}
        self.m_mid = None

    def get_ranges(self, wlen):
        return [(x, x + self.depth + 1) for x in range(wlen - self.depth)]

    def decompose(self, word):
        return [word[r[0]:r[1]] for r in self.get_ranges(len(word))]

    def get_parts(self, word):
        return [frame for frame in self.decompose(word.lower().strip())]

    def process_word(self, word):
        parts = self.get_parts(word)
        plen = len(parts)
        if len(parts) == 0:
            word = word.rstrip()
            self.m_init[word] = self.m_init[word] + 1 if self.m_init.__contains__(word) else 1
            self.m_tail[word] = self.m_tail[word] + 1 if self.m_tail.__contains__(word) else 1
            return word

        else:
            self.m_init[parts[0]] = self.m_init[parts[0]] + 1 if self.m_init.__contains__(parts[0]) else 1
            self.m_tail[parts[plen - 1]] = self.m_tail[parts[plen - 1]] + 1 if self.m_tail.__contains__(
                parts[plen - 1]) else 1
            return parts

    def build_model(self, paths, box):
        words_box = []
        words_path = []
        words_sum = []
        if box != "":
            words_split = box.replace('\n', '').split(" ")
            for word in words_split:
                words_box += self.process_word(word)
            print(words_box)
        for path in paths:
            if path != "":
                with open(path) as fp:
                    words = [word for word in fp]
                    for word in words:
                        words_sum += self.process_word(word)
                words_path += words_sum
                words_sum.clear()
                print("sum len: " + str(len(words_path)))
        self.m_mid = collections.Counter(words_box + words_path)

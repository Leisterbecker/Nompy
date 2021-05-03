import random

class Generator:
    def __init__(self, depth, minlen, maxlen, m_init, m_mid, m_tail):
        self.depth = depth
        self.minlen = minlen
        self.maxlen = maxlen
        self.m_init = m_init
        self.m_tail = m_tail
        self.m_mid = m_mid

    def generate_name(self):
        length = random.randint(self.minlen, self.maxlen)
        print("len=" + str(length))
        res = ""
        i = 0
        while i < length:
            if i == 0:
                s = str(random.choice(list(self.m_init.keys()))).capitalize()
                i += 1
            else:
                if i < length - 2:
                    s = self.find_next_letter(res[i:])
                    if s == '' and i < (2 * (length / 3)):
                        s = str(random.choice(list(self.m_mid.keys())))
                        i += len(s)
                    else:
                        i += 1
                    print("next letter is: " + s)
                else:
                    s = self.find_next_letter(res[i:])
                    if s == '' and i < (2 * (length / 3)):
                        s = str(random.choice(list(self.m_tail.keys())))
                        i += len(s)
                    else:
                        i += 1
                    print("next (end) letter is: " + s)
            res = res + s
        print("res is: " + res)
        print("\n\n")
        return res

    def find_next_letter(self, last):
        print("finding next letter for last: " + last)
        tmp = self.get_subtable(last)
        print("subtable of last: " + str(tmp))
        ran = random.random() * sum(tmp.values())
        letter = ''
        for item in tmp:
            ran -= tmp[item]
            if ran < 0:
                letter = item[-1]
        print("letter is: " + letter)
        return letter

    def get_subtable(self, last):
        tmp = {}
        for item in self.m_mid.keys():
            if item[:-1] == last:
                tmp[item] = self.m_mid[item]
        return tmp
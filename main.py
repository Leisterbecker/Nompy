import random
import os


def process_word(initial, table, depth, word):
    word = word.lower().strip()
    if len(word)>depth and depth>0:
        for i in range(depth, len(word)):
            str = ""
            for j in range(0,depth+1):
                str = word[i-j] + str
            if i == depth:
                if str in initial.keys():
                    initial[str] = initial.get(str) + 1
                else:
                    initial[str] = 1
            else:
                if str in table.keys():
                    table[str] = table.get(str) + 1
                else:
                    table[str] = 1


def process_file(initial, table, depth, path):
    filepath = path
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            words = line.split(" ")
            for word in words:
                process_word(initial, table, depth, word)
            line = fp.readline()
            cnt += 1


def get_subtable(table, last):
    tmp = {}
    for item in table.keys():
        if item[:-1] == last:
            tmp[item] = table[item]
    return tmp


def find_next_letter(table, last):
    tmp = get_subtable(table, last)
    ran = random.random() * sum(tmp.values())
    letter = ''
    for item in tmp:
        ran -= tmp[item]
        if ran < 0:
            letter = item[-1]
    return letter


def generate_name(initial, table, depth, minlen, maxlen):
    len = random.randint(minlen, maxlen)
    res = ""
    for i in range(0, len):
        if i == 0:
            s = str(random.choice(list(initial)))
            s = s.capitalize()
        else:
            s = find_next_letter(table, res[i:])
        res = res + s
    return res




def main():
    generate_files = False

    names = []
    max = 1000
    depth = 4
    init_table = {}
    markov_table = {}

    files = os.listdir('input')
    if generate_files:
        for file in files:
            process_file(init_table, markov_table, depth, 'input/'+file)
            for i in range(0, max):
                names.append(generate_name(init_table, markov_table, depth, 5, 9))
            with open('output/out_'+str(depth)+'_' + file, "w") as outfile:
                outfile.write("\n".join(names))

            names.clear()
            init_table.clear()
            markov_table.clear()
    else:
        while True:
            process_file(init_table, markov_table, depth, 'input/german_names.txt')
            name = generate_name(init_table, markov_table, 2, 13, 13)
            if name == 'Leisterbecker':
                break
        print('Success! -> ' + name)

main()

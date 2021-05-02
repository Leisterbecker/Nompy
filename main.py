import PySimpleGUI as sg
import random
import os
import collections

# General globals

depth = 3
names = []
max = 1000
minlen = 4
maxlen = 11

word_initials = {}
word_endings = {}



# Part A: Analysis


# take word length and global depth, return list with frame indices inside word
def get_ranges(wlen):
    return [ (x,x+depth+1) for x in range(wlen-depth) ]


# take word, return list with frames inside word
def decompose(word):
    return [ word[r[0]:r[1]] for r in get_ranges(len(word)) ]


# take word, decompose and list with [ (frame, 1) ]
def process_word(word):
    return [ frame for frame in decompose(word.lower().strip()) ]


def build_model(paths, box):
    words_box = []
    words_path = []
    words_sum = []
    if box != "":
        words_box = sum(map(process_word, [word for word in box.replace('\n','').split(" ")]), [])
        print(words_box)
    for path in paths:
        if path != "":
            with open(path) as fp:
                words = [word for word in fp]
                for word in words:
                    parts = process_word(word)
                    plen = len(parts)
                    word_initials[parts[0]] = word_initials[parts[0]] + 1 if word_initials.__contains__(parts[0]) else 1
                    word_endings[parts[plen-1]] = word_endings[parts[plen-1]] + 1 if word_endings.__contains__(parts[plen-1]) else 1
                    words_sum += parts
            words_path += words_sum
            print("sum len: " + str(len(words_path)))
    return collections.Counter(words_box + words_path)


# Part B: Generation


def generate_name(markov, minlen, maxlen):
    len = random.randint(minlen, maxlen)
    res = ""
    for i in range(0, len):
        if i == 0:
            s = str(random.choice(list(word_initials.keys()))).capitalize()
        else:
            if i < len -2:
                s = find_next_letter(markov, res[i:])
            else:
                s = find_next_letter(word_endings, res[i:])
        res = res + s
    return res


def find_next_letter(markov, last):
    tmp = get_subtable(markov, last)
    ran = random.random() * sum(tmp.values())
    letter = ''
    for item in tmp:
        ran -= tmp[item]
        if ran < 0:
            letter = item[-1]
    return letter


def get_subtable(markov, last):
    tmp = {}
    for item in markov.keys():
        if item[:-1] == last:
            tmp[item] = markov[item]
    return tmp




# GUI functions

def clear_input_files():
    chosenFiles.clear()
    for i in range(1, maxfiles + 1):
        index = 'k' + str(i)
        window[index].update('')


# Layout

control_inner = [
    [ sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse()],
    [ sg.Text('Depth:') ],
    [ sg.Text('Min-Length:')],
    [ sg.Text('Max-Length:'),],
    [ sg.Text('Amount:')],
    [ sg.HSeparator()],
    [sg.Text('File 1:')],
    [sg.Text('File 2:')],
    [sg.Text('File 3:')],
    [sg.Text('File 4:')],
    [sg.Text('File 5:')],
    [sg.Text('Input-Text:')]
]



control_column = [
    [ sg.Button('Build Model'), sg.Button('Reset Input'), sg.Button('Generate')],
    [ sg.Input(key='depth') ],
    [ sg.Input(key='min') ],
    [ sg.Input(key='max')],
    [ sg.Input(key='amount')],
    [ sg.HSeparator()],
    [sg.Input(key='k1')],
    [sg.Input(key='k2')],
    [sg.Input(key='k3')],
    [sg.Input(key='k4')],
    [sg.Input(key='k5')],
    [sg.Multiline(size=(30, 5), key='inputbox', autoscroll=True)],

]


errorCol = [
    [sg.Column([[sg.Text('Error:')]]), sg.Column([[sg.Input(key='error')]])]
]


control = [
    [ sg.Column(control_inner,  vertical_alignment='Top'), sg.Column(control_column,  vertical_alignment='Top') ],
    [ sg.HSeparator()],
    [ sg.Column(errorCol)]
]

view_column = [
    [ sg.Multiline(size=(30, 40), key='outputbox', auto_size_text=True,autoscroll=True)]
]


layout = [
    [
        sg.Column(control, vertical_alignment='Top'),
        sg.VSeparator(),
        sg.Column(view_column)
    ]
]

# Gui globals
window = sg.Window("Nompy - Markov Name Generation Tool", layout, resizable=True, finalize=True)
maxfiles = 5
chosenFiles = []

markov = 0

window['depth'].update('3')
window['min'].update('3')
window['max'].update('10')
window['amount'].update('100')


# Event Loop

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    elif event == "Build Model":
        if len(chosenFiles) == 0 and len(str(values['inputbox'])) == 1:
            window['error'].update('Error: Please choose file[s] or append words in the input field!')
        else:
            if values['depth']=='':
                window['error'].update('Error: Please provide depth!')
            else:
                depth = int(values['depth'])
                markov = build_model(chosenFiles, values['inputbox'])
                clear_input_files()
    elif event == "Generate":
        names = ""
        if values['depth']=='':
            window['error'].update('Error: Please provide depth!')
        else:
            depth = int(values['depth'])
            if values['min'] == '' or values ['max'] == '':
                window['error'].update('Error: Please provide valid min or max length!')
            else:
                minlen = int(values['min'])
                maxlen = int(values['max'])
                if values['amount'] == '':
                    window['error'].update('Error: Please provide valid amount of generations (<1000)!')
                else:
                    max = int(values['amount'])
                    for i in range(0,max):
                        name = generate_name(markov, minlen, maxlen) + '\n'
                        names += name
                    window['outputbox'].update(names)

    elif event == "-FILE-":
        print(values['-FILE-'])
        lst = str(values['-FILE-']).split('/')
        l = len(lst)
        chosen = lst[l-1]
        for i in range(1,maxfiles+1):
            index = 'k' + str(i)
            if values[index]=='' and (not chosenFiles.__contains__(values['-FILE-'])):
                window[index].update(chosen)
                chosenFiles.append(values['-FILE-'])
                break
    elif event == 'Reset Input':
        clear_input_files()

window.close()




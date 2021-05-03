import PySimpleGUI as sg


mode = [
    [sg.Text('Modus:'),
     sg.Radio('Single', "rg", True, key='r1'),
     sg.Radio('Double', "rg", False),
     sg.Combo(['Default'], key='c1'),
     sg.Combo(['Default'], key='c2') ]
]

top_buttons = [
    [sg.Input(key='-FILE-', visible=False, enable_events=True),
     sg.FileBrowse(),
     sg.Button('Build Model'),
     sg.Button('Reset Input'),
     sg.Button('Generate'),
     sg.Input(key='amount')]
]


#TABS for Markov Models
tab0 = [
    [sg.Column([[
        sg.Text('Depth:')],
       [sg.Text('Min-Length:')],
       [sg.Text('Max-Length:')]]),
     sg.Column([[
         sg.Input(key='d0')],
        [sg.Input(key='mi0')],
        [sg.Input(key='ma0')]])]
]

tab1 = [
    [sg.Column([[
        sg.Text('Depth:')],
       [sg.Text('Min-Length:')],
       [sg.Text('Max-Length:')]]),
     sg.Column([[
         sg.Input(key='d1')],
        [sg.Input(key='mi1')],
        [sg.Input(key='ma1')]])]
]

tab2 = [
    [sg.Column([[
        sg.Text('Depth:')],
       [sg.Text('Min-Length:')],
       [sg.Text('Max-Length:')]]),
     sg.Column([[
         sg.Input(key='d2')],
        [sg.Input(key='mi2')],
        [sg.Input(key='ma2')]])]
]

tab3 = [
    [sg.Column([[
        sg.Text('Depth:')],
       [sg.Text('Min-Length:')],
       [sg.Text('Max-Length:')]]),
     sg.Column([[
         sg.Input(key='d3')],
        [sg.Input(key='mi3')],
        [sg.Input(key='ma3')]])]
]

tab4 = [
    [sg.Column([[
        sg.Text('Depth:')],
       [sg.Text('Min-Length:')],
       [sg.Text('Max-Length:')]]),
     sg.Column([[
         sg.Input(key='d4')],
        [sg.Input(key='mi4')],
        [sg.Input(key='ma4')]])]
]

tab5 = [
    [sg.Column([[
        sg.Text('Depth:')],
       [sg.Text('Min-Length:')],
       [sg.Text('Max-Length:')]]),
     sg.Column([[
         sg.Input(key='d5')],
        [sg.Input(key='mi5')],
        [sg.Input(key='ma5')]])]
]

tab_container = [
    [sg.TabGroup([[sg.Tab('Input Tab', tab0, key='tab0')],
                  [sg.Tab('Tab 1', tab1, key='tab1', visible=False)],
                  [sg.Tab('Tab 2', tab2, key='tab2', visible=False)],
                  [sg.Tab('Tab 3', tab3, key='tab3', visible=False)],
                  [sg.Tab('Tab 4', tab4, key='tab4', visible=False)],
                  [sg.Tab('Tab 5', tab5, key='tab5', visible=False)]], key='tabs')]
]


# Layouts for text input

in_left = [
    [sg.Text('Model name:')],
    [sg.Text('File 1:')],
    [sg.Text('File 2:')],
    [sg.Text('File 3:')],
    [sg.Text('File 4:')],
    [sg.Text('File 5:')],
    [sg.Text('Input-Text:')]

]

in_right = [
    [sg.Input(key='name')],
    [sg.Input(key='k1')],
    [sg.Input(key='k2')],
    [sg.Input(key='k3')],
    [sg.Input(key='k4')],
    [sg.Input(key='k5')],
    [sg.Multiline(size=(30, 5), key='inputbox', autoscroll=True)]
]

input = [
    [sg.Column(in_left, vertical_alignment='Top'),
     sg.Column(in_right)]
]

error = [
    [   sg.Column([[sg.Text('Error:')]]),    sg.Column([[sg.Input(key='error')]])]
]

controls = [
    [sg.Column(mode, vertical_alignment='Top')],
    [sg.Column(top_buttons, vertical_alignment='Top')],
    [sg.HSeparator()],
    [sg.Column(tab_container)],
    [sg.HSeparator()],
    [sg.Column(input)],
    [sg.HSeparator()],
    [sg.Column(error)]
]

names_list = [
    [sg.Multiline(size=(40, 40), key='outputbox', auto_size_text=True, autoscroll=True)]
]

layout = [
    [sg.Column(controls, vertical_alignment='Top'),
     sg.VSeparator(),
     sg.Column(names_list, vertical_alignment='Top')]
]

def get_layout():
    return layout
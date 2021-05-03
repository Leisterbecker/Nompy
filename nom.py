import PySimpleGUI as sg
import sg_layout

from generator import Generator
from analyzer import Analyzer

# TODO: delete active models, save and load models, inputbox to file (for model creation, not saving), error messages


class Nompy:
    def __init__(self):
        self.analyzer = None
        self.generators = []
        self.active_generators = 0
        self.names_generators = []
        self.chosen_files = []
        self.max_files = 5
        self.layout = sg_layout.get_layout()
        self.window = sg.Window("Nompy - Markov Name Generation Tool", self.layout, resizable=True, finalize=True)
        self.window['d0'].update(3)
        self.window['mi0'].update(3)
        self.window['ma0'].update('10')
        self.window['amount'].update('100')

        #Event Loop
        while True:
            event, values = self.window.read()
            if event == "OK" or event == sg.WIN_CLOSED:
                break
            elif event == "Build Model":
                print("len chosen files: " + str(len(self.chosen_files)) + ", len str inputbox: " + str(len(str(values['inputbox']))))
                if len(self.chosen_files) == 0 and len(str(values['inputbox'])) == 1:
                    self.window['error'].update('Error: Please choose file[s] or append words in the input field!')
                else:
                    if values['d0']=='':
                        self.window['error'].update('Error: Please provide depth!')
                    else:
                        self.depth = int(values['d0'])
                        self.analyzer = Analyzer(self.depth)
                        self.analyzer.build_model(self.chosen_files, values['inputbox'])

                        #add generator to generator list
                        if self.active_generators <= 5:
                            self.generators.append(Generator(int(values['d0']),
                                                             int(values['mi0']),
                                                             int(values['ma0']),
                                                             self.analyzer.m_init,
                                                             self.analyzer.m_mid,
                                                             self.analyzer.m_tail))
                            self.active_generators += 1

                            index = 'tab' + str(self.active_generators)
                            name = 'undefined' + str(self.active_generators) if str(values['name'])=='' else str(values['name'])
                            self.names_generators.append(name)
                            self.window[index].update(visible = True)
                            self.window.Element('tabs').Widget.tab(self.active_generators, text=name)
                            self.window['d' + str(self.active_generators)].update(values['d0'])
                            self.window['mi' + str(self.active_generators)].update(values['mi0'])
                            self.window['ma' + str(self.active_generators)].update(values['ma0'])

                            self.window['c1'].update(values=self.names_generators)
                            self.window['c2'].update(values=self.names_generators)

                            self.clear_input_files()
            elif event == "Generate":


                # EXCEPTION when no combo item selected


                names = ""
                if values['r1']:
                    gen1 = self.names_generators.index(values['c1'])
                    if values['d' + str(gen1)] == '':
                        self.window['error'].update('Error: Please provide depth!')
                    else:
                        self.generators[gen1].depth = int(values['d' + str(gen1) ])
                        if values['mi' + str(gen1)] == '' or values['ma' + str(gen1)] == '':
                            self.window['error'].update('Error: Please provide valid min or max length!')
                        else:
                            self.generators[gen1].minlen = int(values['mi' + str(gen1)])
                            self.generators[gen1].maxlen = int(values['ma' + str(gen1)])
                            if values['amount'] == '':
                                self.window['error'].update(
                                    'Error: Please provide valid amount of generations (<1000)!')
                            else:
                                if self.analyzer.m_mid == 0:
                                    self.window['error'].update('Error: Please build a model!')
                                else:
                                    for i in range(0, int(values['amount'])):
                                        name = self.generators[gen1].generate_name() + ',\n'
                                        names += name
                                    self.window['outputbox'].update(names)
                else:
                    gen1 = self.names_generators.index(values['c1'])
                    gen2 = self.names_generators.index(values['c2'])
                    if values['d' + str(gen1)]=='' or values['d' + str(gen2)]=='':
                        self.window['error'].update('Error: Please provide depth!')
                    else:
                        self.generators[gen1].depth = int(values['d' + str(gen1) ])
                        self.generators[gen2].depth = int(values['d' + str(gen2) ])
                        if values['mi' + str(gen1)] == '' or values['mi' + str(gen2)] == '' or \
                           values['ma' + str(gen1)] == '' or values['ma' + str(gen2)] == '':
                            self.window['error'].update('Error: Please provide valid min or max length!')
                        else:
                            self.generators[gen1].minlen = int(values['mi' + str(gen1)])
                            self.generators[gen1].maxlen = int(values['ma' + str(gen1)])
                            self.generators[gen2].minlen = int(values['mi' + str(gen2)])
                            self.generators[gen2].maxlen = int(values['ma' + str(gen2)])
                            if values['amount'] == '':
                                self.window['error'].update('Error: Please provide valid amount of generations (<1000)!')
                            else:
                                max = int(values['amount'])
                                if self.analyzer.m_mid == 0:
                                    self.window['error'].update('Error: Please build a model!')
                                else:
                                    for i in range(0,max):
                                            name = self.generators[gen1].generate_name() + "  " + \
                                                   self.generators[gen2].generate_name() + ',\n'
                                            names += name
                                    self.window['outputbox'].update(names)
            elif event == "-FILE-":
                print(values['-FILE-'])
                lst = str(values['-FILE-']).split('/')
                l = len(lst)
                chosen = lst[l-1]
                for i in range(1,self.max_files+1):
                    index = 'k' + str(i)
                    if values[index]=='' and (not self.chosen_files.__contains__(values['-FILE-'])):
                        self.window[index].update(chosen)
                        self.chosen_files.append(values['-FILE-'])
                        break
            elif event == 'Reset Input':
                self.clear_input_files()
        self.window.close()

    def clear_input_files(self):
        self.chosen_files.clear()
        for i in range(1, self.max_files + 1):
            index = 'k' + str(i)
            self.window[index].update('')




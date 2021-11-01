# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 10:48:11 2018
@author: kaiser_lu
"""
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import csv

with open('elembase.csv', 'r', encoding='utf-8') as out_file:
    filereader = csv.reader(out_file, delimiter=';')
    elembase = [row for row in filereader]


class ChemicalElement:
    """
    Базовый класс. Является родительским классом для подгрупп - металлов, неметаллов, а далее:
    галогенов и т.д
    """

    def __init__(self, atomic_number, symbol, element, element_native_lang,
                 group, period, atomic_weight, density, melt, boil,
                 heat_capacity, el_negativity, oxid_stat):
        self.atomic_number = int(atomic_number)
        self.symbol = symbol
        self.element = element
        self.element_native_lang = element_native_lang

        def tst_int(parameter):
            try:
                return int(parameter)
            except ValueError:
                return parameter

        self.group = tst_int(group)
        self.period = int(period)

        def tst_float(parameter):
            try:
                return float(parameter)
            except ValueError:
                return parameter

        self.atomic_weight = tst_float(atomic_weight)
        self.density = float(density.replace(',', '.'))

        def init_k_in_c(parameter):
            try:
                if str(parameter).find('[') > -1 and str(parameter).find('[') > -1:
                    parameter = str(parameter).replace('[', '').replace(']', '')
                    parameter = '[%s]' % (float(parameter) - 273)
                else:
                    parameter = '[%s]' % (float(parameter) - 273)
                return parameter
            except Exception:
                return parameter

        self.melt = init_k_in_c(melt)
        self.boil = init_k_in_c(boil)
        self.heat_capacity = tst_float(heat_capacity)
        self.el_negativity = tst_float(el_negativity)
        self.oxid_stat = [str(i) for i in str(oxid_stat).split(' ')]
        self.oxid_stat = self.init_oxid_stat
        self.valence = self.init_val

    def __str__(self):
        def list_stat_convert(_list):
            _list = str(_list)
            _list = _list.replace('[', '').replace(']', '').replace("'", "")
            return _list

        dictionary = dict(zip(['AlkaliMetal', 'AlkalineEarthMetal', 'TransitionMetal', 'PostTransitionMetal',
                               'Metalloid', 'Actinide', 'Lanthanide', 'OtherNonmetal', 'Halogen',
                               'NobleGas', 'ChemicalElement'],
                              ['Щелочной металл', 'Щелочноземельный металл', 'Переходный металл',
                               'Постпереходный металл',
                               'Металлоид', 'Актиноид', 'Лантаноид', 'Другой неметалл', 'Галоген',
                               'Инертный (благородный) газ', 'Об этом элементе мало информации']))

        return '[{}]\n[{}: {}]\n[{}]\n{}: {}, {}: {}\n{} {}, {} {}\n{}: {} {}\n' \
               '{}: {} {}\n{}: {} {}\n{}: {} {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}'.format(
            str(self.element_native_lang), 'Английское название элемента', self.element,
            dictionary[str(self.__class__).replace("<class '__main__.", "").replace("'>", '')],
            'Химический знак', str(self.symbol), 'атомный номер', str(self.atomic_number),
            'Группа', str(self.group), 'период', str(self.period),
            'Атомная масса', str(self.atomic_weight),
            'а.е.м.', 'Температура плавления', str(self.melt), 'ºC', 'Температура кипения', str(self.boil),
            'ºC', 'Теплоёмкость элемента', str(self.heat_capacity), 'Дж/К',
            'Электроотрицательность', str(self.el_negativity), 'Все возможные степени окисления',
            list_stat_convert(self.oxid_stat[1]), 'Наиболее встречающиеся', list_stat_convert(self.oxid_stat[0]),
            'Возможные валентности', list_stat_convert(self.valence))

    @property
    def init_oxid_stat(self):
        if self.oxid_stat == ['0.0']:
            return [['–'], 0]
        big_set, small_set = self.oxid_stat, list()
        for i in big_set:
            if str(i).find('[') > -1 and str(i).find(']') > -1:
                small_set.append(i)
        for i in range(len(small_set)):
            small_set[i] = str(small_set[i]).replace('[', '').replace(']', '')
        for j in range(len(big_set)):
            if str(big_set[j]).find('[') > -1 and str(big_set[j]).find(']') > -1:
                big_set[j] = str(big_set[j]).replace('[', '').replace(']', '')

        return [sorted(small_set, key=int), sorted(big_set, key=int)]

    @property
    def init_val(self):
        small_set = self.oxid_stat[0].copy()
        if small_set == ['–']:
            return '–'
        for i in small_set:
            if '-' in i:
                if i in small_set and i.replace('-', '') in small_set:
                    small_set.remove(i)
            else:
                if i in small_set and '-{}'.format(i) in small_set:
                    small_set.remove(i)
        dictionary = dict(zip([1, 2, 3, 4, 5, 6, 7, 8], ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']))
        dictionary1 = dict(zip(['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'], [1, 2, 3, 4, 5, 6, 7, 8]))
        for val in range(len(small_set)):
            small_set[val] = abs(int(small_set[val]))
            small_set[val] = dictionary[small_set[val]]
        small_set.sort(key=lambda x: int(dictionary1[x]))
        return small_set


class Metal(ChemicalElement):
    pass


class Nonmetal(ChemicalElement):
    pass


class AlkaliMetal(Metal):
    pass


class AlkalineEarthMetal(Metal):
    pass


class TransitionMetal(Metal):
    pass


class PostTransitionMetal(Metal):
    pass


class Metalloid(ChemicalElement):
    pass


class Actinide(TransitionMetal):
    pass


class Lanthanide(TransitionMetal):
    pass


class OtherNonmetal(Nonmetal):
    pass


class Halogen(Nonmetal):
    pass


class NobleGas(Nonmetal):
    pass


# PyQt5.QtCore.QRect(0, 29, 1920, 1001)

class Table(QtWidgets.QWidget):
    def __init__(self, screen):
        super().__init__()
        self.setupUI(screen)

    def setupUI(self, screen):
        self.screen = screen
        self.setWindowTitle('Neuronet #OSADCHAYA 2.0: Таблица')
        self.highframe = QtWidgets.QFrame(self)
        self.highframe.setStyleSheet('background-color: rgb(250, 250, 250);')
        self.lowframe = QtWidgets.QFrame(self)
        self.lowframe.setStyleSheet('background-color: rgb(192, 192, 192);')
        self.setform()

    def setform(self):
        self.mainbox = QtWidgets.QVBoxLayout()
        self.highgrid = QtWidgets.QGridLayout()
        self.lowgrid = QtWidgets.QGridLayout()

        self.mainbox.setSpacing(10)

        self.highframe.setLayout(self.highgrid)
        self.lowframe.setLayout(self.lowgrid)

        self.mainbox.addWidget(self.highframe)
        self.mainbox.addWidget(self.lowframe)
        self.setLayout(self.mainbox)

    def setplace(self):
        point = QtCore.QPoint((self.screen.width() - self.width())//2,(self.screen.height() - self.height())//2)
        self.move(point)
        self.showMaximized()


class Button(QtWidgets.QPushButton):
    def __init__(self, master, cls):
        super().__init__()
        self.setupUI(master, cls)

    def setupUI(self, m, c):
        dictionary = dict(zip(['AlkaliMetal', 'AlkalineEarthMetal', 'TransitionMetal', 'PostTransitionMetal',
                               'Metalloid', 'Actinide', 'Lanthanide', 'OtherNonmetal', 'Halogen',
                               'NobleGas', 'ChemicalElement'],
                              ['rgb(255, 0, 0)', 'rgb(255, 218, 185)', 'rgb(240, 128, 128)', 'rgb(119, 136, 153)',
                               'rgb(154, 205, 50)', 'rgb(153, 50, 204)','rgb(205, 104, 137)', 'rgb(173, 255, 47)',
                               'rgb(255, 255, 0)', 'rgb(127, 255, 212)', 'rgb(211,211,211)']))
        self.master = m
        self.cls = c
        if self.cls.group == '–':
            self.setParent(self.master.lowframe)
            self.setText('{}\n\n{}\n\n{}'.format(self.cls.atomic_number, self.cls.symbol,self.cls.element_native_lang))
            self.setStyleSheet('background-color: {};'.format(dictionary[str(self.cls.__class__).
                                                              replace("<class '__main__.", "").replace("'>", '')]))
            if self.cls.atomic_number in [int(i) for i in range(57, 72)]:
                if self.cls.atomic_number == 58:
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 0, 0)
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 0, 1)
                self.master.lowgrid.addWidget(self, 0, (self.cls.atomic_number - 57) + 2)
                if self.cls.atomic_number == 71:
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 0, 15)
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 0, 16)
            else:
                if self.cls.atomic_number == 90:
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 1, 0)
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 1, 1)
                self.master.lowgrid.addWidget(self, 1, (self.cls.atomic_number - 89) + 2)
                if self.cls.atomic_number == 103:
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 1, 15)
                    self.master.lowgrid.addWidget(QtWidgets.QWidget(), 1, 16)

        else:
            self.setParent(self.master.highframe)
            self.setText('{}\n\n{}\n\n{}'.format(self.cls.atomic_number, self.cls.symbol,self.cls.element_native_lang))
            self.setStyleSheet('background-color: {};'.format(dictionary[str(self.cls.__class__).
                                                              replace("<class '__main__.", "").replace("'>", '')]))
            self.master.highgrid.addWidget(self, self.cls.period - 1, self.cls.group - 1)

        self.clicked.connect(self.newWin)

    def newWin(self):
        self.window = ElemWindow(self.master,self.cls)

class ElemWindow(QtWidgets.QWidget):
    def __init__(self, master, cls):
        super().__init__()
        self.setupUI(master, cls)

    def setupUI(self, m, c):
        self.master = m
        self.cls = c
        self.master.hide()
        self.setWindowTitle('{}'.format(self.cls.element_native_lang))
        self.setStyleSheet('background-color: rgb(250, 250, 250);')
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setMidLineWidth(2)
        self.frame.setLineWidth(2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text = QtWidgets.QTextEdit(self)
        self.text.setText(str(self.cls))
        self.text.setFont(font)
        self.text.setReadOnly(True)

        self.setform()
        self.show()

    def setform(self):
        self.mainform = QtWidgets.QVBoxLayout()
        self.mainform.setContentsMargins(5,5,5,5)
        self.mainform.addWidget(self.frame)
        self.innerlayout = QtWidgets.QVBoxLayout(self.frame)
        self.frame.setLayout(self.innerlayout)
        self.innerlayout.setContentsMargins(5,5,5,5)
        self.innerlayout.addWidget(self.text)
        self.setLayout(self.mainform)

    def closeEvent(self, e):
        self.master.show()
        e.accept()

def init_elements(number, word):
    globals()[elembase[number][2]] = eval(word)(elembase[number][0], elembase[number][1],
                                                       elembase[number][2], elembase[number][3],
                                                       elembase[number][4], elembase[number][5],
                                                       elembase[number][6], elembase[number][7],
                                                       elembase[number][8], elembase[number][9],
                                                       elembase[number][10], elembase[number][11],
                                                       elembase[number][12])

for number in range(1, 118 + 1):
    if number in [3, 11, 19, 37, 55, 87]:
        init_elements(number, 'AlkaliMetal')
    elif number in [4, 12, 20, 38, 56, 88]:
        init_elements(number, 'AlkalineEarthMetal')
    elif number in [21, 22, 23, 24, 25, 26, 27, 28, 29, 39, 40, 41, 42, 43, 44, 45, 46, 47,
                    72, 73, 74, 75, 76, 77, 78, 79, 104, 105, 106, 107, 108]:
        init_elements(number, 'TransitionMetal')
    elif number in [13, 30, 31, 48, 49, 50, 80, 81, 82, 83, 84, 112]:
        init_elements(number, 'PostTransitionMetal')
    elif number in [5, 14, 32, 33, 51, 52, 85]:
        init_elements(number, 'Metalloid')
    elif number in [1, 6, 7, 8, 15, 16, 34]:
        init_elements(number, 'OtherNonmetal')
    elif number in [9, 17, 35, 53]:
        init_elements(number, 'Halogen')
    elif number in range(57, 72):
        init_elements(number, 'Lanthanide')
    elif number in range(89, 104):
        init_elements(number, 'Actinide')
    elif number in [109, 110, 111, 113, 114, 115, 116, 117, 118]:
        init_elements(number, 'ChemicalElement')
    elif number in [2, 10, 18, 36, 54, 86]:
        init_elements(number, 'NobleGas')
        
app = QtWidgets.QApplication(sys.argv)
win = Table(app.desktop().screenGeometry(app.desktop().primaryScreen()).size())
for i in range(1, 119):
    globals()['{}_btn'.format(elembase[i][2])] = Button(master=win, cls=globals()[elembase[i][2]])
win.setplace()
sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
qtCreatorFile = "playfair_kantor.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
                              
    rn = range(5)
    unwanted_characters = ['.', '-', ',', '!', '_', ')', '(', '<', '>']
    numbers = [t.upper()
               for t in ["+", "ě", "š", "č", "ř", "ž", "ý", "á", "í", "é"]]


    def get_matrix(self, key):
        rn = range(5)
        matrix = [['' for _i in rn] for _j in rn]
        alphabet = []
        row = 0
        col = 0

        for character in key:
            if character not in alphabet:
                matrix[row][col] = character
                alphabet.append(character)
            else:
                continue

            if (col == 4):
                col = 0
                row += 1
            else:
                col += 1

        for character in range(65, 91):
            if character == 74:
                continue

            if chr(character) not in alphabet:
                alphabet.append(chr(character))

        index = 0

        for i in rn:
            for j in rn:
                matrix[i][j] = alphabet[index]
                index += 1

        matrix[4][4] = ' '

        return matrix


    def handle_same_characters(self, text):
        index = 0

        while (index < len(text)):
            l1 = text[index]

            if index == len(text) - 1:
                text = text + 'X'
                index += 2
                continue

            l2 = text[index+1]

            if l1 == l2:
                text = text[:index + 1] + "X" + text[index + 1:]

            index += 2

        return text


    def get_index(self, character, matrix):
        rn = range(5)
        for i in rn:
            try:
                index = matrix[i].index(character)
                return (i, index)
            except:
                continue


    def encrypt(self):
        unwanted_characters = ['.', '-', ',', '!', '_', ')', '(', '<', '>']
        numbers = [t.upper()
                   for t in ["+", "ě", "š", "č", "ř", "ž", "ý", "á", "í", "é"]]
        output = ''
        key = self.vstup_klic.text()
        key = key.upper()
        key = key.replace(" ", "")
        for character in unwanted_characters:
            key = key.replace(character, "")
        key = "".join(dict.fromkeys(key))
        matrix = self.get_matrix(key)
        text = self.vstup_zasifrovani.text()
        text = text.upper()
        text = text.replace("J", "I")
        text = self.handle_same_characters(text)
        for character in unwanted_characters:
            text = text.replace(character, "")

        index = 0
        for character in text:
            if character in numbers:
                text[index] = numbers[numbers.index(character)]
            index += 1
        for (l1, l2) in zip(text[0::2], text[1::2]):
            if l1.isnumeric():
                output += numbers[int(l1)]
                continue

            if l2.isnumeric():
                output += numbers[int(l2)]
                continue

            row1, col1 = self.get_index(l1, matrix)
            row2, col2 = self.get_index(l2, matrix)

            if row1 == row2:
                output += matrix[row1][(col1 + 1) % 5] + \
                    matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                output += matrix[(row1 + 1) % 5][col1] + \
                    matrix[(row2 + 1) % 5][col2]
            else:
                output += matrix[row1][col2] + matrix[row2][col1]
        
        self.table(matrix)
        output = self.get_split_from_text(output)
        self.vystup.setText(output)


    def decrypt(self):
        unwanted_characters = ['.', '-', ',', '!', '_', ')', '(', '<', '>']
        numbers = [t.upper()
                   for t in ["+", "ě", "š", "č", "ř", "ž", "ý", "á", "í", "é"]]
        output = ''
        key = self.vstup_klic.text()
        key = key.upper()
        key = key.replace(" ", "")
        for character in unwanted_characters:
            key = key.replace(character, "")
        key = "".join(dict.fromkeys(key))
        matrix = self.get_matrix(key)
        text = self.vstup_desifrovani.text()
        text = text.upper()
        text = self.handle_same_characters(text)
        for character in unwanted_characters:
            text = text.replace(character, "")

        index = 0
        for character in text:
            if character in numbers:
                text[index] = numbers[numbers.index(character)]
            index += 1
        for (l1, l2) in zip(text[0::2], text[1::2]):
            if l1 in numbers:
                output += str(numbers.index(l1))
                continue

            if l2 in numbers:
                output += str(numbers.index(l2))
                continue

            row1, col1 = self.get_index(l1, matrix)
            row2, col2 = self.get_index(l2, matrix)

            if row1 == row2:
                output += matrix[row1][(col1 - 1) % 5] + \
                    matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                output += matrix[(row1 - 1) % 5][col1] + \
                    matrix[(row2 - 1) % 5][col2]
            else:
                output += matrix[row1][col2] + matrix[row2][col1]

        self.vystup.setText(output)


    def get_split_from_text(self, text, n=5):
        return ' '.join([text[i:i + n] for i in range(0, len(text), n)])

    def table(self, matrix):
        self.label_00.setText(matrix[0][0])
        self.label_01.setText(matrix[0][1])
        self.label_02.setText(matrix[0][2])
        self.label_03.setText(matrix[0][3])
        self.label_04.setText(matrix[0][4])
        self.label_05.setText(matrix[1][0])
        self.label_06.setText(matrix[1][1])
        self.label_07.setText(matrix[1][2])
        self.label_08.setText(matrix[1][3])
        self.label_09.setText(matrix[1][4])
        self.label_10.setText(matrix[2][0])
        self.label_11.setText(matrix[2][1])
        self.label_12.setText(matrix[2][2])
        self.label_13.setText(matrix[2][3])
        self.label_14.setText(matrix[2][4])
        self.label_15.setText(matrix[3][0])
        self.label_16.setText(matrix[3][1])
        self.label_17.setText(matrix[3][2])
        self.label_18.setText(matrix[3][3])
        self.label_19.setText(matrix[3][4])
        self.label_20.setText(matrix[4][0])
        self.label_21.setText(matrix[4][1])
        self.label_22.setText(matrix[4][2])
        self.label_23.setText(matrix[4][3])
        self.label_24.setText(matrix[4][4])
        
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.zasifrovat.clicked.connect(self.encrypt)
        self.desifrovat.clicked.connect(self.decrypt)
        
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

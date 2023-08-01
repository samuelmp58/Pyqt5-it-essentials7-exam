import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel, QCheckBox, QDesktopWidget
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
import requests
from bs4 import BeautifulSoup

class SpellcheckDialog(QDialog):
    def __init__(self, link):
        super().__init__()

        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(240, 240, 240))
        pal.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.setPalette(pal)
        self.resize(900, 400)
        

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.site = requests.get(link, headers=headers)
        self.sitesoup = BeautifulSoup(self.site.content, 'html.parser')
        self.li_list = self.sitesoup.find('ol').find_all('li')
        self.current_index = 0

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        font = QtGui.QFont("Arial", 14)
        self.label.setFont(font)
        #self.label.setGeometry(10, 20, self.width() + 240, self.height() - 70)
        self.label.setGeometry(10, 20, self.width() - 20, self.height() - 70)
        self.label.setWordWrap(True)
        self.checkbox = QCheckBox("Show Answers", self)
        self.checkbox.setGeometry(10, 300, 100, 30)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)

        self.proximo_button = QPushButton('Next', self)
        self.proximo_button.move(100, 350)
        self.proximo_button.clicked.connect(self.proximo)

        self.voltar_button = QPushButton('Previous', self)
        self.voltar_button.move(10, 350)
        self.voltar_button.clicked.connect(self.voltar)

        self.answer = False
        self.show_current_li()

    def on_checkbox_changed(self, state):
        self.answer = state == Qt.Checked
        self.show_current_li()

    def show_current_li(self):
        li = self.li_list[self.current_index]
        table = li.find('table')
        q1 = str(li)
        q1 = q1.replace("color: #ff0000;", "") if not self.answer else q1
        q1 = q1.replace(str(table), "") #if not self.answer else q1
        self.label.setText(q1)

    def proximo(self):
        next_li = self.li_list[self.current_index].find_next_sibling('li')
        if next_li:
            self.current_index = self.li_list.index(next_li)
            self.show_current_li()

    def voltar(self):
        next_li = self.li_list[self.current_index].find_previous_sibling('li')
        if next_li:
            self.current_index = self.li_list.index(next_li)
            self.show_current_li()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('IT 7.0 Exam')
        self.setGeometry(200, 200, 430, 210)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        chapters = [
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-1-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-2-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-3-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-4-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-5-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-6-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-7-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-8-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-9-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-10-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-11-exam-answers-ite-7-0-ite-7-02/",
            "https://infraexam.com/it-essentials-7/it-essentials-7-0-chapter-12-exam-answers-ite-7-0-ite-7-02/",
        ]

        self.buttons = []
        for idx, link in enumerate(chapters):
            button = QPushButton(f'Chapter {idx+1}', self)
            button.move(10 + (idx % 4) * 103, 35 * (idx // 4))
            button.clicked.connect(lambda checked, url=link: self.get_site(url))
            self.buttons.append(button)

    def get_site(self, url):
        spellcheck_dialog = SpellcheckDialog(url)
        spellcheck_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

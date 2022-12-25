from PyQt5 import QtWidgets
import random, time, sqlite3
from Ui_MainWindow import Ui_MainWindow

class Game(Ui_MainWindow):
    def __init__(self):
        self.i = 0
        self.mistakes = 0

    #Наследование интерфейса
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.buttons()

    #Добавление функционала кнопке и полю ввода
    def buttons(self):
        self.pushButton.clicked.connect(self.get_sentences)
        self.lineEdit.clicked.connect(self.run_timer)
        self.lineEdit.pressed.connect(self.run_game)

    #Метод для полчуения приложения из файла
    def get_sentences(self):
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText("")
        try:
            f = open('words.txt', 'r', encoding="utf-8").read()
        except Exception as e:
            print(e)
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        self.label.setText(f"{sentence}")

    #Запуск таймера по нажатию ЛКМ по полю ввода
    def run_timer(self):
        self.lineEdit.setReadOnly(False)
        self.tic = time.perf_counter()

    #Начало игры нажатием клавиши на клавиатуре
    def run_game(self):
        text_1 = f"'{self.label.text()[self.i]}'"
        if self.lineEdit.text() == "" or self.lineEdit.data == "''":
            return
        else:
            try:
                text_2 = f"'{self.lineEdit.text()[self.i]}'"
            except:
                return
        if text_1 != text_2:
            self.mistakes += 1
            self.lineEdit.setText(self.lineEdit.text()[:-1])
        elif text_1 == text_1:
            self.i += 1

        if self.label.text() == self.lineEdit.text():
            self.toc = time.perf_counter()
            timer = round(self.tic - self.toc, 1)
            accuracy = round(100 - (self.mistakes / len(self.label.text()) * 100), 1)
            speed = round((60 / round(self.tic - self.toc, 1)) * len(self.label.text())*-1)
            wpm = round(((len(self.label.text()) / 5) / (timer / 60))*-1)
            self.label_2.setText(f"Точность: {accuracy}%")
            self.label_3.setText((f"Скорость: {speed} сим/мин"))
            self.label_4.setText(f"Слов в минуту: {wpm}")
            get_Db(self.label.text(), wpm, accuracy, speed)
            self.reset()

    #Перезапуск игры после окончания придыдущего замера скорости
    def reset(self):
        self.lineEdit.setText('')
        self.lineEdit.setReadOnly(True)
        self.label.setText("Нажмите СТАРТ")
        self.i = 0
        self.mistakes = 0


#Подлючение БД
def get_Db(sentence, wpm, accuracy, speed):
    try:
        sqlite_connection = sqlite3.connect('sqlite3.db')
        cursor = sqlite_connection.cursor()

        table_creation = """CREATE TABLE IF NOT EXISTS db(sentence text, wpm integer, accuracy real, speed integer)"""

        cursor.execute(table_creation)

        sqlite_insert = """INSERT INTO db(sentence, wpm, accuracy, speed) VALUES (?, ?, ?, ?)"""

        data_tuple = (sentence, wpm, accuracy, speed)
        cursor.execute(sqlite_insert, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        return error
    finally:
        if sqlite_connection:
            sqlite_connection.close()

#Основной метод запуска программы
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Game()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

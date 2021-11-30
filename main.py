import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/app.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run_s2adv)
        self.pushButton_2.clicked.connect(self.run_flappy_bird)
        self.pushButton_3.clicked.connect(self.run_snake)
        """
        we upload the user to the database 
        if he is not there yet and change the coin
        """
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone() is None:
            cursor.execute("""INSERT INTO User
                              VALUES ('1', '0', '0',
                              '0', '-')"""
                           )
            conn.commit()
        """
        if there are no purchased games yet,
        then we suggest buying one
        """
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone()[4] == '-':
            self.pushButton.setText('BUY (1 coin)')
            self.pushButton_2.setText('BUY (1 coin)')
            self.pushButton_3.setText('BUY (1 coin)')

    def run_s2adv(self):
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone()[4] == '-':
            cursor.execute(f"""UPDATE User
                              SET purchased_games = 'S2ADV'""")
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Выполнена покупка игры")
            msg.setText("Выполнена покупка игры S2WAdventure")
            msg.exec_()
            self.pushButton.setText('PLAY')
        else:
            # TODO: starting the game, checking if there is no "-", debiting a coin or refusal
            pass

    def run_flappy_bird(self):
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone()[4] == '-':
            cursor.execute(f"""UPDATE User
                               SET purchased_games = 'Bird'""")
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Выполнена покупка игры")
            msg.setText("Выполнена покупка игры Bird")
            msg.exec_()
            self.pushButton_2.setText('PLAY')
        else:
            # TODO: starting the game, checking if there is no "-", debiting a coin or refusal
            pass

    def run_snake(self):
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone()[4] == '-':
            cursor.execute(f"""UPDATE User
                               SET purchased_games = 'Snake'""")
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Выполнена покупка игры")
            msg.setText("Выполнена покупка игры Snake")
            msg.exec_()
            self.pushButton_3.setText('PLAY')
        else:
            # TODO: starting the game, checking if there is no "-", debiting a coin or refusal
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

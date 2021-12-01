import os
import sqlite3
import sys

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
        s = cursor.execute("""SELECT * FROM User""").fetchone()
        self.label_8.setText(f'{s[0]}')
        self.label_8.setStyleSheet("QLabel { font-size:36pt; color:#fce94f; } ")
        """
        if there are no purchased games yet,
        then we suggest buying one
        """
        s = cursor.execute("""SELECT * FROM User""").fetchone()
        if s[4] == '-':
            self.pushButton.setText('BUY (1 coin)')
            self.pushButton_2.setText('BUY (1 coin)')
            self.pushButton_3.setText('BUY (1 coin)')
        else:
            if 'S2ADV' in s[4]:
                self.pushButton.setText('PLAY')
            else:
                self.pushButton.setText('BUY (1 coin)')
            if 'Bird' in s[4]:
                self.pushButton_2.setText('PLAY')
            else:
                self.pushButton_2.setText('BUY (1 coin)')
            if 'Snake' in s[4]:
                self.pushButton_3.setText('PLAY')
            else:
                self.pushButton_3.setText('BUY (1 coin)')
        """
        change defolt button settings
        """
        buttonsettings = '''
        QPushButton {
            border: 2px solid #876020;
        }
        QPushButton:hover:pressed {
            background-color: #967117;
        }
        '''
        self.pushButton.setStyleSheet(buttonsettings)
        self.pushButton_2.setStyleSheet(buttonsettings)
        self.pushButton_3.setStyleSheet(buttonsettings)

    def run_s2adv(self):
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone()[4] == '-':
            cursor.execute(f"""UPDATE User
                              SET purchased_games = 'S2ADV'""")
            conn.commit()
            cursor.execute(f"""UPDATE User
                               SET Coins = '0'""")
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Выполнена покупка игры")
            msg.setText("Выполнена покупка игры S2WAdventure")
            msg.exec_()
            self.pushButton.setText('PLAY')
            s = cursor.execute("""SELECT * FROM User""").fetchone()
            self.label_8.setText(f'{s[0]}')
            self.label_8.setStyleSheet("QLabel { font-size:36pt; color:#fce94f; } ")
        else:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM User""")
            s = (cursor.fetchone())
            if int(s[0]) - 1 >= 0 and 'S2ADV' not in s[4]:
                cursor.execute(f"""UPDATE User
                                   SET purchased_games = '{s[4]}, S2ADV'""")
                conn.commit()
                cursor.execute(f"""UPDATE User
                                   SET Coins = '{int(s[0]) - 1}'""")
                conn.commit()
                msg = QMessageBox()
                msg.setWindowTitle("Выполнена покупка игры")
                msg.setText("Выполнена покупка игры S2WAdventure")
                msg.exec_()
                self.pushButton.setText('PLAY')
                s = cursor.execute("""SELECT * FROM User""").fetchone()
                self.label_8.setText(f'{s[0]}')
                self.label_8.setStyleSheet("QLabel { font-size:36pt; color:#fce94f; } ")
            elif int(s[0]) - 1 < 0:
                msg = QMessageBox()
                msg.setWindowTitle("Не выполнена покупка игры")
                msg.setText("Не выполнена покупка игры S2WAdventure из-за недостатка средств")
                msg.exec_()
            elif 'S2ADV' in s[4]:
                ex.close()
                os.system('python3 games/S2WAdventure/main.py')
                ex.show()

    def run_flappy_bird(self):
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone()[4] == '-':
            cursor.execute(f"""UPDATE User
                               SET purchased_games = 'Bird'""")
            conn.commit()
            cursor.execute(f"""UPDATE User
                               SET Coins = '0'""")
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Выполнена покупка игры")
            msg.setText("Выполнена покупка игры Bird")
            msg.exec_()
            self.pushButton_2.setText('PLAY')
            s = cursor.execute("""SELECT * FROM User""").fetchone()
            self.label_8.setText(f'{s[0]}')
            self.label_8.setStyleSheet("QLabel { font-size:36pt; color:#fce94f; } ")
        else:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM User""")
            s = (cursor.fetchone())
            if int(s[0]) - 1 >= 0 and 'Bird' not in s[4]:
                cursor.execute(f"""UPDATE User
                                   SET purchased_games = '{s[4]}, Bird'""")
                conn.commit()
                cursor.execute(f"""UPDATE User
                                   SET Coins = '{int(s[0]) - 1}'""")
                conn.commit()
                msg = QMessageBox()
                msg.setWindowTitle("Выполнена покупка игры")
                msg.setText("Выполнена покупка игры Bird")
                msg.exec_()
                self.pushButton_2.setText('PLAY')
                s = cursor.execute("""SELECT * FROM User""").fetchone()
                self.label_8.setText(f'{s[0]}')
                self.label_8.setStyleSheet("QLabel { font-size:36pt; color:#fce94f; } ")
            elif int(s[0]) - 1 < 0:
                msg = QMessageBox()
                msg.setWindowTitle("Не выполнена покупка игры")
                msg.setText("Не выполнена покупка игры Bird из-за недостатка средств")
                msg.exec_()
            elif 'Bird' in s[4]:
                ex.close()
                os.system('python3 games/FlappyBird/main.py')
                ex.show()

    def run_snake(self):
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM User""")
        if cursor.fetchone()[4] == '-':
            cursor.execute(f"""UPDATE User
                               SET purchased_games = 'Snake'""")
            conn.commit()
            cursor.execute(f"""UPDATE User
                               SET Coins = '0'""")
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Выполнена покупка игры")
            msg.setText("Выполнена покупка игры Snake")
            msg.exec_()
            self.pushButton_3.setText('PLAY')
            s = cursor.execute("""SELECT * FROM User""").fetchone()
            self.label_8.setText(f'{s[0]}')
            self.label_8.setStyleSheet("QLabel { font-size:36pt; color:#fce94f; } ")
        else:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM User""")
            s = (cursor.fetchone())
            if int(s[0]) - 1 >= 0 and 'Snake' not in s[4]:
                cursor.execute(f"""UPDATE User
                                   SET purchased_games = '{s[4]}, Snake'""")
                conn.commit()
                cursor.execute(f"""UPDATE User
                                   SET Coins = '{int(s[0]) - 1}'""")
                conn.commit()
                msg = QMessageBox()
                msg.setWindowTitle("Выполнена покупка игры")
                msg.setText("Выполнена покупка игры Snake")
                msg.exec_()
                self.pushButton_3.setText('PLAY')
                s = cursor.execute("""SELECT * FROM User""").fetchone()
                self.label_8.setText(f'{s[0]}')
                self.label_8.setStyleSheet("QLabel { font-size:36pt; color:#fce94f; } ")
            elif int(s[0]) - 1 < 0:
                msg = QMessageBox()
                msg.setWindowTitle("Не выполнена покупка игры")
                msg.setText("Не выполнена покупка игры Snake из-за недостатка средств")
                msg.exec_()
            elif 'Snake' in s[4]:
                ex.close()
                os.system('python3 games/WarShake/main.py')
                ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

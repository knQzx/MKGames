import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/app.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run_s2adv)
        self.pushButton_2.clicked.connect(self.run_flappy_bird)
        self.pushButton_3.clicked.connect(self.run_snake)

    def run_s2adv(self):
        # TODO: run game
        pass

    def run_flappy_bird(self):
        # TODO: run game
        pass

    def run_snake(self):
        # TODO: run game
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

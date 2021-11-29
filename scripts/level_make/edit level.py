import msgpack
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QWidgetItem, QPushButton, QButtonGroup


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.download_data()
        self.initUi()

    def download_data(self):
        with open("data.msgpack", "rb") as data_file:
            self.data = msgpack.unpackb(data_file.read())

    def initUi(self):
        self.add_layout()
        self.add_data()

    def add_layout(self):
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

    def add_data(self):
        self.button_group = QButtonGroup(self)
        self.button_group.buttonClicked.connect(self.update_button)
        self.world_num = input('Number of world: ')
        self.world = self.data[f'world{self.world_num}']
        for row in range(self.data['height']):
            for col in range(self.data['width']):
                button = QPushButton(self)
                button.setText(self.world[row][col])
                self.button_group.addButton(button)
                self.layout.addItem(QWidgetItem(button), row, col)

    def update_button(self, button):
        state_list = ['.', '-', '|', '#', 'F', 'D']
        cur_state = state_list.index(button.text())
        button.setText(state_list[(cur_state + 1) % len(state_list)])
        row, col, _, _ = self.layout.getItemPosition(self.layout.indexOf(button))
        self.world[row][col] = button.text()
        with open("data.msgpack", "wb") as outfile:
            packed = msgpack.packb(self.data)
            outfile.write(packed)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QScrollArea()
    window.setWidget(Window())
    window.show()
    sys.exit(app.exec())

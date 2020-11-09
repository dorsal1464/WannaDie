from PyQt5 import QtWidgets, uic
import sys
from main import *
from client import Client


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        self.client = Client()
        uic.loadUi('main.ui', self)  # Load the .ui file
        self.decryptBtn = self.findChild(QtWidgets.QPushButton, 'decryptBtn')
        self.decryptBtn.clicked.connect(self.decrypt)
        self.keyIn = self.findChild(QtWidgets.QLineEdit, 'keyIn')
        self.ivIn = self.findChild(QtWidgets.QLineEdit, 'ivIn')
        self.status = self.findChild(QtWidgets.QTextEdit, 'statusConsole')
        id = get_random_bytes(32)
        self.text = 'ID: '+hexlify(id).decode()+'\n'
        self.status.setPlainText(self.text)
        self.update("Encrypting...")
        encrypt(self.client, id)
        self.update("done encrypting")
        self.show()  # Show the GUI

    def update(self, msg):
        self.text += msg+"\n"
        self.status.setPlainText(self.text)

    def decrypt(self):
        self.update("Decrypting...")
        key = self.keyIn.text()
        iv = self.ivIn.text()
        decrypt(self.update, key, iv)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Ui()  # Create an instance of our class
    app.exec_()  # Start the application


if __name__ == "__main__":
    main()

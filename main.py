from PySide6.QtWidgets import QApplication
from app.ui import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

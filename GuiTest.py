import sys
import PyQt4.QtGui as QtGui

def main():
    app=QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    window.resize(250,150)
    window.move(300,300)
    window.setWindowTitle("Simple")
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


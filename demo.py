#!/usr/bin/env python

import sys
from time import sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication

class Demo(QMainWindow) :
    """Build a game demo."""

    def __init__( self, parent=None ):
        super().__init__(parent)
        uic.loadUi("Demo.ui", self)

        self.button.clicked.connect(self.buttonClickedHandler)

    def updateUI ( self ):
        self.outputLabel.setText("Click!")        # Add your code here to update the GUI view so it matches the game state.

    def buttonClickedHandler( self ):
        print("Button clicked")            # Replace this line with your roll event handler

        def crapGame(dice):
            firstRolled = randint(1, 6) + randint(1, 6)
            if firstRolled == '7' or '11':
                print("You win!")
            elif firstRolled == '2' or '3' or '12':
                print("You lose!")
            else:
                def rollAgain(dice):
                    secondRolled = randint(1, 6) + randint(1, 6)
                    if secondRolled == firstRolled:
                        print("You win!")
                    elif secondRolled == '7':
                        print("You lose!")

        self.updateUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    diceApp = Demo()
    diceApp.show()
    sys.exit(app.exec_())



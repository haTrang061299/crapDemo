#!/usr/bin/env python

from die import *
import sys
import crapsResources_rc
from time import sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication

class Craps(QMainWindow) :
    """A game of Craps."""
    die1 = die2 = None

    def __init__( self, parent=None ):
        """Build a game with two dice."""

        super().__init__(parent)
        uic.loadUi("Craps.ui", self)

        self.bidSpinBox.setRange ( 10, 100 )
        self.bidSpinBox.setSingleStep ( 5 )

        self.die1 = Die()
        self.die2 = Die()
        self.lastRoll = 0
        self.valueRolled = 0
        self.currentBet = 0
        self.results = ("Roll to play")
        self.firstRoll = True
        self.wins = 0
        self.losses = 0
        self.bank = 500
        self.buttonText = "Roll"

             #          0  1  2  3  4    5    6    7    8    9    10   11   12
        self.payouts = [0, 0, 0, 0, 2.0, 1.5, 1.2, 1.0, 1.2, 1.5, 2.0, 1.0, 0]

        self.rollButton.clicked.connect(self.rollButtonClickedHandler)

    def __str__( self ):
        """String representation for Dice."""

        return "Die1: %s\nDie2: %s" % ( str(self.die1),  str(self.die2) )

    def updateUI ( self ):
        print("Die1: {0}, Die2: {1}".format(self.die1.getValue(),  self.die2.getValue()))
        self.die1View.setPixmap(QtGui.QPixmap( ":/" + str( self.die1.getValue() ) ) )
        self.die2View.setPixmap(QtGui.QPixmap( ":/" + str( self.die2.getValue() ) ) )
        # Add your code here to update the GUI view so it matches the game state.
        self.lossesLabel.setText(str(self.losses))
        self.winsLabel.setText(str(self.wins))
        self.rollingForLabel.setNum(int(self.valueRolled))
        self.bankValue.setNum(int(self.bank))
        self.resultsLabel.setText(str(self.results))
		# Player asked for another roll of the dice.
    def rollButtonClickedHandler ( self ):
        self.currentBet = self.bidSpinBox.value()
        winsCount = 0
        lossesCount = 0
        # Play the first roll
        self.valueRolled = self.die1.roll() + self.die2.roll()
        if self.firstRoll:
            if self.valueRolled == 7 or self.valueRolled == 11:
                winsCount +=1
                self.wins += winsCount
                self.bank += self.currentBet
                self.results = ("Great, You win!")
                print("You win!")
            elif self.valueRolled in (2, 3, 12):
                lossesCount +=1
                self.losses += lossesCount
                self.bank -= self.currentBet
                self.results = ("Oh, You lose!")
                print("You lose!")
            else:
                self.lastRoll = self.valueRolled
                self.firstRoll = False
        else:
            if self.valueRolled == self.lastRoll:
                self.wins +=1
                self.bank += self.currentBet
                self.results = ("Yay, You won!")
                print("Won!")
            else:
                self.losses += 1
                self.bank -= self.currentBet
                self.results = ("Lose :(")
                print("Lose")
            self.firstRoll = True

        self.updateUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    diceApp = Craps()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())



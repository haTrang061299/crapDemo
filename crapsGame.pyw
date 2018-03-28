#!/usr/bin/env python

from die import *
import sys
from os import path
import crapsResources_rc
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from PyQt5.QtCore import pyqtSlot, Qt, QSettings, QCoreApplication
from PyQt5 import QtGui, uic, QtCore
from PyQt5.QtWidgets import  QMainWindow, QApplication, QDialog, QFileSystemModel, QDialogButtonBox, QHeaderView, QMessageBox

startingBankDefault = 100
maxinumBetValueDefault = 100
minimumBetValueDefault = 10
logFilenameDefault = 'craps.log'
pickleFilenameDefault = ".crapsSavedObjects.pl"

class Craps(QMainWindow) :
    """A game of Craps."""
    die1 = die2 = None

    def __init__( self, parent=None ):
        """Build a game with two dice."""

        super().__init__(parent)
        self.logger = getLogger("Trang.craps")
        self.appSettings = QSettings()
        self.quitCounter = 0
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
        self.currentBank = 500
        self.buttonText = "Roll"

             #          0  1  2  3  4    5    6    7    8    9    10   11   12
        self.payouts = [0, 0, 0, 0, 2.0, 1.5, 1.2, 1.0, 1.2, 1.5, 2.0, 1.0, 0]
        self.pickleFilename = pickleFilenameDefault

        self.restoreSettings()

        if path.exists(self.pickleFilename):
            self.die1, self.die2, self.firstRoll, self.results, self.playerLost, self.firstRollValue, self.buttonText, self.wins, self.losses, self.currentBet, self.currentBank = self.restartGame()
        else:
            self.restartGame()

        self.rollButton.clicked.connect(self.rollButtonClickedHandler)
        self.preferencesButton.clicked.connect(self.preferencesButtonClickedHandler)

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
        self.bankValue.setNum(int(self.currentBank))
        self.resultsLabel.setText(str(self.results))
		# Player asked for another roll of the dice.

    def restartGame(self):
        self.die1 = Die()
        self.die2 = Die()
        self.die1.setValue(5)
        self.die2.setValue(6)
        self.firstRoll = True
        self.results = ""
        self.playerLost = False
        self.firstRollValue = 0
        self.buttonText = "Roll"
        self.wins = 0
        self.losses = 0
        self.currentBet = 0
        self.currentBank = self.startingBank

    def saveGame(self):
        saveItems = (self.die1, self.die2, self.firstRoll, self.results, self.playerLost, self.firstRollValue, self.buttonText, self.wins, self.losses, self.currentBet, self.currentBank)
        if self.appSettings.contains("pickleFilename"):
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value("pickleFilename", type=str)), 'wb') as pickleFile:
                dump(saveItems, pickleFile)
        else:
            self.logger.critical("No pickle filename")

    def restoreGame(self):
        if self.appSettings.contains("pickleFilename"):
            self.appSettings.value("pickleFilename", type = str)
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value("pickleFilename", type=str)), 'rb') as pickleFile:
                return load(pickleFile)
        else:
            self.logger.critical("No pickle filename")


    def restoreSettings(self):
        if self.appSettings.contains('startingBank'):
            self.startingBank = self.appSettings.value('startingBank', type=int)
        else:
            self.startingBank = startingBankDefault
            self.appSettings.setValue('startingBank', self.startingBank_)

        if self.appSettings.contains('maximumBet'):
            self.maximumBet = self.appSettings.value('maximumBet', type=int)
        else:
            self.maximumBet = maxinumBetValueDefault
            self.appSettings.setValue('maximumBet', self.maximumBet_)
        if self.appSettings.contains('minumumBet'):
            self.minimumBet = self.appSettings.value('minimumBet', type = int)
        else:
            self.minimumBet = self.minimumBetDefault
            self.appSettings.setValue('minimumBet', self.minimumBet_)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile = self.appSettings.value('createLogFile', type = bool)
        else:
            self.createLogFile = logFilenameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile_)
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
                self.currentBank += self.currentBet
                self.results = ("Great, You win!")
                print("You win!")
            elif self.valueRolled in (2, 3, 12):
                lossesCount +=1
                self.losses += lossesCount
                self.currentBank -= self.currentBet
                self.results = ("Oh, You lose!")
                print("You lose!")
            else:
                self.lastRoll = self.valueRolled
                self.firstRoll = False
        else:
            if self.valueRolled == self.lastRoll:
                self.wins +=1
                self.currentBank += self.currentBet
                self.results = ("Yay, You won!")
                print("Won!")
            else:
                self.losses += 1
                self.currentBank -= self.currentBet
                self.results = ("Lose :(")
                print("Lose")
            self.firstRoll = True

        self.updateUI()
    @pyqtSlot()
    def preferencesButtonClickedHandler(self):
        print("Setting preferences")
        self.logger.info("Setting preferences")
        preferencesDialog = PreferencesDialog()
        preferencesDialog.show()
        preferencesDialog.exec_()
        self.restoreSetting()
        self.updateUI()

    def closeEvent(self, event):
        if self.quitCounter == 0:
            self.quitCounter +=1
            quitMessage = "Are you sure you want to quit?"
            reply = QMessageBox.question(self, "Message", quitMessage, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.saveGame()
                event.accept()
            else:
                event.ignore()
            return super().closeEvent(event)

class PreferencesDialog(QDialog):
        def __init__(self, parent = Die):
            super(PreferencesDialog, self).__init__()

            uic.loadUi('window.ui', self)

            self.appSettings = QSettings()
            if self.appSettings.contains('startingBank'):
                self.startingBank = self.appSettings.value('startingBank', type = int)
            else:
                self.startingBank = startingBankDefault
                self.appSettings.setValue('startingBank', self.startingBank)

            if self.appSettings.contains('maximumBet'):
                self.maximumBet = self.appSettings.value('maximumBet', type = int)
            else:
                self.maximumBet = minimumBetValueDefault
                self.appSettings.setValue('maximumBet', self.maximumBet)

            if self.appSettings.contains('minimumBet'):
                self.minimumBet = self.appSettings.value('minimumBet', type = int)
            else:
                self.minimumBet = minimumBetValueDefault
                self.appSettings.setValue('minimumBet', self.minimumBet)

            if self.appSettings.contains('createLogFile'):
                self.createLogFile = self.appSettings.value('createLogFile', type = bool)
            else:
                self.createLogFile = logFilenameDefault
                self.appSettings.setValue('createLogFile', self.createLogFile)

            self.buttonBox.rejected.connect(self.cancelClickedHandler)
            self.buttonBox.accepted.connect(self.okayClickedHandler)
            self.startingBankValue.editingFinished.connect(self.startingBankValueChanged)
            self.maximumBetValue.editingFinished.connect(self.maximumBetValueChanged)
            self.minimumBetValue.editingFinished.connect(self.minimumBetValueChanged)
            self.createLogFileCheckBox.stateChanged.connect(self.createLogFileChanged)

            self.updateUI()

        def startingBankValueChanged(self):
            self.startingBank = int(self.bank.text())

        def maximumBetValueChanged(self):
            self.maximumBet = int(self.maximumBetValue.text())

        def minimumBetValueChanged(self):
            self.minimumBet = int(self.minimumBetValue.text())

        def createLogFileChanged(self):
            self.createLogFile = self.createLogFileCheckBox

        def updateUI(self):
            self.startingBankValue.setText(str(self.startingBank))
            self.maximumBetValue.setText(str(self.maximumBet))
            self.minimumBetValue.setText(str(self.minimumBet))
            if self.createLogFile:
                # if not self.createLogFileCheckBox.isChecked():
                    self.createLogFileCheckBox.setCheckState(Qt.Checked)
            else:
                if self.createLogFileCheckBox.isChecked():
                    self.createLogFileCheckBox.setCheckState(Qt.Unchecked)

        def okayClickedHandler(self):
            # basePath = path.dirname(path.realpath(__file__))
            # self.logFileName = "dice.log"
            self.preferencesGroup = (('startingBank', self.startingBank),\
                                     ('maximumBet', self.maximumBet),\
                                     ('minimumBet', self.minimumBet),\
                                     ('createLogFile', self.createLogFile))

            for setting, variableName in self.preferencesGroup:
                self.appSettings.setValue(setting, variableName)
            self.close()

        def cancelClickedHandler(self):
            self.close()







if __name__ == "__main__":
    QCoreApplication.setOrganizationName("Trang Software");
    QCoreApplication.setOrganizationDomain("trangsoftware.com");
    QCoreApplication.setApplicationName("Craps");
    appSettings = QSettings()
    startingFolderName = path.dirname(path.realpath(__file__))
    if appSettings.contains('logFile'):
        logFilename = appSettings.value('logFile', type=str)
    else:
        logFilename = logFilenameDefault
        appSettings.setValue('logFile', logFilename)
    basicConfig(filename = path.join(startingFolderName, logFilename), level=INFO, format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s')
    app = QApplication(sys.argv)
    diceApp = Craps()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())


#!/usr/bin/env python3
# Pi-Ware main UI

from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKitWidgets import QWebView , QWebPage
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtNetwork import *

import subprocess
import os
import sys
import webbrowser
from functools import partial
import getpass

#Set global variables
global username
username = getpass.getuser()
global pwversion
with open(f'/home/{username}/.local/share/pi-ware-pyqt5/version') as f:
    pwver = f.read()
    f.close()

#Import custom  pi-ware functions
from apps import *

#Developer check
def istherefile(file): # This Function checks whether a file exists
    try:
        file_tst = open(file)
        file_tst.close()
    except FileNotFoundError:
        return False
    else:
        return True

#Check if dev files exist
if istherefile(f"/home/{username}/pi-ware-pyqt5/.dev"):
    IsDev = "True"
else:
    IsDev = "False"

def featuredTab(parent):
     widget = QWidget(parent)
     layout = QVBoxLayout(widget)
     browser = QWebView(widget)
     browser.showMaximized()
     browser.setUrl(QUrl("http://pi-ware-telemetry.ml/widget-2/"))
     layout.addWidget(browser)
     widget.setLayout(layout)
     return widget

def appsTab(parent):
     widget = QWidget(parent)
     scrollbar_widget = QWidget(widget)
     scroll_layout = QVBoxLayout(scrollbar_widget)
     apps = parseApps()
     appWindows = list()
     for app in apps:                                          
          btn = QPushButton(app.name, widget)            
          text = btn.text()
          btn.setIcon(QtGui.QIcon(app.icon))
          btn.app = AppWindow(app)
          btn.clicked.connect(btn.app.show)
          scroll_layout.addWidget(btn)
     scroll_layout.addStretch(1)
     scroll = QScrollArea()
     scroll.setWidget(scrollbar_widget)
     scroll.setWidgetResizable(True)
     layout = QVBoxLayout(widget)
     layout.addWidget(scroll)
     widget.setLayout(layout)
     return widget

def wikiTab(parent):
     widget = QWidget(parent)
     layout = QVBoxLayout(widget)
     browser = QWebView(widget)
     browser.showMaximized()
     browser.setUrl(QUrl("http://github.com/piware14/pi-ware/wiki"))
     layout.addWidget(browser)
     widget.setLayout(layout)
     return widget

def DEVTab(parent):
    widget = QWidget(parent)
    layout = QGridLayout(widget)
    apps = parseApps()
    totalapps = 0
    for app in apps:
        totalapps = totalapps+1
    #Apps
    Totalappstext = QLabel("Total Apps:")
    Totalappstext.setFont(QFont('Arial', 30))
    layout.addWidget(Totalappstext, 0, 0)
    appcount = QLabel(f'{totalapps}')
    appcount.setFont(QFont('Arial', 30))
    layout.addWidget(appcount, 0, 1)
    #Version
    Versiontext = QLabel("Version:")
    Versiontext.setFont(QFont('Arial', 30))
    layout.addWidget(Versiontext, 1, 0)
    versiontext = QLabel(f'{pwver}')
    versiontext.setFont(QFont('Arial', 15))
    layout.addWidget(versiontext, 1, 1)
    #Set layout
    widget.setLayout(layout)
    return widget

linkTemplate = '<a href={0}>{1}</a>'
class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet('font-size: 35px')
        self.setOpenExternalLinks(True)
        self.setParent(parent)

#Link example:
#label1 = HyperlinkLabel(self)
#label1.setText(linkTemplate.format('https://Google.com', 'Google.com'

class PiWare(QMainWindow):
     def __init__(self, x):
         super(PiWare, self).__init__()
         #self.resize(300, 800)
         self.setWindowIcon(QtGui.QIcon(f'/home/{username}/pi-ware-pyqt5/icons/logo-full.png'))
         self.setWindowTitle("Pi-Ware")
         self.table_widget = Tabs(self)
         self.setCentralWidget(self.table_widget)      

class Tabs(QTabWidget):
   def __init__(self, parent = None):
      super(Tabs, self).__init__(parent)
      self.featuredTab = featuredTab(self)
      self.appsTab = appsTab(self)
      self.wikiTab = wikiTab(self)
      self.addTab(self.featuredTab,"Featured")
      self.addTab(self.appsTab,"Apps")
      self.addTab(self.wikiTab,"Wiki")
      if IsDev == "True":
          self.DEVTab = DEVTab(self)
          self.addTab(self.DEVTab,"Developer Information")

class AppWindow(QWidget):
    def __init__(self, app: App):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(f'{app.icon200}'))
        self.setWindowTitle(f'{app.name}')
        layout = QGridLayout()
        self.install_script = app.install
        self.uninstall_script = app.uninstall
        self.nameLabel = QLabel(app.name)
        self.nameLabel.setFont(QFont('Arial', 30))
        layout.addWidget(self.nameLabel, 0, 0)
        logoLabel = QLabel(self)
        logoPixmap = QPixmap(app.icon200)
        logoLabel.setPixmap(logoPixmap)
        layout.addWidget(logoLabel, 1, 0)
        archLabel = QLabel("Architecture: "+app.architecture)
        layout.addWidget(archLabel, 0, 1)
        descLabel = QLabel("\n"+app.description+"\n\n"+app.website)
        layout.addWidget(descLabel, 1, 1)
        installButton = QPushButton("Install")
        installButton.clicked.connect(self.install)
        layout.addWidget(installButton, 2, 0)
        uninstallButton = QPushButton("Uninstall")
        uninstallButton.clicked.connect(self.uninstall)
        layout.addWidget(uninstallButton, 2, 1)
        self.setLayout(layout)

    def install(self):
         if IsDev == "True":
             print(f"bash /home/{username}/pi-ware/func/term/term-run {self.install_script}")
         os.system(f"bash /home/{username}/pi-ware/func/term/term-run {self.install_script}")

    def uninstall(self):
        if IsDev == "True":
            print(f"bash /home/{username}/pi-ware/func/term/term-run {self.uninstall_script}")
        os.system(f"bash /home/{username}/pi-ware/func/term/term-run {self.uninstall_script}")

if __name__ == '__main__':
     app = QApplication([])
     window = PiWare(3)
     app.setStyle('Breeze')
     window.show()
     sys.exit(app.exec_())

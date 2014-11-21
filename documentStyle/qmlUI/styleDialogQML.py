'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal

from documentStyle.qmlUI.qmlMaster import QmlMaster
from documentStyle.qmlUI.qmlDelegate import QmlDelegate


class StyleSheetDialogQML(QObject):
  '''
  QML GUI form of StyleSheetDialog
  
  Static: QML declaration must match the formation.
  Formation has the models?
  
  Abstract, uses Template pattern: subclasses specialize substeps of algorithm i.e. adding buttons and enabling
  '''

  accepted = Signal()
  rejected = Signal()

  def __init__(self, parentWindow, formation, titleParts):  # , flags=Qt.Dialog, ):
    
    # TODO, parentWindow should be the document, which may not be the activeWindow?
    # parentWindow = QCoreApplication.instance().activeWindow()
    super(StyleSheetDialogQML, self).__init__() # parent=parentWindow, flags=flags)
    
    qmlFilename = "resources/qml/stylesheet.qml"
    
    qmlMaster = QmlMaster()
    self.styleQuickView = qmlMaster.quickViewForQML(qmlFilename)
    self.dialogDelegate = qmlMaster.findComponent(quickview=self.styleQuickView, 
                                                       className=QmlDelegate, 
                                                       objectName="dialogDelegate")
    
  def open(self):
    print("TODO open")
    # self.quickView.show()
    ''' ??? showing crashes. '''
    self.dialogDelegate.activate()
    

    
  
    
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
    self.createDialog(parentWindow)
    
    
    
  def createDialog(self, parentWindow):
    qmlFilename = "resources/qml/stylesheet.qml"
    
    qmlMaster = QmlMaster()
    qwin = qmlMaster.appQWindow()
    self.styleQuickView = qmlMaster.quickViewForQML(qmlFilename, transientParent=qwin)
    self.dialogDelegate = qmlMaster.findComponent(quickview=self.styleQuickView, 
                                                  className=QmlDelegate, 
                                                  objectName="dialogDelegate")
    assert self.dialogDelegate is not None
    
    "Wrap it, so it is visible?"
    " container takes ownership.  container is a widget"
    self.container = qmlMaster.widgetForQuickView(self.styleQuickView, parentWindow)
    
    
    
  
  def createDialog2(self):
    qmlFilename = "resources/qml/stylesheet.qml"
    
    qmlMaster = QmlMaster()
    qwin = qmlMaster.appQWindow()
    self.widget, self.styleQuickView = qmlMaster.widgetAndQuickViewForQML(qmlFilename, transientParent=qwin)
    
    self.dialogDelegate = qmlMaster.findComponent(quickview=self.styleQuickView, 
                                                  className=QmlDelegate, 
                                                  objectName="dialogDelegate")
    assert self.dialogDelegate is not None
    
  def open(self):
    '''
    execute the dialog.
    Just show() ing is not enough.
    Tell delegate to call QML Dialog method open()
    '''
    self.dialogDelegate.activate()
    

    
  
    
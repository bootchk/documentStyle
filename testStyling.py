#!/usr/bin/env python

'''
A Qt app that demonstrates DocumentElement (QGraphicItem) styling.

Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''
import sys

# Set PyQt API version to 2
import sip
API_NAMES = ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]
API_VERSION = 2
for name in API_NAMES:
  sip.setapi(name, API_VERSION)
  
  
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSlot as Slot
from PyQt4.QtGui import *

from documentStyle.styleSheetCascadion import StyleSheetCascadion
from documentStyle.styleable import Styleable


'''
Test cases:

Undo/Redo (nonstacking.)
Style an element.
Undo style an element.
Redo style an element.
-> element is restored
Style element again.
Redo (really a reset)
-> element is restored to original

Saving Stylesheet:
Save.
Change.
Restore
-> document is restored to original style
'''
    

'''
DocumentElements (aka Morph, QGraphicItem, or other custom classes)
'''

class LineItem(Styleable, QGraphicsLineItem):
  def __init__(self, x1, y1, x2, y2):
    QGraphicsLineItem.__init__(self, x1, y1, x2, y2)
    self.setStylingDocumentElementType("Line")
  
  def scalePen(self, pen, value):
    unscaledWidth = value
    itemScale = self.scale()  # !!! scale is used for 1D sizing
    scaledWidthF = 1.0/itemScale * unscaledWidth
    
    # !!! Note float value and setWidthF is float setter
    pen.setWidthF(scaledWidthF)
    

class TextItem(Styleable, QGraphicsTextItem):
  def __init__(self, text):
    QGraphicsTextItem.__init__(self, text)
    self.setStylingDocumentElementType("Text")
    
  
  
class EllipseItem(Styleable, QGraphicsEllipseItem):
  def __init__(self):
    QGraphicsEllipseItem.__init__(self)
    self.setRect(30, 30, 40, 40)
    self.setStylingDocumentElementType("Shape")
  
  def scalePen(self, pen, value):
    unscaledWidth = value
    '''
    !!! transform is used for 2D sizing.
    Scale pen to min of x,y dimension.
    '''
    itemScale = min(self.transform().m11(), self.transform().m22())
    scaledWidthF = 1.0/itemScale * unscaledWidth
    
    # !!! Note float value and setWidthF is float setter
    pen.setWidthF(scaledWidthF)

  
  
class PixmapItem(Styleable, QGraphicsPixmapItem ):
  def __init__(self, filename):
    pic = QPixmap(filename)
    assert not pic.isNull()  # file or encoding exceptions
    QGraphicsPixmapItem.__init__(self, pic)
    self.setPos(100,100)
    self.setStylingDocumentElementType("Pixmap")
    
 
 
 

class DiagramScene(QGraphicsScene):
  def __init__(self, *args):
    QGraphicsScene.__init__(self, *args)
    
    self.addItem(TextItem("RMB styles item.\n a,u,d, keys edit stylesheets, s,r save/restore doc stylesheet"))
    self.addItem(EllipseItem())
    # Two lines to show that both are styled by docStyleSheet change
    self.addItem(LineItem(80, 80, 80, 150))
    self.addItem(LineItem(90, 90, 90, 160))
    #self.addItem(PixmapItem("/home/bootch/Pictures/smalldonkey.png"))
    #self.addItem(PixmapItem("/home/bootch/ufoWTransparent.png"))
    self.addItem(PixmapItem("data/smalldonkey.png"))

  
  @Slot()
  def polish(self):
    '''
    Restyle on signal styleSheetchanged.
    '''
    print ">>>testStyling polishing document"
    for item in self.items():
      item.polish()
    
    
  def restoreItemsToStyleCascade(self):
    ''' reparent item's to new DSS in cascade. '''
    for item in self.items():
      item.addToStyleCascade()
  
    
   
class GraphicsView(QGraphicsView):
  def __init__(self, scene):
    super(GraphicsView, self).__init__(scene)
    
    assert self.dragMode() == QGraphicsView.NoDrag
    
    self.setRenderHint(QPainter.Antialiasing)
    self.setRenderHint(QPainter.TextAntialiasing)
    self.scene = scene
    
  
  def keyPressEvent(self, event):
    # Let user edit a StyleSheet
    key = event.key()
    if key == Qt.Key_A:
      QCoreApplication.instance().cascadion.appStyleSheet.edit()
    elif key == Qt.Key_D:
      QCoreApplication.instance().cascadion.docStyleSheet.edit()
    elif key == Qt.Key_U:
      QCoreApplication.instance().cascadion.userStyleSheet.edit()
    elif key == Qt.Key_S:
      print "Saved doc stylesheet"
      self.pickledDSS = QCoreApplication.instance().cascadion.pickleDocStyleSheet()
    elif key == Qt.Key_R:
      print "Restored doc stylesheet"
      QCoreApplication.instance().cascadion.restoreDocStyleSheet(self.pickledDSS)
      # !!! So far we have only tested unpickling.) 
      # To complete test, tell document to reparent documentElements (if they already exist)
      self.scene.restoreItemsToStyleCascade()
      # Now must polish (via events or otherwise.)

       
class MainWindow(QMainWindow):
  def __init__(self, *args):
    QMainWindow.__init__(self, *args)
    
  def newDocument(self):
    ''' Widget for new document (scene). '''
    self.scene = DiagramScene()
    self.view = GraphicsView(self.scene)
    self.setCentralWidget(self.view)
    return self.view
    
  def closeEvent(self, event):
    print "App closed"
    QCoreApplication.instance().cascadion.saveUserStylesheetAsSettings()
    event.accept()
  
  
    
       
class App(QApplication):
  
  def __init__(self, args):
    super(App, self).__init__(args)
    
    self.setOrganizationName("DocumentStyle")
    self.setOrganizationDomain("lloyd konneker")
    self.setApplicationName("testStyling")
    
    # Must precede creation of document because documentElementStyleSheets parented to docStyleSheet
    self.cascadion = StyleSheetCascadion() 
    
    mainWindow = MainWindow()
    self.documentView = mainWindow.newDocument()
    mainWindow.setGeometry(100, 100, 500, 400)
    mainWindow.show()
    self.mainWindow = mainWindow
    
    # Arrange that changes to styleSheets will polish doc
    self.cascadion.connectSignals(mainWindow.scene.polish)
    
    # Initial polishing (using Styleable)
    mainWindow.scene.polish()
    
    self.exec_()
 
    
  
app = App(sys.argv)


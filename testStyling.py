#!/usr/bin/env python

'''
A Qt app that demonstrates DocumentElement (QGraphicItem) styling.

Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import *
from PySide.QtGui import *
import sys

from documentStyle.styleSheet.appStyleSheet import AppStyleSheet
from documentStyle.styleSheet.intermediateStyleSheet import IntermediateStyleSheet
from documentStyle.styleable import Styleable


    

'''
DocumentElements (aka Morph, QGraphicItem, or other custom classes)
'''

class LineItem(Styleable, QGraphicsLineItem):
  def __init__(self, x1, y1, x2, y2):
    QGraphicsLineItem.__init__(self, x1, y1, x2, y2)
    self.setStylingDocumentElementType("Line")
  

class TextItem(Styleable, QGraphicsTextItem):
  def __init__(self, text):
    QGraphicsTextItem.__init__(self, text)
    self.setStylingDocumentElementType("Text")
    
  
class EllipseItem(Styleable, QGraphicsEllipseItem):
  def __init__(self):
    QGraphicsEllipseItem.__init__(self)
    self.setRect(30, 30, 40, 40)
    self.setStylingDocumentElementType("Shape")
    
  
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
    
    self.addItem(TextItem("RMB to style item, a or d key to edit stylesheets"))
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
    for item in self.items():
      item.polish()
    
  
    
   
class GraphicsView(QGraphicsView):
  def __init__(self, scene):
    super(GraphicsView, self).__init__(scene)
    
    assert self.dragMode() is QGraphicsView.NoDrag
    
    self.setRenderHint(QPainter.Antialiasing)
    self.setRenderHint(QPainter.TextAntialiasing)
    self.scene = scene
    
  
  
  def keyPressEvent(self, event):
    # Let user edit a StyleSheet
    # TODO user and morph stylesheets
    key = event.key()
    if key == Qt.Key_A:
      QCoreApplication.instance().appStyleSheet.edit()
    elif key == Qt.Key_D:
      QCoreApplication.instance().docStyleSheet.edit()
    
    #self.morphStyleSheet.edit()

       
class MainWindow(QMainWindow):
  def __init__(self, *args):
    QMainWindow.__init__(self, *args)
    
  def newDocument(self):
    ''' Widget for new document (scene). '''
    self.scene = DiagramScene()
    self.view = GraphicsView(self.scene)
    self.setCentralWidget(self.view)
    return self.view
    
        
class App(QApplication):
  
  def __init__(self, args):
    super(App, self).__init__(args)
    self._createStyleSheets()  # Must precede window
    mainWindow = MainWindow()
    self.documentView = mainWindow.newDocument()
    mainWindow.setGeometry(100, 100, 500, 400)
    mainWindow.show()
    self.mainWindow = mainWindow
    self.docStyleSheet.styleSheetChanged.connect(mainWindow.scene.polish)
    self.exec_()
    
    
    
  
  def _createStyleSheets(self):
    ''' 
    Create inheriting sequence of stylesheets.
    Ordering is important.
    '''
    # !!! styleSheet() also a method of Qt QGV
    
    # Root (default) stylesheet
    self.appStyleSheet = AppStyleSheet() 
    # Serialized to user preferences, identical between sessions with different docs
    self.userStyleSheet = IntermediateStyleSheet(parent=self.appStyleSheet, name="User")
    # Serialized, attached to document.
    self.docStyleSheet = IntermediateStyleSheet(parent=self.userStyleSheet, name="Doc")
    # DocumentElementStyleSheets are created and owned by DocumentElements



app = App(sys.argv)

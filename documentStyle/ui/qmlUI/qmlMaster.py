'''
Object with methods (utilities) dealing with QML.

Hides details but also more robust than Qt methods.

Note findChild was broken until recently, see PyQt mail list report.
result = qmlRoot.findChild(model.person.Person, "person")
'''
from PyQt5.QtCore import qWarning, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtQuick import QQuickItem, QQuickView
from PyQt5.QtQml import QQmlProperty

#from documentStyle.qmlResources import styleResourceManager
from qtEmbeddedQmlFramework.resourceManager import resourceMgr


class QmlMaster(object):
  
  def quickViewRoot(self, quickview):
    '''
    QQuickView is a QWindow having a tree of QML objects.
    Root of the tree.
    '''
    assert isinstance(quickview, QQuickView)
    try:
      qmlRoot = quickview.rootObject()  # objects()[0]
    except:
      qWarning("quickview empty: failed to read or parse qml?")
      raise
    
    #print(qmlRoot)
    assert isinstance(qmlRoot, QQuickItem)
    return qmlRoot

  
  def findComponent(self, quickview, className, objectName):
      '''
      In quickview, find child with class className and objectName equal to objectName.
      '''
      root = self.quickViewRoot(quickview)
      return self.findComponentFromRoot(root, className, objectName)
  
  
  def findComponentFromRoot(self, root, className, objectName):
      '''
      In tree at root, find child with class className and objectName equal to objectName.
      '''
      result = None
      
      children = root.findChildren(QObject)
      for item in children:
        # Note the QML id property is NOT the objectName
        if isinstance(item, className) and item.objectName()==objectName:
          print("Found object of class", className, objectName)
          result = item
          break
      if result is None:
        print("Failed to find component named:", objectName)
      return result
  
  
  '''
  Find without searching.  Broken by bug in PyQt, reported and since fixed.
  '''
  def findComponent2(self, aType, name):
    assert isinstance(name, str)
    result = self.getWindow().findChild(aType, name)
    #result = self.getWindow().findChild(QObject, name)

    if result is None:
      print("Failed to find instance named:", name, " of type:", aType)
      raise RuntimeError
    assert result is None or isinstance(result, QQuickItem)
    return result
    
    
  def dumpQMLComponents(self, root):
    children = root.findChildren(QObject)
    for item in children:
      # Note the QML id property is NOT the objectName
      print(item, "name is:", item.objectName() )
      try:
        '''
        Apparently you can't just access item's properties: item.id
        Also, the id property apparently is not accessible via QQmlProperty.
        '''
        foo = QQmlProperty.read(item, "shoeSize")
        print("shoeSize property:", foo)
      except AttributeError:
        pass
      #if isinstance(item, model.person.Person):
      #  print("Is Person")
    
    
  def createQuickView(self, transientParent=None):
    '''
    Create empty QQuickView.
    More robust: connects to error.
    Subsequently, you should set context and then setSource()
    '''
    result = QQuickView()
    result.statusChanged.connect(self.onStatusChanged)
    if transientParent is not None:
      print("transientParent is:", transientParent, transientParent.isTopLevel())
      result.setTransientParent(transientParent)
    assert result is not None
    assert isinstance(result, QQuickView)
    return result
  
    
  def setSourceOnQuickView(self, view, qmlSubpath):
    print("setSourceOnQuickView to subpath: ", qmlSubpath)
    
    qurl = resourceMgr.urlToQMLResource(resourceSubpath=qmlSubpath)
    view.setSource(qurl)
    print("setSource on quickview to:", qurl.path())
    
    
  def quickViewForQML(self, qmlSubpath, transientParent=None):
    '''
    Create a QQuickView for qmlFilename.
    More robust: connects to error
    
    !!! Don't use this if the QML depends on names defined with setContextProperty()
    '''
    quickView = self.createQuickView(transientParent)
    self.setSourceOnQuickView(quickView, qmlSubpath=qmlSubpath)
    '''
    Show() the enclosing QWindow?
    But this means the window for e.g. the toolbar is visible separately?
    '''
    #quickView.show()
    
    return quickView
  
  
  def widgetAndQuickViewForQML(self, qmlFilename, transientParent=None):
    '''
    widget containing quickview, and quickview itself.
    See QTBUG-32934, you can't find the QWindow from the container QWidget, you must remember it.
    '''
    quickview = self.quickViewForQML(qmlFilename, transientParent)
    widget = self.wrapWidgetAroundQuickView(quickview, parentWindow=transientParent)
    return widget, quickview
  
  
  def widgetForQML(self, qmlFilename, parentWindow):
    ''' 
    Put QML in QQuickView and wrap in QWidget window. 
    
    I found that if you don't parent the widget,
    you get strange behaviour such as QML Dialog not visible when you open() it.
    '''
    quickview = self.quickViewForQML(qmlFilename)
    result = self.wrapWidgetAroundQuickView(quickview, parentWindow)
    return result
  
  
  def wrapWidgetAroundQuickView(self, quickview, parentWindow):
    '''
    Create QWidget window wrapping given quickview.
    Widget is parented by not positioned.
    QQuickView is empty of QML.
    '''
    assert parentWindow is not None
    result = QWidget.createWindowContainer(quickview, parent=parentWindow)
    assert isinstance(result, QWidget)
    print("Position of widgetForQML", str(result.pos()), result.pos().x(), result.pos().y())
    result.move(200,200)
    print("Position of widgetForQML", str(result.pos()), result.pos().x(), result.pos().y())
    return result
  
  
  def appQWindow(self):
    '''
    QWindow of app, or None.
    
    Needed to transientParent a QQuickView to app QWindow.
    '''
    qwinList = QGuiApplication.topLevelWindows()
    #print("window count", len(qwinList))
    #print(qwinList[0])
    if len(qwinList)==1:
      result = qwinList[0]
    else:
      print("Fail to find single QWindow for app.")
      result = None
    return result
    
    
    
  def onStatusChanged(self, status):
    " Handler for signal from QQuickView. "
    print("status changed", status)
    # TODO look for errors
    
"""
An experiment to use QQuickWidget.
It hangs at setSource
Dec. 8, 2014
 
  def createDialog(self, parentWindow, prefix, formation):
    '''
    Create QML based dialog.
    
    This implementation uses QQuickWidget
    '''
    qmlFilename="resources/qml/styleSheets/"+prefix+"stylesheet.qml"  # e.g. Userstylesheet.qml
    
    qmlMaster = QmlMaster()
    
    '''
    Order is important: create quickView, setContext, setSource, findComponent
    setContext defines names referred to in the source
    findComponent looks for names defined by the source.
    
    Note each .qml file has a DialogDelegate, all with same objectName "dialogDelegate" but separate instances.
    '''
    self.qw = QQuickWidget(parent=parentWindow)
    self.exposeFormationModelToQML(view=self.qw, editedFormation=formation, prefix=prefix)
    self.qw.statusChanged.connect(self.onStatusChanged)
    self.qw.sceneGraphError.connect(self.onSceneGraphError)
    print("before set source")
    self.qw.setSource(QUrl.fromLocalFile(qmlFilename))
    #self.qw.setSource(qmlMaster.qmlFilenameToQUrl(qmlFilename))
    print("after set source")
    self.dialogDelegate = qmlMaster.findComponent(quickview=self.qw, 
                                                  className=QmlDelegate, 
                                                  objectName="dialogDelegate")
    assert self.dialogDelegate is not None
    self.qw.show()
  
  def onStatusChanged(self, status):
    print("status changed", status)

  def onSceneGraphError(self, error, message):
    print("scene graph error", error, message)
"""
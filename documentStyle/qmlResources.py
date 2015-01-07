

from PyQt5.QtCore import QFileInfo


class StyleResourceManager():
  '''
  Know path to qml resources.
  '''
  
  def setStyleQmlResourceRoot(self):
    '''
    Assert self's file is at same level in directory structure as resources directory.
    E.G. self is at       documentStyle/qmlResources.py
    and resources are at documentStyle/resources
    Thus self.root becomes 'documentStyle/', i.e. the name of this submodule.
    
    Or if pyqtdeployed, self is an executable somewhere on target device file system,
    and Qt (using its rcc mechanism) find resources in the excecutable's compiled resources on that path.
    '''
    self.root = QFileInfo(__file__).absolutePath()
  
  
  def styleQmlPath(self):
    
    return self.root + '/resources/qml/style/'

styleResourceManager = StyleResourceManager()
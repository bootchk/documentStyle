

class StyleResourceManager():
  '''
  Know path to qml resources.
  '''
  
  def setStyleQmlResourceRoot(self, resourceRoot):
    '''
    Assert resourceRoot is a directory containing subdirectory resources/qml/style containing this projects .qml files.
    
    Typically the app using this subsystem passes
    the result of 'QFileInfo(__file__).absolutePath()' called in its main .py file.
    
    If pyqtdeployed, main is an executable somewhere on target device file system,
    and Qt (using its rcc mechanism) findd resources in the executable's compiled resources on that path.
    '''
    self.root = resourceRoot
    
  
  
  def styleQmlPath(self):
    
    return self.root + '/resources/qml/style/'

styleResourceManager = StyleResourceManager()
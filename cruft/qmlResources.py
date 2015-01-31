
from PyQt5.QtCore import QUrl



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
    self._root = resourceRoot
    
  
  
  def styleQmlPath(self):
    return self._root + '/resources/qml/style/'
  
  
  def styleQmlSubpath(self):
    '''
    subpath to qml resources.
    Must prefix with a root and suffix with more path.
    '''
    return '/resources/qml/style/'
  
  
  def qmlFilenameToQUrl(self, qmlSubpath):
    
    root_url = 'qrc:' if self._root.startswith(':') else self._root
    print("root_url: ", root_url)
    #url = QUrl(root_url + '/' + self._appPackageName + qmlSubpath)
    url = QUrl(root_url + qmlSubpath)
    
    print("urlToQMLResource", url)
    assert url.isValid()
    #print(url.path())
    #assert url.isLocalFile()
    return url


styleResourceManager = StyleResourceManager()
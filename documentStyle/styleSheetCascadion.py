'''
'''
import cPickle

from PySide.QtCore import QSettings

from documentStyle.styleSheet.appStyleSheet import AppStyleSheet
from documentStyle.styleSheet.intermediateStyleSheet import IntermediateStyleSheet


class StyleSheetCascadion(object):
  '''
  Conventional cascading set of style sheets: app, user, doc.
  Cascadion is noun, cascade is verb.
  
  Methods are exported to app (a document editing app.)
  '''

  def __init__(self):
    '''
    Create cascading sequence of stylesheets.
    Ordering is important.
    '''
    # !!! styleSheet() also a method of Qt QGV
    
    # Root (default) stylesheet
    self.appStyleSheet = AppStyleSheet() 
    
    # Serialized to user preferences, identical between sessions with different docs
    savedUserStyleSheet = self._getUserStylesheetFromSettings()
    if savedUserStyleSheet is None:
      self.userStyleSheet = IntermediateStyleSheet(name="User")
    else:
      self.userStyleSheet = savedUserStyleSheet
    self.userStyleSheet.setParent(self.appStyleSheet)
    
    '''
    A DocStyleSheet is usually serialized, attached to document.
    Here, create cascade with default DocStyleSheet (with empty StylingActSetCollection)
    Don't assume that a document and its stylesheet exists when cascadion is created.
    If it does exists, caller should call restoreDocStyleSheet
    '''
    self.docStyleSheet = IntermediateStyleSheet(name="Doc")
    self.docStyleSheet.setParent(self.userStyleSheet)
    
    # DocumentElementStyleSheets are created and owned by DocumentElements
    # and are parented automatically (in init()) to docStyleSheet
    
    
    
    
  def connectSignals(self, handler):
    '''
    Arrange signals so when any stylesheet changes, call handler (that polishes all document elements.)
    
    appStyleSheet is not user changeable.
    
    FUTURE: Optimize by choosing stylesheet to start cascade?
    '''
    self.userStyleSheet.styleSheetChanged.connect(handler)
    self.docStyleSheet.styleSheetChanged.connect(handler)
    
  
  def saveUserStylesheetAsSettings(self):
    settings = QSettings()
    pickledUserStyleSheet = cPickle.dumps(self.userStyleSheet, cPickle.HIGHEST_PROTOCOL)
    settings.setValue("UserStyleSheet", pickledUserStyleSheet)
    
    
  def _getUserStylesheetFromSettings(self):
    " Private, called at init. "
    print "UserStyleSheetFromSettings"
    settings = QSettings()
    styleSheetPickledInSettings = settings.value("UserStyleSheet")
    if styleSheetPickledInSettings is not None:
      # convert unicode to str
      print styleSheetPickledInSettings
      return cPickle.loads(str(styleSheetPickledInSettings))
    else:
      return None
    # Assert caller will link stylesheet into cascade and restyle document
      

  def pickleDocStyleSheet(self):
    return cPickle.dumps(self.docStyleSheet, cPickle.HIGHEST_PROTOCOL)
    
    
  def restoreDocStyleSheet(self, pickle):
    self.docStyleSheet = cPickle.loads(pickle)
    
    # Restore cascade of styleSheets, i.e. insert into linked tree.
    self.docStyleSheet.setParent(self.userStyleSheet)
    
    # Assert caller will reparent documentElements and restyle (polish) document
    # signal styleSheetChanged is NOT emitted on setParent()

  
    
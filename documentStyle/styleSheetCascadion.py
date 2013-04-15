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
    self.userStyleSheet = IntermediateStyleSheet(parent=self.appStyleSheet, name="User")
    
    # Serialized, attached to document.
    self.docStyleSheet = IntermediateStyleSheet(parent=self.userStyleSheet, name="Doc")
    
    # DocumentElementStyleSheets are created and owned by DocumentElements
    self._restoreUserStylesheetFromSettings()
    
    
    
  def connectSignals(self, handler):
    '''
    Arrange signals so when any stylesheet changes, call handler (that polishes all document elements.)
    
    appStyleSheet is not user changeable.
    
    FUTURE: Optimize by choosing stylesheet to start cascade?
    '''
    self.userStyleSheet.styleSheetChanged.connect(handler)
    self.docStyleSheet.styleSheetChanged.connect(handler)
    
    # Initial cascaded styling of document
    handler()
    
  
  def saveUserStylesheetAsSettings(self):
    " Exported to app "
    settings = QSettings()
    pickledUserStyleSheet = cPickle.dumps(self.userStyleSheet.getSerializable())
    settings.setValue("UserStyleSheet", pickledUserStyleSheet)
    
    
  def _restoreUserStylesheetFromSettings(self):
    " Private, called at init. "
    print "UserStyleSheetFromSettings"
    settings = QSettings()
    settingStyleSheet = settings.value("UserStyleSheet")
    if settingStyleSheet is not None:
      # use pickle to restore type (class)
      serializable = cPickle.loads(str(settingStyleSheet))
      self.userStyleSheet.resetFromSerializable(serializable)


  def pickleDocStyleSheet(self):
    print "Saved document style sheet"
    serializableDSS = self.docStyleSheet.getSerializable()
    self.pickledDSS = cPickle.dumps(serializableDSS)
    
    
  def restoreDocStyleSheet(self):
    print "Restored document style sheet"
    unpickledDSS = cPickle.loads(self.pickledDSS)
    self.docStyleSheet.resetFromSerializable(unpickledDSS)
  
  
    
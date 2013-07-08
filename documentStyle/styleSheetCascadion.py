'''
'''
import cPickle

from PySide.QtCore import QSettings, Qt

from documentStyle.styleSheet.appStyleSheet import AppStyleSheet
from documentStyle.styleSheet.intermediateStyleSheet import IntermediateStyleSheet
from documentStyle.debugDecorator import report


class StyleSheetCascadion(object):
  '''
  Conventional cascading set of style sheets: app, user, doc.
  Cascadion is noun, cascade is verb.
  
  Methods are exported to app (a document editing app.)
  
  Responsibilities:
  - initialize a default cascade prefix: [app, user, doc] (less documentElementSS suffix)
  - save and restore UserStyleSheet as settings
  - serialize and deserialize DocumentStyleSheet
  - insert new DocumentStyleSheet into cascade (and signal change)
  - know what part of cascade may change (be able to connect signals)
  '''

  def __init__(self):
    '''
    Create cascading sequence of stylesheets.
    Ordering is important.
    !!! Getting userStyleSheet from setting is built-in, but some apps may not want this.
    '''
    # !!! styleSheet() also a method of Qt QGV
    
    # Root (default) stylesheet
    self.appStyleSheet = AppStyleSheet() 
    
    # Serialized to user preferences, identical between sessions with different docs
    savedUserStyleSheet = self._getUserStylesheetFromSettings()
    if savedUserStyleSheet is None:
      # Default userStyleSheet (empty of styling acts.)
      self.userStyleSheet = IntermediateStyleSheet(name="User")
    else:
      self.userStyleSheet = savedUserStyleSheet
    self.userStyleSheet.setParent(self.appStyleSheet)
    
    '''
    A DocStyleSheet is usually serialized, attached to document.
    Here, create cascade with default DocStyleSheet (with empty StylingActSetCollection)
    Don't assume that a document and its stylesheet exists when cascadion is created.
    If not-trivial DocStyleSheet does exist, caller should call restoreDocStyleSheet
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
    # !!! Queued so that they are handled in event loop AFTER any other changes to doc structure or style
    self.userStyleSheet.styleSheetChanged.connect(handler, Qt.QueuedConnection)
    self.docStyleSheet.styleSheetChanged.connect(handler, Qt.QueuedConnection)
    # Remember my parent's handler
    self.parentHandler = handler
    
  
  def saveUserStylesheetAsSettings(self):
    settings = QSettings()
    '''
    This does not work, yields "invalid load key" on unpickling:
    pickledUserStyleSheet = cPickle.dumps(self.userStyleSheet, cPickle.HIGHEST_PROTOCOL)
    Attempting: settings.setIniCodec('UTF-8') does not help the problem.
    So we use the default protocol.
    '''
    pickledUserStyleSheet = cPickle.dumps(self.userStyleSheet)
    settings.setValue("UserStyleSheet", pickledUserStyleSheet)
    
    
  def _getUserStylesheetFromSettings(self):
    " Private, called at init. "
    print "UserStyleSheetFromSettings"
    settings = QSettings()
    
    styleSheetPickledInSettings = settings.value("UserStyleSheet")
    print "Type unpickled", type(styleSheetPickledInSettings)
    if styleSheetPickledInSettings is not None:
      # convert unicode to str
      # print "Pickled stylesheet in settings: ", styleSheetPickledInSettings
      return cPickle.loads(str(styleSheetPickledInSettings))
    else:
      return None
    # Assert caller will link stylesheet into cascade and restyle document
      

  def pickleDocStyleSheet(self):
    return cPickle.dumps(self.docStyleSheet, cPickle.HIGHEST_PROTOCOL)
    
    
  def restoreDocStyleSheet(self, pickle):
    ''' set DocStyleSheet from a pickle. '''
    newDocStyleSheet = cPickle.loads(pickle)
    self.setDocStyleSheet(newDocStyleSheet)
    
    
    
  @report
  def setDocStyleSheet(self, newDocStyleSheet):
    '''
    Insert newDocStyleSheet into cascade, i.e. insert into linked tree.
    
    Old DocStyleSheet usually garbage collected.
    Callers should not save references to DocStyleSheet.
    
    This encapsulates that changing DocStyleSheet requires signal.
    (No caller should directly write self.docStyleSheet.)

    '''
    self.docStyleSheet = newDocStyleSheet
    self.docStyleSheet.setParent(self.userStyleSheet)
    
    # !!! Connect newDocStyleSheet signals (signals are from instances, old instance connections are lost.)
    self.docStyleSheet.styleSheetChanged.connect(self.parentHandler, Qt.QueuedConnection)
    
    '''
    signal styleSheetChanged is NOT emitted on setParent() (but maybe it should be, since cascade changes?)
    Instead, emit signal now.
    New stylesheet might not be substantively different from old, but assume it is.
    '''
    self.docStyleSheet.styleSheetChanged.emit()
    # Assert caller will reparent documentElements  (before signal handled in event loop by polish() )
    

  
    
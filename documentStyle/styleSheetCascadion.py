

import pickle

from PyQt5.QtCore import QSettings, Qt

from documentStyle.styleSheet.appStyleSheet import AppStyleSheet
from documentStyle.styleSheet.intermediateStyleSheet import IntermediateStyleSheet

from documentStyle.model.brush import AdaptedBrushModel
from documentStyle.model.pen import AdaptedPenModel
from documentStyle.model.lineSpacing import AdaptedLineSpacingModel
from documentStyle.model.textalignment import AdaptedAlignmentModel

import documentStyle.config as config
from documentStyle.debugDecorator import report

from documentStyle.qmlUI.qmlModel import QmlModel

from . import compat




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
    
    '''
    # !!! styleSheet() also a method of Qt QGV
    
    # assert translator installed
    # create singletons requiring translation
    config.i18ns = config.Translations()
    
    self._initModels()  # Needed by GUI
    self._initStyleSheets()
    " assert cascade of stylesheets exists, but not prepared for GUI edit. "
    
    
    
  def _initStyleSheets(self):
    '''
    Create cascade of stylesheets.
    Order is important.
    !!! Getting userStyleSheet from setting is built-in, but some apps may not want this.
    '''
    # Root (default) stylesheet
    self.appStyleSheet = AppStyleSheet() 
    
    # Serialized to user preferences, identical between sessions with different docs
    savedUserStyleSheet = self._getUserStylesheetFromSettings()
    if savedUserStyleSheet is None:
      # Default userStyleSheet (empty of styling acts.)
      self.userStyleSheet = IntermediateStyleSheet(name='User')
    else:
      print("UserStyleSheet restored from settings")
      self.userStyleSheet = savedUserStyleSheet
    self.userStyleSheet.setParent(self.appStyleSheet)
    
    '''
    A DocStyleSheet is usually serialized, attached to document.
    Here, create cascade with default DocStyleSheet (with empty StylingActSetCollection)
    Don't assume that a document and its stylesheet exists when cascadion is created.
    If not-trivial DocStyleSheet does exist, caller should call restoreDocStyleSheet
    '''
    self.docStyleSheet = IntermediateStyleSheet(name='Doc')
    self.docStyleSheet.setParent(self.userStyleSheet)
    
    '''
    DocumentElementStyleSheets are created and owned by DocumentElements
    and are parented automatically (in init()) to docStyleSheet.
    GUI is created on the fly?
    
    Tool stylesheets are created and owned by Tools.
    GUI created on the fly?
    
    TODO Optimization: only create GUI's once.
    '''
  
  
  def preGui(self, parentWindow):
    '''
    Prepare for editing stylesheets.
    
    For QWidgets, formerly these were created on the fly.
    '''
    print("preGui called")
    if config.useQML:
      " Register dialog delegates. "
      model = QmlModel()
      model.register()
      
    '''
    Not calling _createEditors now.
    Editors are created as needed (when edit() is called.)
    '''
  
  def _createEditors(self, parentWindow):
    '''
    Create editors in a batch, ahead of user request.
    Omit App stylesheet GUI, not important to users
    '''
    #self.appStyleSheet.createGui(parentWindow)
    self.userStyleSheet.createGui(parentWindow)
    self.docStyleSheet.createGui(parentWindow)
  
  
  def _initModels(self):
    " Create domain models. Needed by QWidget GUI, not QML. "
    # Temp always.
    # if not config.useQML:
    config.BrushModel = AdaptedBrushModel()
    config.PenModel = AdaptedPenModel()
    config.LineSpacingModel = AdaptedLineSpacingModel()
    config.AlignmentModel = AdaptedAlignmentModel()
    
    
    
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
    '''
    User stylesheet is a setting (doc stylesheet is not.)
    '''
    settings = QSettings()
    '''
    This does not work, yields 'invalid load key' on unpickling:
    pickledUserStyleSheet = piclle.dumps(self.userStyleSheet, pickle.HIGHEST_PROTOCOL)
    Attempting: settings.setIniCodec('UTF-8') does not help the problem.
    So we use the default protocol.
    '''
    pickledUserStyleSheet = pickle.dumps(self.userStyleSheet)
    settings.setValue('UserStyleSheet', pickledUserStyleSheet)
    
    
  def _getUserStylesheetFromSettings(self):
    ' Private, called at init. '
    #print 'UserStyleSheetFromSettings'
    settings = QSettings()
    
    styleSheetPickledInSettings = settings.value('UserStyleSheet')
    
    if styleSheetPickledInSettings is not None:
      if compat.PY2:
        assert styleSheetPickledInSettings is None or isinstance(styleSheetPickledInSettings, unicode)
        return pickle.loads(str(styleSheetPickledInSettings))
      else:
        assert styleSheetPickledInSettings is None or isinstance(styleSheetPickledInSettings, bytes)
        return pickle.loads(styleSheetPickledInSettings)
    else:
      return None
    # Assert caller will link stylesheet into cascade and restyle document
      

  def pickleDocStyleSheet(self):
    return pickle.dumps(self.docStyleSheet, pickle.HIGHEST_PROTOCOL)
    
    
  def restoreDocStyleSheet(self, pickledStylesheet):
    '''
    set DocStyleSheet from a pickledStylesheet. 
    !!! Caller must restore downstream styleables and toolStylers to cascadion.
    '''
    newDocStyleSheet = pickle.loads(pickledStylesheet)
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
    del(self.docStyleSheet) # !!! Old references to it are stale.
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
    

  
    
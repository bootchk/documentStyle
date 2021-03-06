'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

import pickle

from PyQt5.QtCore import QSettings

from .dynamicStyler import DynamicStyler
from documentStyle.selector import DETypeSelector



class ToolStyler(DynamicStyler):
  '''
  Dynamic: cascades.
  User editing of DocumentStyleSheet changes set of DocumentElements that have not been individually styled.
  
  Note this is pickleable since attributes are pickleable.
  !!! Assert a deserialized self does NOT have _styleSheet parented; must call addToStyleCascade()
  '''
  
  def __init__(self, DEType, toolName):
    assert isinstance(DEType, str)  # Type of style for element e.g. 'Line'
    selector = DETypeSelector(DEType)
    super(ToolStyler, self).__init__(selector)
    self.toolName = toolName  # Type of elementTool e.g. 'Freehand Tool'
    # ensure self is in style cascade (DESS() ensures it.)
    
  
  def edit(self, parentWindow):
    ''' 
    Let user edit style of tool that creates DocumentElement.
    Return Style, or None if canceled.
    '''
    print("Calling editStyleofDocElement with toolname:", self.toolName)
    self.editStyleOfDocElement(parentWindow = parentWindow,
                              titleParts=(self.toolName, "Style"),  # WAS "Tool Style".  "Tool" migrated to toolname.
                              docElement=self)
    '''
    Execution continues.
    see self.accept()
    '''
  
  def accept(self):
    '''
    User accepted dialog.
    Result is in self.editedFormation.
    Apply it to tool that was passed to this editing session.
    Update self's styleSheet.  Doesn't affect any document elements now.
    '''
    # assert isinstance(self._editedDocElement, Styleable)
    self.styleLeafFromFormation(formation=self.editedFormation)
    
    

  def applyTo(self, documentElement):
    '''
    Apply tool style to documentElement.
    
    Assert documentElement has-a styler.
    '''
    #print('foo', documentElement.styler._styleSheet)
    #documentElement.styler._styleSheet._dump()
    # Stamp documentElement's styler from my stylesheet i.e. change model
    documentElement.styler.styleLeafFromStyleSheet(self.styleSheet())
    
    # Now documentElement.styler.stylesheet has styling acts the same as self
    # TODO assertions that check that new styling acts were added.
    
    # Change view i.e. visuals
    documentElement.polish()  # Cascade again, through updated styling acts.
    
    '''
    OLD, BAD DESIGN:
    Why does it fail to work as expected?  If self formation is cascaded,
    why isn't this enough to style the document element?
    Maybe the above is not successfully adding styling acts.
    
    # Essentially documentElement.polish(), but more efficient (forego another cascade.)
    style.applyTo(documentElement)
    '''
    
  
  def saveAsSetting(self):
    settings = QSettings()
    '''
    This does not work, yields "invalid load key" on unpickling:
    pickledUserStyleSheet = pickle.dumps(self.userStyleSheet, pickle.HIGHEST_PROTOCOL)
    Attempting: settings.setIniCodec('UTF-8') does not help the problem.
    So we use the default protocol.
    '''
    pickledToolStyler = pickle.dumps(self)
    settings.setValue(ToolStyler._settingsNameForTool(self.toolName), pickledToolStyler)

  @classmethod
  def _settingsNameForTool(cls, toolName):
    assert isinstance(toolName, str)
    return toolName + "ToolStyle"
  
  
  @classmethod
  def getToolStylerFromSettings(cls, toolName):
    " Private, called at init. "
    toolStylerPickledInSettings = QSettings().value(cls._settingsNameForTool(toolName))
    
    if toolStylerPickledInSettings is not None:
      """
      ## P2 type of toolStylerPickledInSettings is unicode, P3 type is bytes.  Don't know a clean way to handle both
      if not PY2:
        isinstance(toolStylerPickledInSettings, bytes)
        result = pickle.loads(toolStylerPickledInSettings)
      else:
        result = pickle.loads(str(toolStylerPickledInSettings))
      """
      assert isinstance(toolStylerPickledInSettings, bytes)
      result = pickle.loads(toolStylerPickledInSettings)
      result.addToStyleCascade()
    else:
      result = None
    assert result is None or result.isInCascadion() # parented to DocumentStyleSheet
    return result
    
  
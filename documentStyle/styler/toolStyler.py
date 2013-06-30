'''
Copyright 2013 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from dynamicStyler import DynamicStyler
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
    self.toolName = toolName  # Type of element e.g. 'Freehand'
    # ensure self is in style cascade (DESS() ensures it.)
    
  
  def edit(self):
    ''' 
    Let user edit style of tool that creates DocumentElement.
    Return Style, or None if canceled.
    '''
    newStyle = self.getEditedStyle(dialogTitle=self.toolName + "Tool Style")
    if newStyle is None:
      # canceled, self's styleSheet unchanged
      return 
    else:
      # update self's styleSheet, but doesn't affect any document elements now
      self.setFormation(newStyle)
    
    

  def applyTo(self, documentElement):
    '''
    Apply tool style to documentElement.
    
    Assert documentElement has-a styler.
    '''
    # Stamp documentElement's stylesheet with my stylesheet
    # i.e. change model
    style = self.formation()
    documentElement.styler.setFormation(style)
    
    # Change view i.e. visuals
    # Essentially documentElement.polish(), but more efficient (forego another cascade.)
    style.applyTo(documentElement)
    
    
    
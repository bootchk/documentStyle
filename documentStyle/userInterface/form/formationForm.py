'''

'''

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLabel, QFormLayout

# circular from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation


class FormationForm(QFormLayout):
  '''
  A form with tree-like, indented, spanning labels.
  A form is two columns: (label, control),
  having label right aligned and control left-aligned.
  Thus there is a center line, but left and right edges are jagged.
  IOW the Apple/Mac/OSX style for forms.
  See QFormLayout.
      
      Title
      
  name1  (QLabel)
    widgetGroup  (group of control)
  name2:subname1
    widgetGroup
  name2:subname2
    widgetGroup
  
  Recursive !!
  Collaborates with Formation.
  '''


  def __init__(self, formation, top):
    
    super(FormationForm, self).__init__()
    
    # Emulate Mac style
    self.setRowWrapPolicy(QFormLayout.DontWrapRows)
    self.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
    self.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
    self.setLabelAlignment(Qt.AlignRight)
    
    self.addFormationToForm(formation, labelPrefix="", top=top)
  
  
  def addFormationToForm(self, formation, labelPrefix, top):
    assert isinstance(labelPrefix, str)
    
    '''
    Selector tells how to label:  don't use labelPrefix.
    '''
    #print " add formation", formation.name, top, formation.selector
    if top == True:
      pass  # name is in window title
    else:
      self.addFormationLabelToForm(formation)
    
    if len(formation) > 0:  # recursion termination
      for subformation in formation:
        # Recurse
        self.addFormationToForm(subformation, labelPrefix="not used", top=False)
    else: # No child formations
      self.addStylePropertiesToForm(formation, labelPrefix)
        
        
  def addStylePropertiesToForm(self, formation, labelPrefix):
    #assert isinstance(formation, InstrumentFormation)
    
    for styleProperty in formation.generateStyleProperties():
      #print "sp"
      layout = styleProperty.getLayout(isLabeled=False)
      """
      if formation.isSingleValued():
        # Only a single property, label with selector
        label = labelPrefix + ":" + layout.getLabel()
        self.addRow(label, layout.getWidget())
      else:
        # more than one, label each with just label of style property
        self.addRow(layout.getLabel(), layout.getWidget())
      """
      # Indent all style properties
      label = "   " + layout.getLabel()
      self.addRow(label, layout)
    
      
  def addFormationLabelToForm(self, formation):
    ''' 
    Add a QLabel to form, spanning columns, as a separator.
    Text equal to role cat name to form. 
    Return text.
    
    Note no special logic for single-property formations:
    they still yield a label separator.
    '''
    #print "add label"
    selector = formation.selector
    if selector.isAnyDETypeAndInstrumentSelector():
      text = "Any:" + formation.name
    elif selector.isDETypeSelector():
      text = formation.name
    elif selector.isDETypeAndInstrumentSelector():
      # e.g. Text:Frame Pen or Line:Pen
      # assert role is '' or role is 'Foo ' with trailing space
      text = selector.DEType + ":" + formation.role + formation.name
        
      
    label = QLabel(text)
    self.addRow(label)  # spans both columns
    return text
  
  

  
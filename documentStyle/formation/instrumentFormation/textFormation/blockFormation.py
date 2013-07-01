'''
'''

#from PySide.QtCore import Qt
from PySide.QtGui import QTextBlockFormat

from textFormation import TextFormation
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation
from documentStyle.formation.styleProperty import IntStyleProperty
#from documentStyle.formation.styleProperty import ComboBoxStyleProperty
#from documentStyle.userInterface.model.textalignment import AlignmentModel

class BlockFormation(TextFormation):
  '''
  Styling attributes of blocks.
  
  Specialize to Qt <QTextBlockFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Block", parentSelector=parentSelector)
    self.instrument = QTextBlockFormat()
    '''
    Note in Qt a doc has a global indentWidth having default of 40 pixels.
    This is the count of indents, more or less tabs.
    '''
    self.styleProperties=[IntStyleProperty("Indent", self.instrument.setIndent, self.instrument.indent, self.selector, 
                                           0, maximum=10, singleStep=1),
                          ]
    '''
                          ComboBoxStyleProperty("Alignment", 
                                                self.instrument.setAlignment, self.instrument.alignment, self.selector,
                                                minimum = Qt.AlignmentFlag.AlignLeft, # "Left",
                                                model = AlignmentModel),
                          ]
    
    Alignment property not working yet: it is a Boolean combination of flags, not handled by this code.
    Need a BooleanOfFlagsStyleProperty ???
                          ComboBoxStyleProperty("Alignment", 
                                                self.instrument.setAlignment, self.instrument.alignment, 
                                                model = Qt.AlignmentFlag),]
    '''
  
  
  def applyToCursor(self, cursor):
    cursor.mergeBlockFormat(self.instrument)

    

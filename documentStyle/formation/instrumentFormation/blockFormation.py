'''
'''

from PySide.QtGui import QTextBlockFormat
from textFormation import TextFormation
from instrumentFormation import InstrumentFormation
from ..styleProperty import IntStyleProperty

class BlockFormation(TextFormation):
  '''
  Styling attributes of blocks.
  
  Specialize to Qt <QTextBlockFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Block", parentSelector=parentSelector)
    self.base = QTextBlockFormat()
    self.styleProperties=[IntStyleProperty("Indent", self.base.setIndent, self.base.indent, self.selector(), 0, 10),]
    '''
    Alignment property not working yet: it is a Boolean combination of flags, not handled by this code.
    Need a BooleanOfFlagsStyleProperty ???
                          ComboBoxStyleProperty("Alignment", 
                                                self.base.setAlignment, self.base.alignment, 
                                                model = Qt.AlignmentFlag),]
    '''
  
  
  def applyToCursor(self, cursor):
    cursor.mergeBlockFormat(self.base)

    

'''
'''

from PySide.QtGui import QTextBlockFormat

from textFormation import TextFormation
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation
from documentStyle.formation.styleProperty import IntStyleProperty
from documentStyle.formation.styleProperty import ComboBoxStyleProperty
from documentStyle.formation.styleProperty import UnwrappedComboBoxStyleProperty
from documentStyle.model.textalignment import alignmentModel
from documentStyle.model.lineSpacing import lineSpacingModel
from documentStyle.styleWrapper.styleWrapper import AlignmentStyleWrapper


class BlockFormation(TextFormation):
  '''
  Styling attributes of blocks of text.
  
  Specialize to Qt <QTextBlockFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Block", parentSelector=parentSelector)
    self.instrument = QTextBlockFormat()
    '''
    Note in Qt a doc has a global indentWidth having default of 40 pixels.
    This is the count of indents, more or less tabs.
    '''
    self.styleProperties=[IntStyleProperty("Indent", self.instrument.setIndent, self.selector,
                                           default=self.instrument.indent(), 
                                           minimum=0, maximum=10, singleStep=1),
                          ComboBoxStyleProperty("Alignment", self.instrument.setAlignment, self.selector,
                                                default=AlignmentStyleWrapper(self.instrument.alignment()),
                                                model = alignmentModel),
                          UnwrappedComboBoxStyleProperty("Line spacing", self.adaptLineSpacing, self.selector,
                                                default=100,  # single spacing is default
                                                model = lineSpacingModel),
                          ]
  
  
  def applyToCursor(self, cursor):    
    cursor.mergeBlockFormat(self.instrument)

    
  def adaptLineSpacing(self, value):
    # Always lineHeightType=proportional, values always percent
    self.instrument.setLineHeight(value, QTextBlockFormat.ProportionalHeight)

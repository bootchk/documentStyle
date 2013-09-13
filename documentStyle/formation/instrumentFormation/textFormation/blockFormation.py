'''
'''

from PyQt4.QtGui import QTextBlockFormat

from textFormation import TextFormation
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation
from documentStyle.formation.styleProperty import IntStyleProperty
from documentStyle.formation.styleProperty import ComboBoxStyleProperty
from documentStyle.formation.styleProperty import UnwrappedComboBoxStyleProperty
from documentStyle.model.textalignment import alignmentModel
from documentStyle.model.lineSpacing import lineSpacingModel
#from documentStyle.styleWrapper.styleWrapper import AlignmentStyleWrapper

from documentStyle.debugDecorator import report, reportReturn


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
                                                # PySide default=AlignmentStyleWrapper(self.instrument.alignment()),
                                                default=self.instrument.alignment(),
                                                model = alignmentModel),
                          UnwrappedComboBoxStyleProperty("Line spacing", self.adaptLineSpacing, self.selector,
                                                default=100,  # single spacing is 100% is default
                                                model = lineSpacingModel),
                          ]
    '''
    !!! QTextBlockFormat.lineHeight() defaults to value 0 for 'single spacing.'  
    Need the following to set the default according to lineHeightType=proportional
    '''
    self.adaptLineSpacing(100)
  
  
  @report
  def applyToCursor(self, cursor):    
    cursor.setBlockFormat(self.instrument)
    # Strong: all fields same
    assert cursor.blockFormat() == self.instrument
    ## Weak: only the fields we futz with are same
    ##assert cursor.blockFormat().lineHeight() == self.instrument.lineHeight(), str(cursor.blockFormat().lineHeight()) +','+ str(self.instrument.lineHeight())
    ##assert cursor.blockFormat().indent() == self.instrument.indent(), str(cursor.blockFormat().indent()) +','+ str(self.instrument.indent())
    ##assert cursor.blockFormat().alignment() == self.instrument.alignment(), str(cursor.blockFormat().alignment()) +','+ str(self.instrument.alignment())
    
  @reportReturn
  def adaptLineSpacing(self, value):
    # Always lineHeightType=proportional, values always percent
    assert value > 0
    self.instrument.setLineHeight(value, QTextBlockFormat.ProportionalHeight)

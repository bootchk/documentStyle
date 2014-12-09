
from .textFormation import TextFormation
from documentStyle.instrument.blockInstrument import BlockInstrument
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation

from documentStyle.styleProperty.styleProperty import BaseStyleProperty
from documentStyle.userInterface.layout.typedStylePropertyLayout import ComboBoxStylePropertyLayout
#, UnwrappedComboBoxStylePropertyLayout
import documentStyle.config as config
#from documentStyle.styleWrapper.styleWrapper import AlignmentStyleWrapper

from documentStyle.debugDecorator import report

'''
i18n: no names are translated here.  Names here are internal names, always in English.  Translated before display.
'''


class BlockFormation(TextFormation):
  '''
  Styling attributes of blocks of text.
  
  Specialize to Qt <QTextBlockFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name='Block', parentSelector=parentSelector)
    self.instrument = BlockInstrument() # QTextBlockFormat()
    '''
    Note in Qt a doc has a global indentWidth having default of 40 pixels.
    This is the count of indents, more or less tabs.
    '''
    self.styleProperties=[# WAS 'Alignment'
                          BaseStyleProperty('Aligned', self.instrument.setAlignment, self.selector,
                                            default=self.instrument.defaultAligning,
                                            layoutFactory=ComboBoxStylePropertyLayout,
                                            domainModel = config.AlignmentModel),
                          # WAS 'Line spacing', too long
                          # TODO why was this UnwrappedComboBoxStyleProperty
                          BaseStyleProperty('Spacing', self.instrument.setSpacing, self.selector,
                                            default = self.instrument.defaultSpacing,
                                            layoutFactory=ComboBoxStylePropertyLayout,
                                            domainModel = config.LineSpacingModel),
                          ]
    """
    #Eliminated this because it is buggy: it doesn't seem to get properly layout by document.
    
    BaseStyleProperty('Indent', self.instrument.setIndent, self.selector,
                                           default=self.instrument.indent(),
                                           layoutFactory=IntStylePropertyLayout,
                                           minimum=0, maximum=10, singleStep=1),
    """
  
  
  @report
  def applyToCursor(self, cursor):    
    cursor.setBlockFormat(self.instrument)
    # Strong: all fields same
    assert cursor.blockFormat() == self.instrument
    ## Weak: only the fields we futz with are same
    ##assert cursor.blockFormat().lineHeight() == self.instrument.lineHeight(), str(cursor.blockFormat().lineHeight()) +','+ str(self.instrument.lineHeight())
    ##assert cursor.blockFormat().indent() == self.instrument.indent(), str(cursor.blockFormat().indent()) +','+ str(self.instrument.indent())
    ##assert cursor.blockFormat().alignment() == self.instrument.alignment(), str(cursor.blockFormat().alignment()) +','+ str(self.instrument.alignment())
    
  

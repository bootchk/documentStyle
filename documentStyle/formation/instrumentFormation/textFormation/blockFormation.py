
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextBlockFormat

from .textFormation import TextFormation
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation

from documentStyle.styleProperty.styleProperty import BaseStyleProperty
from documentStyle.userInterface.layout.typedStylePropertyLayout import ComboBoxStylePropertyLayout
#, UnwrappedComboBoxStylePropertyLayout
import documentStyle.config as config
#from documentStyle.styleWrapper.styleWrapper import AlignmentStyleWrapper

from documentStyle.debugDecorator import report, reportReturn

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
    self.instrument = QTextBlockFormat()
    '''
    Note in Qt a doc has a global indentWidth having default of 40 pixels.
    This is the count of indents, more or less tabs.
    '''
    self.styleProperties=[# WAS 'Alignment'
                          BaseStyleProperty('Aligned', self.adaptAlignment, self.selector,
                                            #self.instrument.setAlignment, 
                                              # PySide default=AlignmentStyleWrapper(self.instrument.alignment()),
                                              default=self.instrument.alignment(),
                                              layoutFactory=ComboBoxStylePropertyLayout,
                                              domainModel = config.AlignmentModel),
                          # WAS 'Line spacing', too long
                          # TODO why was this UnwrappedComboBoxStyleProperty
                          BaseStyleProperty('Spacing', self.adaptLineSpacing, self.selector,
                                                default=100,  # single spacing is 100% is default
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
    '''
    Adapt model to instrument setter, which takes two parameters.
    Always lineHeightType=proportional, values always percent e.g. 100, 150, 200
    '''
    assert value > 0
    self.instrument.setLineHeight(value, QTextBlockFormat.ProportionalHeight)
    
    
  @reportReturn
  def adaptAlignment(self, value):
    '''
    Convert int to Qt.Alignment type
    Solves problem in QML that I don't fully understand.
    Note below that Python doesn't care about the comparison types,
    but PyQt gives TypeError if use unadapted value of type int.
    
    Possibly we could also fix by defining ResettableAlignmentValue of type QtCore.Alignment ?
    '''
    assert value > 0, "Zero is not a proper flag."
    
    if value == Qt.AlignLeft:
      adaptedValue = Qt.AlignLeft
    elif value == Qt.AlignRight:
      adaptedValue = Qt.AlignRight
    elif value == Qt.AlignHCenter:  # !!!! Horizontal
      adaptedValue = Qt.AlignHCenter
    elif value == Qt.AlignJustify:
      adaptedValue = Qt.AlignJustify
    else:
      print("Unknown alignment value")
      adaptedValue = Qt.AlignLeft # defaults to some valid value
    print("adaptAlignment called", adaptedValue)
    self.instrument.setAlignment(adaptedValue)

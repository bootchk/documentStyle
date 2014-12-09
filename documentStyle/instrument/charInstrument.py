'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

'''
see instrument.py

Wrap a Qt Instrument.
'''
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat


class CharInstrument(QTextCharFormat):
  '''
  Contain character parameters (foreground color and font)
  
  Parameters of Qt instrument that we omit:
  - setBackgroundColor()  : color behind text
  - setTextOutline(QPen)  : pen to stroke char outline
  - brush.setStyle(Qt.SolidPattern) : brush to fill chars
  '''
  def __init__(self):
    super().__init__()
    # These should be the same as framework's default, from new instrument
    self.defaultColor = self.foregroundColor()
    self.defaultFont = self.font()
    
    self._adaptInitialInstrument()
    
    
  def _adaptInitialInstrument(self):
    '''
    Ensure instrument is initted with our defaults.
    '''
    pass  # Not necessary, we're not adapting values, only signatures
    

  '''
  ForegroundColor
  '''
  def setForegroundColor(self, value):
    '''
    Adapt signature and get around Qt inconsistencies.
    
    Qt has no direct setter for this property.
    Indirect: get brush, set color on brush, set brush.
    Get brush gets a copy of brush that must be reset onto the format.
    Just :get brush, set color on brush: has no effect.
    And self.instrument.foreground().setColor apparently justs sets color on a brush copy, not affecting text.
    
    At one time, applyToCursor was calling setForegroundColor() (and it was resetting brush.)
    '''
    brush = super().foreground()
    brush.setColor(value)
    brush.setStyle(Qt.SolidPattern) # HACK: doesn't allow brush pattern editable by user
    super().setForeground(brush)
    
    
  def foregroundColor(self):
    '''
    Adapt signature.
    No need to adapt model values (QColor)
    '''
    result = super().foreground().color()
    return result
  


  '''
  Font does not need adaption: setFont() and font() inherited from super.
  '''
  
    
    

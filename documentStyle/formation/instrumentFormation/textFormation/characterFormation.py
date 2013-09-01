'''
'''

from PySide.QtCore import Qt
from PySide.QtGui import QTextCharFormat
from textFormation import TextFormation
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation
from documentStyle.formation.styleProperty import ColorStyleProperty, FontStyleProperty
from documentStyle.styleWrapper.fontStyleWrapper import FontStyleWrapper



class CharacterFormation(TextFormation):
  '''
  Styling attributes of characters.
  
  Specialize to Qt <QTextCharFormat>
  
  Notes:
  Color property is foreground.
  We choose not to offer background color as a style property.
  Background color applied to text document gives jaggy blocks of color background.
  Probably better to offer a property on a background layer (symmetric balloon) behind the text. 
  Background color defaults to transparent.
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Character", parentSelector=parentSelector)
    self.instrument = QTextCharFormat()
    self.styleProperties=[ColorStyleProperty("Color", 
                                             self.setForegroundColor,  
                                             self.selector,
                                             default=self.instrument.foreground().color(),
                                             minimum=0, maximum=0), 
                      FontStyleProperty("Font", self.instrument.setFont, self.selector,
                                        default=FontStyleWrapper(self.instrument.font()),
                                        minimum=0, maximum=0,)]
                                        ## model = FontModel),]

  
  def applyToCursor(self, cursor):
    ''' Effect deferred method. '''
    '''
    Alternatively, setCharFormat.
    Merging leaves some style unchanged, e.g. block format if char format is being merged?
    '''
    cursor.mergeCharFormat(self.instrument)
    
    
  def setForegroundColor(self, color):
    '''
    Setter for foreground color.
    
    Adapter: Qt has no direct setter for this property.
    Indirect: get brush, set color on brush, set brush.
    Get brush gets a copy of brush that must be reset onto the format.
    Just :get brush, set color on brush: has no effect.
    '''
    brush = self.instrument.foreground()
    brush.setColor(color)
    brush.setStyle(Qt.SolidPattern) # HACK: doesn't allow brush pattern editable by user
    self.instrument.setForeground(brush)
    
    
  # No setBackgroundColor(), see notes in class docstring
    
'''
At one stage of development,
the setter was self.instrument.foreground().setColor.
But that apparently justs sets color on a brush copy, not affecting text.
So applyToCursor was calling setForegroundColor()
(and it was resetting brush.)


Notes:

TODO instrument.setTextOutline(QPen) another StyleProperty ???

TODO brush.setStyle(Qt.SolidPattern) another StyleProperty so can have non-filled Shapes or non-filled Text ???

'''
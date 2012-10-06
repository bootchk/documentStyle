'''
'''

from PySide.QtCore import Qt
from PySide.QtGui import QTextCharFormat
from textFormation import TextFormation
from instrumentFormation import InstrumentFormation
from ..styleProperty import ColorStyleProperty, FontStyleProperty


class CharacterFormation(TextFormation):
  '''
  Styling attributes of characters.
  
  Specialize to Qt <QTextCharFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Character", parentSelector=parentSelector)
    self.base = QTextCharFormat()
    self.styleProperties=[ColorStyleProperty("Color", 
                                             self.base.foreground().setColor, self.base.foreground().color, self.selector(),
                                             0, 0), 
                      FontStyleProperty("Font", self.base.setFont, self.base.font, self.selector(), 0, 0),]
  
  
  def applyToCursor(self, cursor):
    ''' Effect deferred method. '''
    
    '''
    For some reason, StyleProperty calling the setter doesn't work.
    The QBrush object seems to change.
    (May be a bug in PySide?? or my improper understanding of it.)
    (Elsewhere, StyleProperty calling the setter does seem to work.)
    So this hack sets the QBrush at the last moment, using cached value of the StyleProperty.
    '''
    brush = self.base.foreground()
    brush.setColor( self.styleProperties[0].get() ) # HACK: hardcoded
    brush.setStyle(Qt.SolidPattern) # HACK: doesn't allow brush pattern editable by user
    self.base.setForeground(brush)
  
    
    """
    # debugging why QBrush setter doesn't work.
    print "applyToCursor: Property setter", self.styleProperties[0].setter
    print "applyToCursor setter: ", brush.setColor
    print "applyToCursor: color", brush.color()
    print "applyToCursor: brushStyle", brush.style()
    print "applyToCursor:  brush", brush
    #print "applyToCursor: brush again", brush
    """
    
    cursor.mergeCharFormat(self.base)
    
'''
Notes:

TODO base.setTextOutline(QPen) another StyleProperty ???

TODO brush.setStyle(Qt.SolidPattern) another StyleProperty so can have non-filled Shapes or non-filled Text ???

Scraps:

'''
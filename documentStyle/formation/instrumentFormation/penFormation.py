'''

'''
from PySide.QtCore import Qt
from PySide.QtGui import QPen
from instrumentFormation import InstrumentFormation
from ..styleProperty import ColorStyleProperty, IntStyleProperty, ComboBoxStyleProperty

class PenFormation(InstrumentFormation):
  '''
  Specialize to Qt <QPen>
  
  Redefine:
  - applyTo()
  '''
  
  
  def __init__(self, parentSelector):
    '''
    '''
    InstrumentFormation.__init__(self, name="Pen", parentSelector=parentSelector)
    self.base = QPen()
    self.styleProperties=[ColorStyleProperty("Color", self.base.setColor, self.base.color, self.selector()), 
                          IntStyleProperty("Width", self.base.setWidth, self.base.width, self.selector(), 0, 10),
                          ComboBoxStyleProperty("Style", self.base.setStyle, self.base.style, self.selector(),
                                                model = Qt.PenStyle)
                          ]


  def applyTo(self, morph):
    morph.setPen(self.base)
    


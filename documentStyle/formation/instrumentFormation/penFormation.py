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
  
  # TODO: a QPen has a QBrush also, and it needs to be scaled also
  
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
    '''
    Apply my instrument to DocumentElement
    
    Assert this formation's values are propagated to base via editing (which calls Instrument.setters())
    '''
    morph.scalePen(self.base, self.styleProperties[1].resettableValue.value())
    morph.setPen(self.base)
    

  def scaledPropagateToInstrument(self, morph):
    '''
    Propagate my values that are transformed,
    after unscaling by the local (item) transform.
    
    Where a DocumentElement has a transform that is used to size it
    (e.g. when the DocumentElement comprises a unit shape, scaled to size.)
    TODO when item transform is 2D and not uniform in x, y???
    
    This is not undoing viewing transform, only local transform.
    
    For a Pen in Qt, width property.
    Note that in Qt, QPen.setWidth() also affects the QPen's QBrush.
    '''
    unscaledWidth = self.styleProperties[1].resettableValue.value()
    itemScale = morph.scale()
    scaledWidthF = 1.0/itemScale * unscaledWidth
    
    # !!! Note float value and setWidthF is float setter
    self.base.setWidthF(scaledWidthF)
    print "PenFormation.applyTo width: item scale, unscaled width, scaled width", itemScale, unscaledWidth, scaledWidthF, " on morph", morph
    
    
    
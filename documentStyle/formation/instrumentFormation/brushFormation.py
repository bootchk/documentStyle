'''
'''
from PySide.QtCore import Qt
from PySide.QtGui import QBrush #, QTransform
from instrumentFormation import InstrumentFormation
from ..styleProperty import ColorStyleProperty, ComboBoxStyleProperty

class BrushFormation(InstrumentFormation):
  ''' Specialize to Qt <QBrush> '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Brush", parentSelector=parentSelector)
    self.base = QBrush()
    self.styleProperties=[ColorStyleProperty("Color", self.base.setColor, self.base.color, self.selector()),
                          ComboBoxStyleProperty("Pattern", 
                                                self.base.setStyle, self.base.style, self.selector(),
                                                model = Qt.BrushStyle),]
    '''
    sic, BrushPattern is called Style in Qt
    
    Need Pattern, since defaults to NoBrush and that means color is moot.
    If we just have Color, once it is set, no way to go back to unfilled.
    
    TODO: user friendly:  if user chooses color, ensure pattern is not NoBrush
    '''
    
    # TODO gradients and texture not working?
  
  
  def applyTo(self, morph):
    #print "setBrush on morph", self.base.color()
    ##self.scaledPropagateToInstrument(morph)
    morph.setBrush(self.base) 
  
  
  """
  def scaledPropagateToInstrument(self, morph):
    '''
    Propagate my values that are transformed,
    after unscaling by the local (item) transform.
    '''
    unscaledWidth = self.styleProperties[1].resettableValue.value()
    # TODO wrong property
    itemScale = morph.scale()
    scaledWidthF = 1.0/itemScale * unscaledWidth
    
    # !!! Note float value and setWidthF is float setter
    transform = QTransform()
    transform.scale(scaledWidthF, scaledWidthF)
    self.base.setTransform(transform)
    print "BrushFormation.applyTo setPen.width ", unscaledWidth, scaledWidthF, " on morph", morph
  """
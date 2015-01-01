
from PyQt5.QtGui import QBrush

from .instrumentFormation import InstrumentFormation
from documentStyle.styleProperty.styleProperty import BaseStyleProperty
from documentStyle.styleProperty.resettableValue import ResettableColorValue
from documentStyle.ui.layout.typedStylePropertyLayout import ColorStylePropertyLayout, ComboBoxStylePropertyLayout
import documentStyle.config as config



class BrushFormation(InstrumentFormation):
  ''' Specialize to Qt <QBrush> '''
  
  def __init__(self, parentSelector, role=""):
    
    InstrumentFormation.__init__(self, name="Brush", parentSelector=parentSelector, role=role)
    self.instrument = QBrush()
    self.styleProperties=[BaseStyleProperty("Color", self.instrument.setColor, self.selector,
                                            resettableValueFactory=ResettableColorValue,
                                            layoutFactory=ColorStylePropertyLayout,
                                            default=self.instrument.color()),
                          BaseStyleProperty("Style", # Was Pattern
                                            self.instrument.setStyle, self.selector,
                                            default=self.instrument.style(),
                                            # ResettableIntValue defaults and works
                                            layoutFactory=ComboBoxStylePropertyLayout,
                                            domainModel = config.BrushModel),]
    
    '''
    sic, BrushPattern is called Style in Qt
    
    Need Pattern, since defaults to NoBrush and that means color is moot.
    If we just have Color, once it is set, no way to go back to unfilled.
    
    TODO: user friendly:  if user chooses color, ensure pattern is not NoBrush
    '''
    
    # TODO gradients and texture not working?
  
  
  def applyTo(self, morph):
    #print "setBrush on morph", self.instrument.color()
    
    # Morph knows it's scale and applies it to self instrument
    morph.scaleInstrument(self.instrument)  # No baseValue, defaults to 1
    # Tell Morph to use self.instrument to draw itself
    morph.setBrush(self.instrument) 
  
  
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
    self.instrument.setTransform(transform)
    #print "BrushFormation.applyTo setPen.width ", unscaledWidth, scaledWidthF, " on morph", morph
  """
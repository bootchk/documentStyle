
from PyQt5.QtGui import QPen
from .instrumentFormation import InstrumentFormation
from documentStyle.styleProperty.styleProperty import BaseStyleProperty
from documentStyle.userInterface.layout.typedStylePropertyLayout import IntStylePropertyLayout, ColorStylePropertyLayout, ComboBoxStylePropertyLayout
import documentStyle.config as config

#from documentStyle.styleWrapper.styleWrapper import PenStyleWrapper


class PenFormation(InstrumentFormation):
  '''
  Specialize to Qt <QPen>
  
  Redefine:
  - applyTo()
  '''
  
  # TODO: a QPen has a QBrush also, and it needs to be scaled also
  
  def __init__(self, parentSelector, role=""):
    InstrumentFormation.__init__(self, name="Pen", parentSelector=parentSelector, role=role)
    self.instrument = QPen()
    self.styleProperties=[BaseStyleProperty("Color", self.instrument.setColor, self.selector,
                                             layoutFactory=ColorStylePropertyLayout,
                                             default = self.instrument.color()), 
                          BaseStyleProperty("Width", self.instrument.setWidth, self.selector,
                                           default=self.instrument.width(),
                                           layoutFactory=IntStylePropertyLayout,
                                          minimum=0, maximum=10, singleStep=1),
                          BaseStyleProperty("Style", self.instrument.setStyle, 
                                            self.selector,
                                            default=self.instrument.style(), # PySide PenStyleWrapper(self.instrument.style()),
                                            layoutFactory=ComboBoxStylePropertyLayout,
                                            domainModel = config.PenModel)
                          ]
  '''
  Old getters: self.instrument.color, ), 
  self.instrument.width, 
  self.instrument.style, 
  '''


  def applyTo(self, morph):
    '''
    Assert this formation's values have already been applied to instrument via editing (which calls Instrument.setters())
    What remains is to set the instrument to the morph.
    Also, scale instrument correlated with scale of morph.
    '''
    # Callback morph API: only morph knows its scale, and how to inversely scale drawing instrument
    morph.scaleInstrument(self.instrument, baseValue=self.styleProperties[1].resettableValue.value)
    morph.setPen(self.instrument)
    
  """
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
    self.instrument.setWidthF(scaledWidthF)
    #print "PenFormation.applyTo width: item scale, unscaled width, scaled width", itemScale, 
    unscaledWidth, scaledWidthF, " on morph", morph
  """
    
    
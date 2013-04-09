'''
'''

from format.opacityFormat import POpacityFormat
from instrumentFormation import InstrumentFormation
from formation.styleProperty import FloatStyleProperty

class OpacityFormation(InstrumentFormation):
  '''
  Styling attributes of solvent instrument (opacity.)
  
  Specialize to our own <POpacityFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Opacity", parentSelector=parentSelector)
    self.base = POpacityFormat()
    self.styleProperties=[FloatStyleProperty("Opacity", self.base.setOpacity, self.base.opacity, self.selector(), 0.0, 1.0), ]
  
  
  def applyTo(self, morph):
    morph.setOpacity(self.base.opacity()) 

    
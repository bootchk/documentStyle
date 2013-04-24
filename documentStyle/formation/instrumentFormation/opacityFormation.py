'''
'''

from documentStyle.instrument.opacityInstrument import POpacityInstrument

from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation
from documentStyle.formation.styleProperty import FloatStyleProperty

class OpacityFormation(InstrumentFormation):
  '''
  Styling attributes of solvent instrument (opacity.)
  
  Specialize to our own <POpacityFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Opacity", parentSelector=parentSelector)
    self.instrument = POpacityInstrument()
    self.styleProperties=[FloatStyleProperty("Opacity", self.instrument.setOpacity, self.instrument.opacity, self.selector, 0.0, 1.0), ]
  
  
  def applyTo(self, morph):
    '''
    Unlike other InstrumentFormations, can't directly set Instrument on DocumentElement, only its value.
    '''
    morph.setOpacity(self.instrument.opacity()) 

  
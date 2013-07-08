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
    # !!! minimum is 0.1 otherwise it dissappears and user can't access
    self.styleProperties=[FloatStyleProperty("Opacity", 
                                             self.instrument.setOpacity,  self.selector,
                                             default=self.instrument.opacity(),
                                             minimum=0.1, maximum=1.0), ]
  
  
  def applyTo(self, morph):
    '''
    Unlike other InstrumentFormations, can't directly set Instrument on DocumentElement, only its value.
    '''
    morph.setOpacity(self.instrument.opacity()) 

  
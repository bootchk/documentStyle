
from documentStyle.instrument.opacityInstrument import OpacityInstrument

from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation
from documentStyle.styleProperty.styleProperty import BaseStyleProperty
from documentStyle.userInterface.layout.typedStylePropertyLayout import FloatStylePropertyLayout
from documentStyle.styleProperty.resettableValue import ResettableFloatValue


class OpacityFormation(InstrumentFormation):
  '''
  Styling attributes of solvent instrument (opacity.)
  
  Specialize to our own <POpacityFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Opacity", parentSelector=parentSelector)
    self.instrument = OpacityInstrument()
    # !!! minimum is 0.1 otherwise it dissappears and user can't access
    self.styleProperties=[BaseStyleProperty("Opacity", 
                                         self.instrument.setOpacity,  
                                         self.selector,
                                         resettableValueFactory=ResettableFloatValue,
                                         layoutFactory=FloatStylePropertyLayout,
                                         default=self.instrument.opacity(),
                                         minimum=0.1, maximum=1.0), 
                          ]
  
  
  def applyTo(self, morph):
    '''
    Unlike other InstrumentFormations, can't directly set Instrument on DocumentElement, only its value.
    '''
    morph.setOpacity(self.instrument.opacity()) 

  
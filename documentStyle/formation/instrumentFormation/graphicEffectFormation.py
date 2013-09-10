'''
'''

from PyQt4.QtGui import QGraphicsBlurEffect, QGraphicsDropShadowEffect, QGraphicsEffect

from documentStyle.instrument.graphicEffectInstrument import PGraphicEffectInstrument
from documentStyle.formation.instrumentFormation.instrumentFormation import InstrumentFormation
from documentStyle.formation.styleProperty import ComboBoxStyleProperty
from documentStyle.formation.styleProperty import UnwrappedComboBoxStyleProperty
from documentStyle.model.graphicEffect import graphicEffectModel



'''
Unlike other Qt Formats, change ownership
when applied to a DocumentElement.
I.E. DocumentElement takes ownership of a QGraphicsEffect and may delete it
when a new QGraphicsEffect is applied.

Hence, we create a new QGraphicsEffect whenever applied to a DocumentElement
'''

# workaround for Qt bug: effects being deleted, ownership issues
# Keep a copy of all effects applied to DocumentElements, so Python doesn't delete them
# Symptoms: apply effects and Qt doesn't draw them
effects = []



class GraphicEffectFormation(InstrumentFormation):
  '''
  Styling attributes of filter instrument (graphics effect.)
  
  Specialize to <PGraphicEffectInstrument>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Graphic Effect", parentSelector=parentSelector)
    self.instrument = PGraphicEffectInstrument()
    self.styleProperties=[UnwrappedComboBoxStyleProperty("Graphic Effect", 
                                                self.instrument.setGraphicEffect, self.selector,
                                                default=self.instrument.graphicEffect(),
                                                model = graphicEffectModel)]  
  
  
  def applyTo(self, morph):
    effect = self.adaptEncoding(self.instrument.graphicEffect())
    
    global effects
    effects.append(effect)
    
    morph.setGraphicsEffect(effect)
    
  
  # TODO this should be a StyleWrapper ?
  def adaptEncoding(self, codedValue):
    '''
    Adapt coded value to a QGraphicEffect value
    '''
    adaptedValue = None
    if codedValue == 1:
      adaptedValue = QGraphicsBlurEffect()
    elif codedValue == 2:
      adaptedValue = QGraphicsDropShadowEffect()
    #print "Adapted graphic effect:", adaptedValue
    assert adaptedValue is None or isinstance(adaptedValue, QGraphicsEffect)
    return adaptedValue
    


    
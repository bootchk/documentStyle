'''
'''

from PySide.QtGui import QGraphicsBlurEffect, QGraphicsDropShadowEffect, QGraphicsEffect

from format.graphicEffectFormat import PGraphicEffectFormat
from instrumentFormation import InstrumentFormation
from formation.styleProperty import ComboBoxStyleProperty


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


class Model(object):
  '''
  Mimics a PySide enum: has "values" attribute that is a dictionary
  '''
  def __init__(self):
    self.values = {"None": 0,  # In Qt, does not exist NullGraphicsEffect
                   "Blur": 1,
                   "Drop Shadow": 2 }
    # TODO other effects
  
graphicEffectModel = Model()



class GraphicEffectFormation(InstrumentFormation):
  '''
  Styling attributes of filter instrument (graphics effect.)
  
  Specialize to <PGraphicEffectFormat>
  '''
  
  def __init__(self, parentSelector):
    InstrumentFormation.__init__(self, name="Graphic Effect", parentSelector=parentSelector)
    self.base = PGraphicEffectFormat()
    self.styleProperties=[ComboBoxStyleProperty("Graphic Effect", 
                                                self.base.setGraphicEffect, self.base.graphicEffect, self.selector(),
                                                model = graphicEffectModel)]  
  
  
  def applyTo(self, morph):
    effect = self.adaptEncoding(self.base.graphicEffect())
    
    global effects
    effects.append(effect)
    
    morph.setGraphicsEffect(effect)
    
    
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
    


    
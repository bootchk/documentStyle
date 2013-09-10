'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PyQt4.QtCore import QObject # ???

'''
See instrument.py
'''

class PGraphicEffectInstrument(QObject):  # QObject so members memory managed??
  '''
  Contain GraphicEffect parameters.
  '''
  def __init__(self):
    # Here 0 is the NullGraphicEffect
    self.graphicEffectValue = 0  # This should be the same as the framework's default
    

  def setGraphicEffect(self, value):
    self.graphicEffectValue = value
    
    
  def graphicEffect(self):
    return self.graphicEffectValue

        
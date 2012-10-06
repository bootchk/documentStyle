'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

from PySide.QtCore import QObject # ???

'''
"...Format" Objects which the Qt framework does not supply,
but similar API to Q...Format objects e.g. QBrushFormat

A ...Format object has stereotype: information holder.
It is simply a set of parameters.
'''

class PGraphicEffectFormat(QObject):  # QObject so members memory managed??
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

        
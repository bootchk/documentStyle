'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

'''
see instrument.py
'''

class OpacityInstrument(object):
  '''
  Contain opacity parameters.
  
  There is no corresponding Qt object to inherit from.
  StyleProperty knows how to apply to a Morph.
  TODO we could migrate that here.
  '''
  def __init__(self):
    self.opacityValue = 1.0 # This should be the same as the framework's default
    

  def setOpacity(self, value):
    self.opacityValue = value
    
    
  def opacity(self):
    return self.opacityValue

        
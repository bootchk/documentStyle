'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

'''
"...Format" Objects which the Qt framework does not supply,
but similar API to Q...Format objects e.g. QBrushFormat

A ...Format object has stereotype: information holder.
It is simply a set of parameters.
'''

class POpacityFormat(object):
  '''
  Contain opacity parameters.
  '''
  def __init__(self):
    self.opacityValue = 1.0 # This should be the same as the framework's default
    

  def setOpacity(self, value):
    self.opacityValue = value
    
    
  def opacity(self):
    return self.opacityValue

        
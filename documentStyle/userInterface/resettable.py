'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

class Resettable(object):
  '''
  Resettable behaviour for value holding widget.
  
  Widget has-a ResettableValue.
  Keep Widget and ResettableValue corresponding.
  '''


  def __init__(self, resettableValue):
    self.resettableValue = resettableValue
    self.setValue(self.resettableValue.value())
      
  def reset(self):
    ''' Reset value of widget and its ResettableValue. '''
    self.resettableValue.reset()
    self.setValue(self.resettableValue.value())
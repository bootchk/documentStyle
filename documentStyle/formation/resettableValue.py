'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

class ResettableValue(object):
  '''
  A value whose current value can be reset to an original value,
  and whose current value can be rolled into original value.
  
  Responsibilities:
  - know original value and current value
  - knows reset state
  - 
  '''
  
  def __init__(self, originalValue):
    self._value = originalValue
    self._originalValue = originalValue
    self._isReset = True
    self._wasReset = False
    
    
  def __str__(self):
    return "ResettableValue(original=" + str(self._originalValue) + " value=" + str(self._value)
  
  
  def setValue(self, newValue):
    ''' To resettable state if new value is different from original. '''
    self._isReset = newValue == self._originalValue
    self._value = newValue
    
    
  def value(self):
    return self._value
  
  
  def reset(self):
    ''' Restore current value to original value. '''
    assert not self._isReset
    self._value = self._originalValue
    self._isReset = True
    self._wasReset = True
    
  def isReset(self):
    ''' is current value same as original? '''
    return self._isReset
    
  def wasReset(self):
    ''' was reset() invoked? '''
    return self._wasReset
    
    
  def roll(self):
    ''' Current value becomes new original value. '''
    self.__init__(originalValue = self._value)
    

        
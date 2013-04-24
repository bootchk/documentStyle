'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

# TODO get rid of all these getter,setters: use properties

from documentStyle.debugDecorator import report


class ResettableValue(object):
  '''
  A value whose current value can be reset to an original value,
  and whose current value can be rolled into original value.
  
  Responsibilities:
  - know original value and current value
  - knows reset state
  '''
  
  def __init__(self, originalValue):
    self._value = originalValue
    self._originalValue = originalValue
    self._wasReset = False
    
    
  def __str__(self):
    return "ResettableValue(original=" + str(self._originalValue) + " value=" + str(self._value)
  
  
  def setValue(self, newValue):
    self._value = newValue
    
    
  def value(self):
    return self._value
  
  
  @report
  def reset(self):
    ''' 
    Restore current value to original value. 
    At behest of user.
    '''
    assert not self.isReset()
    self._value = self._originalValue
    self._wasReset = True
    
    
  def isReset(self):
    ''' 
    is current value same as original? 
    
    Note not a state variable (computed), so there is no programming struggle to maintain.
    '''
    result = self._originalValue == self._value
    #print "isReset", self._originalValue, self._value, result
    return result
    
    
  def wasReset(self):
    ''' was reset() invoked by user? '''
    return self._wasReset
    
    
  def roll(self):
    '''
    Current value becomes new original value. 
    AND _wasReset becomes False.
    '''
    self.__init__(originalValue = self._value)
    

        
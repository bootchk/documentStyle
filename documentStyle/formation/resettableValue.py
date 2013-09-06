'''
Copyright 2012 Lloyd Konneker

This is free software, covered by the GNU General Public License.
'''

# TODO get rid of all these getter,setters: use properties

from documentStyle.debugDecorator import reportReturn


class ResettableValue(object):
  '''
  A value whose current value can be reset to an valueToResetTo,
  and whose current value can be rolled into valueToResetTo.
  
  Responsibilities:
  - know valueToResetTo and current value
  - knows reset state
  
  FUTURE:
  - know 'isInlined' i.e. is overridden
  This distinguishes values set by the program (for an existing in-line StylingAct)
  from values set by the user editing (in creating a new in-line StylingAct.)
  In other words, if the program sets a value for an in-line StylingAct, isReset becomes False,
  which is distinct from a user editing the value, where also isReset becomes False.
  An optimization for deleting existing StylingActs,
  but not absolutely necessary.
  '''
  
  def __init__(self, valueToResetTo):
    self._value = valueToResetTo
    self._valueToResetTo = valueToResetTo
    self._isReset = True
    
    
  def __str__(self):
    return "ResettableValue(original=" + str(self._valueToResetTo) + " value=" + str(self._value)
  
  
  @reportReturn
  def setValue(self, newValue):
    '''
    Setting value always changes state to not isReset, even if value equals valueToResetTo.
    IOW, setValue 'touches' and isReset() means 'not touched.'
    If the GUI calls setValue() to what it thinks is valueToResetTo,
    it should also call reset() to set the state.
    '''
    self._value = newValue
    self._isReset = False
    
    
  def value(self):
    return self._value
  
  
  @reportReturn
  def reset(self):
    ''' 
    Restore current value to valueToResetTo. 
    At behest of user.
    '''
    if self._isReset:
      #print "Resetting twice?"
      pass
    self._value = self._valueToResetTo
    self._isReset = True

    
  @reportReturn
  def isReset(self):
    ''' A getter for convenience of debugging. '''
    return self._isReset
    
    
  def roll(self):
    '''
    Current value becomes new valueToResetTo. 
    AND _wasReset becomes False.
    '''
    self.__init__(valueToResetTo = self._value)
    

        
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
    # OLD when value was not a property: self.setValue(self.resettableValue.value())
    self.setValue(self.resettableValue.value)
      
      
  def doUserReset(self):
    ''' 
    User has indicated (clicked BuddyButton) desire for reset.
    Called by BuddyButton, but it also emits userReset.
    This must get done first, since setValue will emit valueChanged,
    whose handler will buddyButton.setEnabled() to a wrong state.
    '''
    # change model's value and state to reset value and state
    self.resettableValue.isReset = True
    # changing view emits viewChanged, which changes model value (again) and state to isReset==False
    self.setValue(self.resettableValue.value) # model->view
    # !!! change model state back to isReset, since above setValue just changed it.
    self.resettableValue.isReset = True
    assert self.resettableValue.isReset == True
    